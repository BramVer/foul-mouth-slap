#!/usr/bin/python

import sys

import evaluator
import io_handler as io

def main():
  # Dict of status with all new / modified files
  affected_files = io.get_repository_status()
  violations = []

  for filename in affected_files.get('modified', []):
    file_type = io.get_file_type(filename)
    appropriate_content = io.get_modified_file_contents(filename)

    evaluation_status = evaluator.check_for_violations(file_type, appropriate_content)
    if (len(evaluation_status) > 0):
      violations.append("\nFound in file\t%s" % filename)

    violations += evaluation_status

  for filename in affected_files.get('new', []):
    file_type = io.get_file_type(filename)
    content = io.open_file_by_lines(filename)

    evaluation_status = evaluator.check_for_violations(file_type, content)
    if (len(evaluation_status) > 0):
      violations.append("\nFound in file\t%s" % filename)

    violations += evaluation_status


  if len(violations) > 0:
    io.log_final_verdict(violations)

    sys.stdin = open('/dev/tty')
    answer = input('Commit anyway? [N/y] ')

    if answer.strip().lower().startswith('y'):
      print('Continued.')
      sys.exit(0)

    print('Aborting commit.')
    sys.exit(1)

  print('No foul mouthed words found. 👌👌👌👏👏🙌🙌🙌        ')
  sys.exit(0)

if __name__ == '__main__':
  main()
