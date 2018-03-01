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

import io_handler as io
import constants as cnt   # Hehe, get it?


# Now, do the checking:
try:
  # Check all files in the staging-area:
  text = subprocess.check_output(
    [cnt.git_binary_path, "status", "--porcelain", "-uno"],
    stderr=subprocess.STDOUT
  ).decode("utf-8")
  file_list = text.splitlines()

  # Check all files:
  for file_s in file_list:
    stat = os.stat(file_s[3:])
    if stat.st_size > (max_file_size*1024):
      # File is to big, abort the commit:
      print("'"+file_s[3:]+"' is too huge to be commited!",
        "("+sizeof_fmt(stat.st_size)+")")
      sys.exit(1)
  
  # Everything seams to be okay:
  print("No huge files found.")
  sys.exit(0)

except subprocess.CalledProcessError:
  # There was a problem calling "git status".
  print("Oops...")
sys.exit(12)