#!/usr/bin/python

# TODO:
# [x] read all files
#  - [ ] Look only at the staged files 
#  - [ ] Look at the file names
# [x] construct a list of words i use when i have a foul-mouth
# [x] set up some rules about other words
# [x] detect variants of words
# [ ] write them permanently to list of foul-words.txt

import os
import re
import sys
import json
import subprocess

from fuzzywuzzy import fuzz


# Constants
git_binary_path = "/usr/bin/git"
foul_words_path = "/home/darm/DEV/foul-mouth-slap/assets/foul-words.txt"
acceptable_chars = [
  ' ',
  '=',
  '-',
  '.',
  '"',
  "'",
]

# Prints to console
def log(level, filename, line, felony):
  print('\033[1m%s\033[0m \t- In file %s on line: %s \t- %s' % (level, filename, line, felony))

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


# Read foul_words
try:
  foul_words = open_file(foul_words_path)

  # Check all files in the staging-area:
  text = subprocess.check_output(
    [git_binary_path, "status", "--porcelain", "-uno"],
    stderr=subprocess.STDOUT
  ).decode("utf-8")

  file_list = text.splitlines()

  # Get paths from file_list and go over all files:
  for fname in [n[3:] for n in file_list]:
    fcontents = open_file(fname)

    # Loop over lines in file
    for index, line in enumerate(fcontents):
      for fw in [fw[:len(fw)-1] for fw in foul_words]:
        # If a foul word is in the line
        if fw in line:
          log(
            'ERROR',
            fname,
            index,
            'You have used the foul word \'%s\'. Know you no shame?' % (fw),
          )
          sys.exit(1)

        # If a variant of a foul word is in the line
        elif fuzz.partial_ratio(fw, line) > 90:
            log(
              'ERROR',
              fname,
              index,
              'You have used a version of the word \'%s\' tsktsktsk.' % (fw),
            )
            sys.exit(1)

        # If a char is repeated too often
        else:
          for i, w in enumerate(line):
            if w not in acceptable_chars and i-2 >= 0:
              if w == line[i-1] and w == line[i-2]:
                log(
                  'ERROR',
                  fname,
                  index,
                  'You have repeated the char \'%s\' like an obnoxious oaf!' % (w),
                )
                sys.exit(1)

  # Everything seams to be okay:
  print("No foul words found.")
  sys.exit(0)

except subprocess.CalledProcessError:
  # There was a problem calling "git status".
  print("Oops...")
sys.exit(12)