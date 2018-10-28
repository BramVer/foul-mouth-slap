import slapper.log_handler as log

def test_format_violation_report():
  violation = 'Ran a red light'
  line = 'When I had to pee real bad oof oof'

  test = log.format_violation_report(violation, line)
  result = 'Ran a red light found in line: \tWhen I had to pee real bad oof oof'

  assert test == result

def test__format_final_verdict():
  violations = ['One bad violation', '2 even worse thing tsktsk']

  # Happy path
  test = log._format_final_verdict(violations)
  assert len(test) == 3

  # Sad path
  violations = []

  test = log._format_final_verdict(violations)
  assert len(test) == 0