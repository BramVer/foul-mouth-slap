'''Handles all I/O in the application.

All input and/or output in the application is defined and handled here.
'''
import sys
import os
import re
import toml
import subprocess


def get_absolute_path_for_script():
  absolute_path = sys.argv[0][:-10]

  return absolute_path

def log_final_verdict(violations):
  print('😱😱😱😤😤 Foul mouthed words found 😤😤😱😱😱')
  for index, viol in enumerate(violations):
    print('%u: %s' % (index, viol.replace("\n", "")))

def format_violation_report(violation, line):
  return "%s found in line: \t%s" % (violation, line)


def open_file_by_lines(file_path):
  file_data = []

  try:
    with open(file_path, 'r') as data:
      file_data = [line for line in data]

  except IOError as e:
    log('No file found for path:\n\n' + str(e))

  finally:
    return file_data

def get_file_type(filename):
  # Build the regex - everything after the last '.'
  regex = re.search(r'([^.]*$)', filename, re.I)

  return regex.group()

def format_and_categorize_git_status(input):
  output = {}
  status_dict = {
    'M': 'modified',
    '??': 'new',
  }

  for i in input.splitlines():
    file_status = status_dict.get(i[:2], 'new')

    if output.get(file_status) is None:
      output[file_status] = []

    output[file_status].append(i[3:])

  return output

def get_repository_status():
  status = {}
  git_binary = get_config().get('executable', {}).get('path_to_git_binary')

  try:
    status = subprocess.check_output([git_binary, "status", "-s"], stderr=subprocess.STDOUT).decode('utf-8')
    status = format_and_categorize_git_status(status)

  except subprocess.CalledProcessError:
    # There was a problem calling "git status".
    print("Oops...")

  return status

def get_diff_of_file(filename):
  diff = ''
  git_binary = get_config().get('executable').get('path_to_git_binary')

  try:
    diff = subprocess.check_output([git_binary, "diff", "--minimal", "--cached", filename], stderr=subprocess.STDOUT).decode('utf-8')

  except subprocess.CalledProcessError:
    print("Oops...")

  return diff

def get_location_of_changes_in_file(diff):
  locations = []

  # Build the regex - everything after the last '.'
  matches = re.finditer(r"@@ -(.*),.* +.*,(.*) @@", diff, re.MULTILINE)
  for match in matches:
    start =  int(match.group(1))
    end = start + int(match.group(2))

    locations.append({'start': start, 'end': end})

  return locations


def get_modified_file_contents(filename):
  output = []

  diff = get_diff_of_file(filename)
  location = get_location_of_changes_in_file(diff)
  content = open_file_by_lines(filename)

  for loc in location:
    start = loc.get('start')
    end = loc.get('end')

    output.extend(content[start:end])

  return output

def get_config():
  config_dict = {}

  try:
    absolute_path = get_absolute_path_for_script()
    config_dict = toml.load(os.path.abspath('%s/../config.toml' % absolute_path))
  except Exception as e:
    print("Could not load configuration file")

  return config_dict

def get_foul_definition_for_type(definition, type):
  violations_dict = get_violations_dict()

  all_foul_definition = violations_dict.get('all', {}).get('foul', {}).get(definition, [])
  type_foul_definition = violations_dict.get(type, {}).get('foul', {}).get(definition, [])
  type_acceptable_definition = violations_dict.get(type, {}).get('acceptable', {}).get(definition, [])

  return [defin for defin in all_foul_definition + type_foul_definition if defin not in type_acceptable_definition]

def get_foul_patterns_for_type(type):
  return get_foul_definition_for_type('patterns', type)

def get_foul_words_for_type(type):
  return get_foul_definition_for_type('words', type)

def get_acceptable_patterns_for_type(type):
  violations_dict = get_violations_dict().get('foul_mouthed_blabber', {})

  all_acceptable_patterns = violations_dict.get('all', {}).get('acceptable', {}).get('patterns', [])
  type_acceptable_patterns = violations_dict.get(type, {}).get('acceptable', {}).get('patterns', [])

  return [pattern for pattern in all_acceptable_patterns + type_acceptable_patterns]
 
def get_violations_dict():
  violations_dict = {}

  try:
    absolute_path = get_absolute_path_for_script()
    violations_dict = toml.load(os.path.abspath('%s/../assets/word_list.toml' % absolute_path))
  except Exception as e:
    print("Could not load violations configuration")

  return violations_dict