#!/usr/bin/env python

"""
no idea what like half of this code is
stole most of it, credit given where due
"""

import os
import glob
import re
import sys
import traceback

def main():
  if len(sys.argv) < 2:
    help()

  paths = []
  for path in sys.argv[1:]:
    paths.append(os.path.realpath(os.path.join(os.getcwd(), path)))

  file_regex = r'.*\.(((s?|p?)(c|a)|le)ss|styl)' # lovely regex
  files = []
  for path in paths:
    if os.path.isdir(path):
      for file in glob.glob(path + '/**/*', recursive=True):
        if re.match(file_regex, file):
          files.append(file)

    elif re.match(file_regex, path):
      files.append(path)

    else:
      help()

  #* Credits: https://github.com/j-f1/DiscordClassChanges/blob/add-update/update.py
  replacements = {}
  differences_path = os.path.join(os.path.dirname(os.path.realpath((__file__))), '../DiscordClassChanges/differences.csv')
  with open(differences_path, mode='r') as f:
    for line in f.readlines():
      classes = line[:-1].split(',')
      for old in classes[:-1]:
        replacements[old] = classes[-1]

  for name in files:
    try:
      with open(name, mode='r') as f:
        content = f.read()

      for old, new in replacements.items():
        content = content.replace(old, new)

      with open(name, mode='w') as f:
        f.write(content)

      print('Successfully updated ' + name + '!')

    except Exception:
      print('Error handling file ' + name + ':')
      traceback.print_exc()

def help():
  print('USAGE:')
  print('  python update-classes.py theme.css')
  print('  python update-classes.py theme1.css theme2.css theme3.css ...')
  print('  python update-classes.py *.css')
  exit(1)

if __name__ == '__main__':
  main()
