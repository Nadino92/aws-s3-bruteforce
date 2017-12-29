#!/usr/bin/env python
base_url = "https://s3.amazonaws.com/"
prefixes_postfixes_file = "./prefixes_postfixes.txt"

#Seconds to sleep between attempts
sleep_sec_between_attempts = .05

#Company entity endings to check for and add to list, with them removed
entities = [
                " Inc", " Incorporated", 
                " Co", "Company", 
                " Corp", " Corporation"
                " LLC",
                " Ltd", "Limited",
           ]

#Things to replace spaces with
space_replacements = ["", "-", "_"]

#Prefixes and postfixes to add to the strings
prefix_postfix_separators = ["", ".", "-", "_"]
# Loaded from the file specified in prefixes_postfixes_file
prefixes_postfixes = []
with open(prefixes_postfixes_file) as f:
    prefixes_postfixes = [line.rstrip('\n') for line in f]

#Domains to add onto the string  (excluding .gov, .edu, etc as that will be more targeted)
#This is removed for right now because it saw few positive results
# domains = [".com", ".net", ".org"]
domains = []
