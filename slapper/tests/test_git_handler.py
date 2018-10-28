import pytest
import slapper.git_handler as git

@pytest.fixture
def get_git_clean_staged_files():
  # Mocks a `git diff --name-status --cached` command
  return "A slapper/dink.py\nD slapper/wat.py\nM slapper/dinkdnok.pyc"

@pytest.fixture
def get_git_dirty_staged_files():
  # Mocks a `git diff --name-status --cached` command
  return "A slapper/dink.py\nD slapper/wat.py\n      "


def test__categorize_staged_files(get_git_clean_staged_files, get_git_dirty_staged_files):
  # Happy path mocking an examplary output
  input = get_git_clean_staged_files

  test = git._categorize_staged_files(input)
  assert type(test) == list
  assert len(test) == 3

  for staged_file in test:
    assert type(staged_file) == tuple

  assert test[0] == ('new', 'slapper/dink.py')
  assert test[1] == ('deleted', 'slapper/wat.py')
  assert test[2] == ('modified', 'slapper/dinkdnok.pyc')

def test__check_if_valid_staged_files_output():
  # Happy path complying to the expected formatting
  staged_files_output = 'A slapper/dink.py'

  test = git._check_if_valid_staged_files_output(staged_files_output)
  assert type(test) == bool
  assert test == True

  # Happy path catching improper formatting
  staged_files_output = 'DasdasdfasdfD sadfslapper/dink.py'

  test = git._check_if_valid_staged_files_output(staged_files_output)
  assert test == False

