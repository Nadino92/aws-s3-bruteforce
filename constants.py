#!/usr/bin/env python
base_url = "https://s3.amazonaws.com/"

#Seconds to sleep between attempts
sleep_sec_between_attempts = .10

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
prefixes = [
            "archive-", "archive.", 
            "backup-", "backup.", 
            "bak-", "bak.", 
            "beta-", "beta.", 
            "dev-", "dev.", 
            "internal-", "internal."
           ]
postfixes = [
                "-archive", 
                "-backup", 
                "-bak", 
                "-beta", 
                "-dev", 
                "-internal"
            ]

#Domains to add onto the string  (excluding .gov, .edu, etc as that will be more targeted)
domains = [".com", ".net", ".org"]