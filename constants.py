#!/usr/bin/env python
base_url = "https://s3.amazonaws.com/"

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
prefixes_postfixes = [
                "archive", 
                "backup", 
                "bak", 
                "beta", 
                "bitcoin", 
                # "cdn",
                # "certs", 
                # "confidential", 
                # "deployment", 
                # "dev", 
                # "download", 
                "files", 
                # "fiannces", 
                # "financial", 
                # "internal",
                # "key",
                # "keys",
                # "operations",
                # "ops",
                # "password",
                # "passwords",
                # "software",
                # "ssl",
                # "tls",
                "wallet",
           ]

#Domains to add onto the string  (excluding .gov, .edu, etc as that will be more targeted)
#This is removed for right now because it saw few positive results
# domains = [".com", ".net", ".org"]
domains = []
