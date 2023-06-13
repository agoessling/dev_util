'''dev_util helper functions.'''
import json
import os
import typing

import git_util


def find_config(cwd: typing.Optional[str] = None) -> typing.Optional[dict]:
  '''Try to find a configuration file

  Args:
    cwd: Working directory from which to start search.

  Returns:
    The path to a configuration file or None.
  '''
  config_name = 'dev_util.json'

  if cwd is None:
    cwd = os.getcwd()

  config_path = os.path.join(cwd, config_name)
  if os.path.isfile(config_path):
    with open(config_path, 'r') as f:
      return json.load(f)

  config_path = os.path.join(git_util.root_dir(cwd), config_name)
  if os.path.isfile(config_path):
    with open(config_path, 'r') as f:
      return json.load(f)

  return None
