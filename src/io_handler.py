'''
This file handles the I/O of the script 🤔🤔🤔🤔
'''
import os
import json

# Prints to console
def log(output, level=None):
  print('\033[1m%s\033[0m\t%s' % (level, output))

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

# Opens the file, extracts information and returns it as array
def open_file(file):
  file_data = []

  try:
    with open(file, 'r') as data:
      file_data = [line for line in data]

  except IOError as e:
    log_to_file('No file found for path.\n\n' + str(e))

  finally:
    return file_data