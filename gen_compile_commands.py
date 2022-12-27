'''Generate compile_commands.json'''

import argparse
import contextlib
import json
import shutil
import subprocess
import typing

import bazel_util
import git_util


def get_workspace_dep() -> str:
  '''Get necessary workspace deps'''
  return '''
http_archive(
    name = "hedron_compile_commands",
    url = "https://github.com/hedronvision/bazel-compile-commands-extractor/archive/83795f870b4c48e95a3427cabff20170be551e72.tar.gz",
    strip_prefix = "bazel-compile-commands-extractor-83795f870b4c48e95a3427cabff20170be551e72",
    sha256 = "509c53598dc673481e1b111cd4523f983393e14e0b17424ef894356e21d64ec6",
)

load("@hedron_compile_commands//:workspace_setup.bzl", "hedron_compile_commands_setup")
hedron_compile_commands_setup()
'''


def get_build_target(targets: typing.Optional[dict[str, str]] = None) -> str:
  '''Get necessary build targets'''
  if targets is None:
    targets = {'//...': ''}

  target_str = ',\n'.join([f'        "{k}": "{v}"' for k, v in targets.items()])

  return f'''
load("@hedron_compile_commands//:refresh_compile_commands.bzl", "refresh_compile_commands")

refresh_compile_commands(
    name = "refresh_compile_commands",
    targets = {{
{target_str}
    }},
)
'''


@contextlib.contextmanager
def temp_append_to_file(file: str, text: str):
  '''Context manager for temporarily appending to file

  File is backed up on __enter__() and restored on __exit__()

  Args:
    file: Path of file to which to append
    text: Text to append
  '''
  backup = f'{file}.bak'
  shutil.copy(file, backup)
  with open(file, 'a') as f:
    f.write(text)
  try:
    yield file
  finally:
    shutil.move(backup, file)


def main():
  '''Main'''
  parser = argparse.ArgumentParser(description='Create compile_commands.json from Bazel project.')
  parser.add_argument('--dir', help='Path to directory in Bazel project of interest.')
  parser.add_argument('--targets',
                      help='Targets dictionary consisting of Bazel target: compile flags')
  parser.add_argument('--no_ignore', action='store_true',
                      help='Do not add generated files to project\'s Git exclude.')

  args = parser.parse_args()

  targets = None
  if not args.targets is None:
    targets = json.loads(args.targets)

  with temp_append_to_file(bazel_util.workspace_file(args.dir), get_workspace_dep()), \
       temp_append_to_file(bazel_util.root_build_file(args.dir), get_build_target(targets)), \
       temp_append_to_file(git_util.ignore_file(args.dir), ''):
    subprocess.run(['bazel', 'run', ':refresh_compile_commands'], cwd=args.dir, check=True)

  if not args.no_ignore:
    git_util.add_to_exclude_file('compile_commands.json')
    git_util.add_to_exclude_file('external')
    git_util.add_to_exclude_file('.cache')


if __name__ == '__main__':
  main()
