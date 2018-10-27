'''Checks for foul words/patterns in staged files during commit.

Executed as a git pre-commit, checks the content of staged files.
'''
import sys

import evaluator
import io_handler as io
import git_handler as git

from sys_handler import halt_and_wait_for_input
from sys_handler import exit_no_violations_found

def main():
  violations = []
  staged_files = git.get_staged_files_per_status()

  for file_status, file_name in staged_files:
    file_type = io.get_file_type(file_name)

    appropriate_content = io.get_file_contents_to_evaluate(file_status, file_name)
    evaluation_status = evaluator.check_for_violations(file_type, appropriate_content)

    if (len(evaluation_status) > 0):
      violations.append("\nFound in file\t%s" % file_name)

    violations += evaluation_status

  if len(violations) > 0:
    halt_and_wait_for_input(violations)

  exit_no_violations_found()

if __name__ == '__main__':
  main()
