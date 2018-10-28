import pytest
import slapper.io_handler as io

@pytest.fixture
def get_empty_test_file():
  '''File exists and contains 5 lines.'''
  return 'tests/empty_file_for_test_purpose.txt'

def test__open_file_by_lines(get_empty_test_file):
  # Happy path returns lines in file (5)
  file_name = get_empty_test_file

  test = io._open_file_by_lines(file_name)
  assert type(test) == list
  assert len(test) == 5

  # File not found should not crash everything
  file_name = 'bleepbloopblurp.textfile'

  test = io._open_file_by_lines(file_name)
  assert type(test) == list
  assert len(test) == 0


def test_get_file_type():
  # Happy path with file extension
  file_name = 'file.txt'

  test = io.get_file_type(file_name)
  assert test == 'txt'

  # Happy path with no file extension
  file_name = 'file'

  test = io.get_file_type(file_name)
  assert test == 'file'

  # Sad path with nothing after last dot
  file_name = 'file.'

  test = io.get_file_type(file_name)
  assert test == 'file.'


def test__get_file_contents(get_empty_test_file):
  # Happy path with file_name to open without locations
  file_name = get_empty_test_file
  locations = []

  test = io._get_file_contents(file_name, locations)
  assert type(test) == list
  assert len(test) == 5

  # Happy path with file_name and locations
  file_name = get_empty_test_file
  locations = [
    {
      'start': 0,
      'end': 2,
    }
  ]

  test = io._get_file_contents(file_name, locations)
  assert len(test) == 2

def test_get_file_contents_to_evaluate(get_empty_test_file):

  # Happy path with renamed status
  file_status = 'renamed'
  file_name = get_empty_test_file

  test = io.get_file_contents_to_evaluate(file_status, file_name)
  assert type(test) == list
  assert len(test) == 0

  # Happy path with deleted status
  file_status = 'deleted'
  file_name = get_empty_test_file

  test = io.get_file_contents_to_evaluate(file_status, file_name)
  assert len(test) == 0

  # @NOTE: Don't know how to fully mock git diffs yet
  # New or Modified files will not get opened, nothing will crash
  # Happy path with new/modified status
  file_status = 'new'
  file_name = 'NON_EXISTING_FILE'

  test = io.get_file_contents_to_evaluate(file_status, file_name)
  assert len(test) == 0

  file_status = 'modified'
  file_name = 'NON_EXISTING_FILE'

  test = io.get_file_contents_to_evaluate(file_status, file_name)
  assert len(test) == 0