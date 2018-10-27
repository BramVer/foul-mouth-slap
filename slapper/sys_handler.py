'''Handles the system calls exiting/continuing/aborting the script.'''

import sys

from log_handler import log_to_user
from log_handler import log_final_verdict
from config_handler import get_config


def _abort():
  '''Aborts the current process and prevents the commit.'''
  log_to_user('Aborting commit.')
  sys.exit(1)

def _exit_gracefully():
  '''Exits the script and continues.'''
  sys.exit(0)


def exit_no_violations_found():
  '''Exits the script and continues the running process it halted.'''
  clean_message = get_config().get('preferences', {}).get('clean_message')
  log_to_user(clean_message)
  _exit_gracefully()

def halt_and_wait_for_input(violations: list):
  '''Halts the current process and delegates based on user input.'''
  log_final_verdict(violations)

  sys.stdin = open('/dev/tty')
  answer = input('Commit anyway? [N/y] ')

  if answer.strip().lower().startswith('y'):
    log_to_user('Continued.')
    _exit_gracefully()

  _abort()
