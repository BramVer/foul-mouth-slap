'''Contains the calls to git.

Gets the staged files, the location of modified contents etc.
'''

import re
import subprocess

from log_handler import log_to_user
from config_handler import get_config


def _check_if_valid_staged_files_output(staged_files_output: str) -> bool:
  '''Checks if the input complies with the known output format.'''
  regex = re.search(r'^[ADRM]\ .*$', staged_files_output)
  if regex and regex.group():
    return True

  return False

def _categorize_staged_files(staged_files_output: str) -> list:
  '''Determines status of staged files based on the diff it receives.

  Return a list of tuples with ('STATUS', 'file_name').
  Unknown status will be marked as 'new' for now.
  '''
  output = []
  status_dict = get_status_dict()

  for line in staged_files_output.splitlines():
    if _check_if_valid_staged_files_output(line):
      file_status = status_dict.get(line[0], 'new')
      output.append((file_status, line[2:]))     # Omits the status and spacedelimiter

  return output

def _get_diff_of_file(file_name: str) -> str:
  '''Executes a git diff for the file against HEAD.'''
  diff = ''
  git_binary = get_config().get('executable', {}).get('path_to_git_binary')

  try:
    diff = subprocess.check_output(
        [git_binary, "diff", "--minimal", "--cached", file_name],
        stderr=subprocess.STDOUT)
    diff = diff.decode('utf-8')

  except subprocess.CalledProcessError as cpe:
    log_to_user("Something went wrong getting the diff against HEAD for file %s." % file_name)
    log_to_user(cpe)

  return diff


def get_status_dict() -> dict:
  '''Returns the predefined set of status codes and explanations.'''
  status_dict = {
    'D': 'deleted',
    'A': 'new',
    'R': 'renamed',
    'M': 'modified',
  }

  return status_dict

def get_staged_files_per_status() -> list:
  '''Gets the files staged for current commit.'''
  files_per_status = []
  git_binary = get_config().get('executable', {}).get('path_to_git_binary')

  if git_binary is None:
    return files_per_status

  try:
    staged_files = subprocess.check_output(
        [git_binary, "diff", "--name-status", "--cached"],
        stderr=subprocess.STDOUT
    )
    files_per_status = _categorize_staged_files(staged_files.decode('utf-8'))

  except subprocess.CalledProcessError as cpe:
    log_to_user("Something went wrong while getting the staged files ready for the commit.")
    log_to_user(cpe)

  return files_per_status

def get_changed_locations_in_file(file_name) -> list:
  '''Regexes a diff to extract the extract location of changes.

  If no location of changes is found, it means the file is not present in HEAD,
  meaning it is not yet tracked, aka new.
  We could do a check here to see if any content got added,
  but it doesn't add enough value to implement for now.
  '''
  locations = []

  diff = _get_diff_of_file(file_name)

  # Find the location of the excerpt based on the location of the new content.
  matches = re.finditer(r"\n@@ .*\+(.*),(.*) @@", diff, re.MULTILINE)
  for match in matches:
    start =  int(match.group(1))
    end = start + int(match.group(2))

    locations.append({'start': start, 'end': end})

  return locations
