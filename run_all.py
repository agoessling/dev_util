'''Run all compile steps.'''
import argparse
import os
import sys

import gen_compile_commands
import gen_pyright_config


def main():
  '''Run all lsp compile steps.'''
  parser = argparse.ArgumentParser(description='Run all LSP config generation.')
  parser.add_argument('--dir', help='Working directory from which to run generation.')

  args = parser.parse_args()

  if args.dir is not None:
    os.chdir(args.dir)

  # Reset arguments.
  sys.argv = sys.argv[:1]

  gen_compile_commands.main()
  gen_pyright_config.main()


if __name__ == '__main__':
  main()
