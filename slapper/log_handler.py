'''Handles logging feedback to the user.'''
from config_handler import get_config

def _format_final_verdict(violations: list) -> list:
  '''Formats and returns all violations.'''
  output = []
  foul_message = get_config().get('preferences', {}).get('foul_message')

  output.append(foul_message)

  for index, viol in enumerate(violations):
    output.append('%u: %s' % (index, viol.replace("\n", "")))

  return output


def format_violation_report(violation: str, line: str) -> str:
  '''Formats the violation to the appropriate form.'''
  return "%s found in line: \t%s" % (violation, line)

def log_to_user(statement: str):
  '''Prints the statement to console.

  This method exists to allow for an easy transition into
  logfiles or other ways of communicating.
  '''
  print(statement)

def log_final_verdict(violations: list):
  '''Logs final verdict to the user.'''
  final_verdict = _format_final_verdict(violations)

  for verdict in final_verdict:
    log_to_user(verdict)
