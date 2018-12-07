'''Contains configuration call.

Will return the user set preferences and list of words and patterns from assets.
'''
import re
import os
import sys
import toml


def _get_absolute_path_for_script() -> str:
 '''Returns the absolute path for the script.

 Seeing as the script is called from a pre commit hook,
 the relative path changes with the repository it's in.
 This gets the path from the execution call.
 '''
 absolute_path = os.path.dirname(os.path.abspath(__file__))   # Everything up until the file_name slapper.py

 regex = re.search(r'.*foul-mouth-slap\/', absolute_path, re.MULTILINE | re.I)
 match = regex.group() if regex else absolute_path

 return match


def _get_violations_as_dict() -> dict:
  '''Returns a dict containing all user-defined violations.'''
  violations_dict = {}

  try:
    relative_path = get_config().get('executable', {}).get('path_to_violations_list', '')
    absolute_path = _get_absolute_path_for_script()
    violations_dict = toml.load(os.path.abspath('%s/%s' % (absolute_path, relative_path)))
  except Exception as e:
    print("Something went wrong while loading the violations dictionary.")
    print(e)

  return violations_dict


def _get_type_definition_for_file_type(definition: str, file_type: str) -> list:
  '''Gets definitions approrpriate for file from the predefined violations list.'''
  violations_dict = _get_violations_as_dict()

  all_foul_definition = violations_dict.get('all', {}).get('foul', {}).get(definition, [])
  file_type_foul_definition = violations_dict.get(file_type, {}).get('foul', {}).get(definition, [])
  file_type_acceptable_definition = violations_dict.get(file_type, {}).get('acceptable', {}).get(definition, [])

  merged_definition = all_foul_definition + file_type_foul_definition

  return [mdef for mdef in merged_definition if mdef not in file_type_acceptable_definition]


def get_foul_patterns_for_file_type(file_type: str) -> dict:
  '''Returns all foul patterns appropriate for the fyle type.'''
  return _get_type_definition_for_file_type('patterns', file_type)

def get_foul_words_for_file_type(file_type: str) -> dict:
  '''Returns all foul words appropriate for the fyle type.'''
  return _get_type_definition_for_file_type('words', file_type)

def get_acceptable_patterns_for_file_type(type: str) -> dict:
  '''Returns all acceptable patterns for the fyle type.'''
  violations_dict = _get_violations_as_dict()

  all_acceptable_patterns = violations_dict.get('all', {}).get('acceptable', {}).get('patterns', [])
  type_acceptable_patterns = violations_dict.get(type, {}).get('acceptable', {}).get('patterns', [])

  return [pattern for pattern in all_acceptable_patterns + type_acceptable_patterns]


def get_config() -> dict:
  '''Returns the user preferences.'''
  config_dict = {}

  try:
    relative_path = '/config.toml'
    absolute_path = _get_absolute_path_for_script()
    os.path.abspath('%s/%s' % (absolute_path, relative_path))
    config_dict = toml.load(os.path.abspath('%s/%s' % (absolute_path, relative_path)))
  except Exception as e:
    print("Something went wrong while loading the configuration.")
    print(e)

  return config_dict


def get_foul_word_fuzzy_match_ratio() -> int:
  '''Returns the tolerance of the fuzzy matches for foul words.'''
  return get_config().get('preferences', {}).get('fuzzy_match_ratio', 69)

def get_is_fuzzy_matching_turned_on() -> bool:
  '''Returns a boolean whether fuzzy matching is turned on or off.'''
  return True if get_config().get('preferences', {}).get('fuzzy_matching') else False