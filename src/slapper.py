#!/usr/bin/python

# TODO:
# [ ] read all files
# [x] construct a list of words i use when i have a foul-mouth
# [ ] set up some rules about other words
# [ ] detect variants of words
# [ ] write them permanently to list of foul-words.txt

import subprocess
import sys
import os
import re
import collections

from fuzzywuzzy import fuzz

import io_handler as io
import constants as cnt   # Hehe, get it?


# Read foul_words
try:
  foul_words = io.open_file(cnt.foul_words_path)

  # Check all files in the staging-area:
  text = subprocess.check_output(
    [cnt.git_binary_path, "status", "--porcelain", "-uno"],
    stderr=subprocess.STDOUT
  ).decode("utf-8")

  file_list = text.splitlines()

  # Get paths from file_list and go over all files:
  for fname in [n[3:] for n in file_list]:
    fcontents = io.open_file(fname)

    # Loop over lines in file
    for index, line in enumerate(fcontents):
      for fw in [fw[:len(fw)-1] for fw in foul_words]:
        # If a foul word is in the line
        if fw in line:
          io.log(
            'ERROR',
            fname,
            index,
            'You have used the foul word \'%s\'. Know you no shame?' % (fw),
          )
          sys.exit(1)

        # If a variant of a foul word is in the line
        elif fuzz.partial_ratio(fw, line) > 90:
            io.log(
              'ERROR',
              fname,
              index,
              'You have used a version of the word \'%s\' tsktsktsk.' % (fw),
            )
            sys.exit(1)

        # If a char is repeated too often
        else:
          for i, w in enumerate(line):
            if w not in cnt.acceptable_chars and i-2 >= 0:
              if w == line[i-1] and w == line[i-2]:
                io.log(
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