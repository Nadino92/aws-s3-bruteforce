#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################
## Purpose: Provies argument parsing capability
###############################################
import argparse

#Documentation
parser = argparse.ArgumentParser(description='''This is a example of how to user argparse.  Nothing fancy.''')

#Arguments
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
                    '-l',
                    '--list',
                    help='List file to use',
                   )
group.add_argument(
                    '-s',
                    '--string',
                    help='String to scan',
                   )
group.add_argument(
                    '-r',
                    '--random_string_options',
                    help='Chars to create random strings from, until script is stopped'
                   )

parser.add_argument(
                    '-a', 
                    '--start_after_value',
                    required=False, 
                    help='Start after this string in the file',
                   )

parser.add_argument(
                    '-n', 
                    '--start_after_line_num',
                    type=int, 
                    required=False, 
                    help='Start after this line num in the file',
                   )

parser.add_argument(
                    '-t', 
                    '--threads',
                    required=True, 
                    type=int, 
                    help='Number of Threads',
                   )

parser.add_argument(
                    '-p', 
                    '--print_bucket_names',
                    action='store_true',
                    help='Print bucket names as they are attempted',
                   )

parser.add_argument(
                    '-c', 
                    '--chars',
                    required=False, 
                    help='Range of chars for the random string, e.g. 3-12',
                  )

args = parser.parse_args()
