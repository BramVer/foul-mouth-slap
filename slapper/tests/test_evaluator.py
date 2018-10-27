'''Tests for the evaluator file.'''
from slapper.evaluator import check_for_violations 

def test_evaluator_clean():
  '''Tests a happy path with no violations in the content.'''

  file_type = 'py'
  content = [
    'this is a line of python code',
    'this is another',
    'Everything oughta be good here',
    'go on with your day kind person',
  ]

  violations = ev.check_for_violations(file_type, content)

  assert len(violations) == 0
