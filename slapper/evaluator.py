'''Collection of evaluators used throughout the script to check for violations.

Each new constraint/check is added to the process.
'''

import re
from fuzzywuzzy import fuzz
from log_handler import format_violation_report

import config_handler as conf


def _check_foul_words_match(line: str, foul_words: list) -> list:
  '''Checks if the content contains one of the foul words.'''
  status = []

  for fword in foul_words:
    if fword in line:
      status.append(format_violation_report(fword, line))

  return status

def _check_foul_words_derivative(line: str, foul_words: list) -> list:
  '''Checks if the content contains a  derivative of one of the foul words.

  This checks for a certainty percentages using the Levenshtein algorithm.
  '''
  status = []
  foul_word_tolerance = conf.get_foul_word_fuzzy_match_ratio()

  for fword in foul_words:
    if fuzz.partial_ratio(fword, line) >= foul_word_tolerance:
      status.append(format_violation_report("Potential derivative of '%s'" % (fword), line))

  return status

def _does_regex_match_anything(regex: str, line: str) -> bool:
  '''Checks if a regex pattern matches anything in the provided line.'''
  is_match = False
  result = re.search(r'' + regex, line, re.I)

  if result and result.group():
    is_match = True

  return is_match

def _is_foul_match_overruled(line :str, acceptable_patterns: list) -> bool:
  '''Checks if the match can be overruled by iterating over available acceptable patterns.'''
  return True in [_does_regex_match_anything(pattern, line) for pattern in acceptable_patterns]

def _check_foul_patterns(line: str, foul_patterns: list, acceptable_patterns: list) -> list:
  '''Checks if a word in the line contains one of the foul patterns.

  When a foul pattern is matched, the list of acceptable patterns
  can overrule a match as a violation.

  Performance and accuracy note:
  It would be much better to run the regexes on the entire line,
  but that would mean the violations could not be overruled
  due to missing context in matches.
  '''
  status = []

  for word in line.split():
    for foul_pat in foul_patterns:
      regex = re.search(r'' + foul_pat, word, re.I)
      hit = regex.group() if regex else None

      if hit and not _is_foul_match_overruled(word, acceptable_patterns):
        status.append(format_violation_report("Pattern '%s'" % (foul_pat), word))

  return status


def check_for_violations(type: str, content: list) -> list:
  """Loops content and checks for predetermined violations.
  
  Iterates the content by line and return an array.
  Each entry in the array will contain a string describing a specific violation.
  """
  violations = []
  is_fuzzy_matching_turned_on = conf.get_is_fuzzy_matching_turned_on()

  foul_words = conf.get_foul_words_for_file_type(type)
  foul_patterns = conf.get_foul_patterns_for_file_type(type)
  acceptable_patterns = conf.get_acceptable_patterns_for_file_type(type)

  for line in content:
    violations.extend(_check_foul_words_match(line, foul_words))
    violations.extend(_check_foul_patterns(line, foul_patterns, acceptable_patterns))

    if is_fuzzy_matching_turned_on:
      violations.extend(_check_foul_words_derivative(line, foul_words))

  return violations    