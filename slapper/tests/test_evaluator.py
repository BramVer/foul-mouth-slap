'''Tests for the evaluator file.'''
import pytest
import slapper.evaluator as ev


@pytest.fixture
def get_foul_words():
  foul_words = ['bythone', 'poop', 'dink']
  return foul_words

@pytest.fixture
def get_foul_patterns():
  foul_patterns = ['([a-z])\\1{3,}']
  return foul_patterns

@pytest.fixture
def get_acceptable_patterns():
  acceptable_patterns = ['#[a-zA-Z0-9]*']
  return acceptable_patterns

def test__check_foul_words_match(get_foul_words):
  # Happy path with 0 violations
  line = 'This is a happy path with no violations.'

  test = ev._check_foul_words_match(line, get_foul_words)
  assert len(test) == 0

  # Happy path with 2 violations
  line = 'This is a happy path with 2 bythone violations poop.'

  test = ev._check_foul_words_match(line, get_foul_words)
  assert len(test) == 2


def test__check_foul_words_derivative(get_foul_words):
  # Happy path with 0 violations
  line = 'This is a happy path with no violations.'

  test = ev._check_foul_words_derivative(line, get_foul_words)
  assert len(test) == 0

  # Happy with 3 'possible' but 1 actual violations
  line = 'I drink dinnk that stuffdink which I like yes'

  test = ev._check_foul_words_derivative(line, get_foul_words)
  assert len(test) == 1


def test__check_foul_patterns(get_foul_patterns, get_acceptable_patterns):
  # Happy path with 0 violations
  line = 'This is a happy path with no violations.'

  test = ev._check_foul_patterns(line, get_foul_patterns, get_acceptable_patterns)
  assert len(test) == 0

  # Happy path with 2 violations
  line = 'This iiiiiiis a haaaaappy path with a couple of violations'

  test = ev._check_foul_patterns(line, get_foul_patterns, get_acceptable_patterns)
  assert len(test) == 2

  # Happy path with an overrule
  line = 'This iiiiiiis a haaaaappy path with a couple of violations getting overruled'

  test = ev._check_foul_patterns(line, get_foul_patterns, get_foul_patterns)
  assert len(test) == 0

  # Happy path with an exception overrule in a violation
  line = 'This is a #haaaaappy path with a couple of violations getting overruled'

  test = ev._check_foul_patterns(line, get_foul_patterns, get_acceptable_patterns)
  assert len(test) == 0

