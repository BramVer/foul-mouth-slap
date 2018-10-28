'''Handles file I/O in the application.

All file input and/or output in the application is defined and handled here.
'''
import re

from log_handler import log_to_user

import git_handler as git
import config_handler as conf


def _open_file_by_lines(file_path: str) -> list:
  file_data = []

  try:
    with open(file_path, 'r') as data:
      file_data = [line for line in data]

  except IOError as e:
    log_to_user('Something went wrong trying to open the file %s' % file_path)
    log_to_user(e)

  finally:
    return file_data

def get_file_type(file_name: str) -> str:
  '''Determines the file type of the file.

  Executes a regex searching for everything after the last dot.
  If no match was found, the entire file_name is returned.
  If a match was found, but the .group() is empty (=> 'file.'),
  the original file_name is returned.
  '''
  regex = re.search(r'([^.]*$)', file_name, re.I)
  match = regex.group() if regex else file_name

  file_type = match or file_name
  return file_type

def _get_file_contents(file_name: str, locations: list) -> list:
  '''Opens file and returns the lines at the locations.

  If locations is an empty list, it will return all content.
  '''
  output = []
  content = _open_file_by_lines(file_name)

  if len(locations) == 0:
    output = content

  for location in locations:
    start = location.get('start')
    end = location.get('end')

    output.extend(content[start:end])

  return output  

def get_file_contents_to_evaluate(file_status: str, file_name: str) -> list:
  appropriate_content = []
  status_dict = git.get_status_dict()

  if file_status in [status_dict.get('R'), status_dict.get('D')]:
    # Renamed or deleted files don't need to be opened.
    return appropriate_content

  locations_of_change_in_file = git.get_changed_locations_in_file(
    file_name
  )
  appropriate_content = _get_file_contents(
    file_name, locations_of_change_in_file
  )

  return appropriate_content
