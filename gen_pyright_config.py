'''Generate pyrightconfig.json'''

import argparse
import json
import os
import re
import subprocess
import tempfile

import bazel_util
import git_util


def get_cquery():
  '''Get cquery for python deps'''
  return '''\
def format(target):
    if "PyInfo" not in providers(target):
        return []
    dep = providers(target)["PyInfo"].imports
    return dep.to_list()
'''


def main():
  '''Main'''
  parser = argparse.ArgumentParser(description='Create pyright config from bazel dependencies.')
  parser.add_argument('--targets', nargs='+', default=['//...'],
                      help='Bazel targets whose dependencies should be added.')
  parser.add_argument('--no_ignore', action='store_true',
                      help='Do not add pyrightconfig.json to project\'s Git exclude.')

  args = parser.parse_args()

  output_base = bazel_util.output_base()

  with tempfile.NamedTemporaryFile() as f:
    f.write(get_cquery().encode())
    f.flush()

    deps = set()
    for target in args.targets:
      bazel_cmd = ['bazel', 'cquery', target, '--output', 'starlark', '--starlark:file', f.name]
      ret = subprocess.run(bazel_cmd, capture_output=True, check=True)

      matches = re.findall(r'"(\S+)"', ret.stdout.decode())
      deps.update(matches)

  extra_paths = [os.path.join(output_base, 'external', x) for x in deps]

  # Add bazel-bin directory to capture generated python files.
  ret = subprocess.run(['bazel', 'info', 'bazel-bin'], capture_output=True, check=True)
  extra_paths.append(ret.stdout.decode().strip())

  output = {
      'exclude': ['bazel-*/'],
      'extraPaths': extra_paths,
  }

  workspace = bazel_util.workspace()
  config_path = os.path.join(workspace, 'pyrightconfig.json')

  with open(config_path, 'w') as f:
    json.dump(output, f)

  if not args.no_ignore:
    git_util.add_to_exclude_file('pyrightconfig.json')


if __name__ == '__main__':
  main()
