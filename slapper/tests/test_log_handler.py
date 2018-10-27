from slapper.log_handler import format_violation_report

def test_format_violation_report():
  violation = 'Ran a red light'
  line = 'When I had to pee real bad oof oof'

  assert format_violation_report(violation, line) == "%s found in line: \t%s" % (violation, line)
