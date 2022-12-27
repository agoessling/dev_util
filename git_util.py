'''Utilities for interacting with Git'''

import os
import subprocess
import typing

import shell_util as su


def root_dir(cwd: typing.Optional[str] = None) -> str:
  '''Get Git repository root directory

  Args:
    cwd: Directory within Git repository.  Defaults to current directory

  Returns:
    The repository root directory path.
  '''
  return su.string_cmd(['git', 'rev-parse', '--show-toplevel'], cwd)


def git_dir(cwd: typing.Optional[str] = None) -> str:
  '''Get .git directory

  Args:
    cwd: Directory within Git repository.  Defaults to current directory

  Returns:
    The path to .git directory.
  '''
  return su.string_cmd(['git', 'rev-parse', '--absolute-git-dir'], cwd)


def exclude_file(cwd: typing.Optional[str] = None) -> str:
  '''Get Git exclude file

  Args:
    cwd: Directory within Git repository.  Defaults to current directory

  Returns:
    The path to the exclude file.
  '''
  return os.path.join(git_dir(cwd), 'info/exclude')


def ignore_file(cwd: typing.Optional[str] = None) -> str:
  '''Get root .gitignore file

  Args:
    cwd: Directory within Git repository.  Defaults to current directory

  Returns:
    The path to the root .gitignore file.
  '''
  return os.path.join(root_dir(cwd), '.gitignore')


def add_to_exclude_file(pattern: str, cwd: typing.Optional[str] = None):
  '''Add pattern to Git exclude file.

  Args:
    pattern: Pattern to add to the exclude file.
    cwd: Directory within Git repository.  Defaults to current directory
  '''
  exclude = exclude_file(cwd)

  try:
    # Only write pattern if not already present.
    subprocess.run(['grep', '-q', pattern, exclude], check=True)
  except subprocess.CalledProcessError as e:
    if e.returncode != 1:
      raise e

    with open(exclude, 'a') as f:
      f.write(f'{pattern}\n')
