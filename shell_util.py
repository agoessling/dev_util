'''Shell utilities'''

import subprocess
import typing


def string_cmd(args: list[str], cwd: typing.Optional[str] = None) -> str:
  '''Execute command returning a string

  Args:
    args: Arguments of command
    cwd: Directory from which to execute command.  Defaults to current directory.

  Returns:
    The stdout output.
  '''
  ret = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)
  return ret.stdout.strip()
