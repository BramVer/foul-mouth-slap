'''
This file handles the I/O of the script 🤔🤔🤔🤔
'''
import os
import json


# Writes all output to a file
def log_to_file(output, write_mode=None, same_line=None, bold=None):
  try:
    target_file = 'output_log.txt'
    write_mode = 'a' if not write_mode else write_mode

    print('\033[1m%s\033[0m' % output if bold else output)
    with open(target_file, write_mode) as log_file:
      if not type(output) == str:
        json.dump(output, log_file)
      else:
        log_file.writelines(output)

      if not same_line:
        log_file.writelines('\n')

  except Exception as e:
    print('Exception while logging\n\n', str(e))

# Appends set of lines to file
def write_word_to_file(word):
  try:
    path = os.path.join('assets', 'foul-words.txt')

    if os.path.exists(path):
      with open(path, 'a') as file:
        file.writelines(content)

  except Exception as e:
    log_to_file(
      'Something went wrong while appending..\n\n' + 
      'Line: %s\n\nException: %s' % (word, str(e))
    )

# Opens the file, extracts information and calls init func
def open_file(file):
  file_data = []

  try:
    with open(file, 'r') as data:
      file_data = [line for line in data]

  except IOError as e:
    log_to_file('No file found for path.\n\n' + str(e))

  finally:
    return file_data