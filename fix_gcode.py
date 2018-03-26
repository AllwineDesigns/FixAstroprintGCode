#!/usr/bin/python

import os
import time
import sys

checked_files = set([])
files_to_update = set([])

firstNLines = 3

while True:
  all_files = set([ f for f in os.listdir('/AstroBoxFiles/uploads/') if f.endswith('gcode') ])
  deleted_files = checked_files-all_files
#  if deleted_files:
#    print 'Deleted ', deleted_files
  checked_files = checked_files-deleted_files

  new_files = all_files-checked_files

#  print 'new files', new_files

  for f in new_files:
    try:
      with open('/AstroBoxFiles/uploads/%s' % f, 'r') as fileObj:
        for i in range(firstNLines):
          line = fileObj.readline()
          if line.startswith('M100.1') and '?' in line:
            print 'need to update %s' % f
            files_to_update.add(f)
      checked_files.add(f)
    except:
      print 'Error reading %s' % f, sys.exc_info()[0]

#  print 'files to update', files_to_update

  while files_to_update:
    f = files_to_update.pop()
    try:
      with open('/AstroBoxFiles/uploads/%s' % f, 'r') as fileObj:
        lines = fileObj.readlines()
        for i in range(firstNLines):
          if lines[i].startswith('M100.1') and '?' in lines[i]:
            lines[i] = lines[i].replace('?', '')
      with open('/AstroBoxFiles/uploads/%s' % f, 'w') as fileObj:
        for line in lines:
          fileObj.write(line)
        print 'Removed question marks from %s' % f
    except:
      print 'Error fixing %s' % f, sys.exc_info()[0]
      files_to_update.add(f)
  time.sleep(1)
