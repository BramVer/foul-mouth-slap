'''Collection of evaluators used throughout the script to check for violations.

Each new constraint/check is added to the process.
'''

import re
from fuzzywuzzy import fuzz

import io_handler as io


def check_foul_words_match(line, foul_words):
  status = []

  for word in line:
    if word in foul_words:
      status.append(io.format_violation_report(word, line))

  return status

def check_foul_words_derivative(line, foul_words):
  status = []

  for fword in foul_words:
    if fuzz.partial_ratio(fword, line) > 90:
      status.append(io.format_violation_report("Derivative of '%s'" % (fword), line))

  return status

def check_foul_patterns(line, foul_patterns, acceptable_patterns):
  status = []

  for foul_pat in foul_patterns:
    regex = re.search(r'' + foul_pat, line, re.I)
    hit = regex.group() if regex else None

    if hit:
      overruled = False

      for accept_pat in acceptable_patterns:
        regex = re.search(r'' + accept_pat, hit, re.I)

        if regex and regex.group():
          overruled = True

      if not overruled:
        status.append(io.format_violation_report("Pattern '%s'" % (foul_pat), line))

  return status

def check_for_violations(type, content):
  violations = []
  foul_words = io.get_foul_words_for_type(type)
  foul_patterns = io.get_foul_patterns_for_type(type)
  acceptable_patterns = io.get_acceptable_patterns_for_type(type)

  for line in content:
    report = check_foul_words_match(line, foul_words)
    if (report != ""):
      violations.extend(report)

    report = check_foul_words_derivative(line, foul_words)
    if (report != ""):
      violations.extend(report)

    report = check_foul_patterns(line, foul_patterns, acceptable_patterns)
    if (report != ""):
      violations.extend(report)

  return violations    