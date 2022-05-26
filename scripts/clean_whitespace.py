#!/usr/bin/env python3
#
# This script takes a list of files as command-line arguments, and modifies
# them to fix some common whitespace issues. 
# Specifically, it does these things:
#
#  1. Converts the line endings to UNIX-style line endings
#  2. Removes all trailing whitespace
#  3. Converts tabs into 8 space characters
#  4. Adds a trailing newline to the file if one is missing
import os
import sys

tabsize = 8

if len(sys.argv) <= 1:
    sys.exit('Error: Please supply a list of filenames')

print('Cleaning up whitespace:')
for filename in sys.argv[1:]:
    temp_filename = filename + '.new'
    with open(filename) as r:
        assert not os.path.exists(temp_filename)
        with open(temp_filename, 'w', newline='\n') as w:
            for line in r:
                w.write(line.replace('\t', ' ' * tabsize).rstrip() + '\n')
    os.rename(temp_filename, filename)
    print(f'  {filename}: done')
