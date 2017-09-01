#!/usr/bin/env python
import os, ast
cur_dir = os.path.dirname(os.path.realpath(__file__))


def get_buckets_found(output_file):
    """Return a list of comb/perm public buckets that have been found"""
    bucket_names = []
    try:
        if not output_file:
            output_file = "buckets_found.txt"
        with open("buckets_found.txt", 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        bucket_names.append(ast.literal_eval(line.strip())["name"])
                    except:
                        pass
        return bucket_names
    except:
        return bucket_names


def log_bucket_found(bucket_response, output_file):
    if not output_file:
        output_file = "buckets_found.txt"

    """Writes potentially open buckets to a file"""
    f = open(output_file, "a")
    f.write("{bucket_response}\n".format(bucket_response=str(bucket_response)))
    f.close()
