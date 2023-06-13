'''Utilities for interacting with Bazel'''

import os
import typing

import shell_util as su


def output_base(cwd: typing.Optional[str] = None) -> str:
  '''Get Bazel output base for directory

  Args:
    cwd: Directory within Bazel workspace.  Defaults to current directory

  Returns:
    The output base path.
  '''
  return su.string_cmd(['bazel', 'info', 'output_base'], cwd)


def workspace(cwd: typing.Optional[str] = None) -> str:
  '''Get Bazel workspace root directory

  Args:
    cwd: Directory within Bazel workspace.  Defaults to current directory

  Returns:
    The workspace root directory.
  '''
  return su.string_cmd(['bazel', 'info', 'workspace'], cwd)


def workspace_file(cwd: typing.Optional[str] = None) -> str:
  '''Get Bazel workspace file

  Args:
    cwd: Directory within Bazel workspace.  Defaults to current directory

  Returns:
    The workspace file path.
  '''
  file = 'WORKSPACE'

  w = workspace(cwd)
  for f in os.listdir(w):
    if f in ['WORKSPACE', 'WORKSPACE.bazel']:
      file = f
      break

  return os.path.join(w, file)


def root_build_file(cwd: typing.Optional[str] = None) -> str:
  '''Get Bazel workspace file

  Args:
    cwd: Directory within Bazel workspace.  Defaults to current directory

  Returns:
    The workspace file path.
  '''
  file = 'BUILD'

  w = workspace(cwd)
  for f in os.listdir(w):
    if f in ['BUILD', 'BUILD.bazel']:
      file = f
      break

  return os.path.join(w, file)
