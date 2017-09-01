#!/usr/bin/env python
import itertools
import random, time
from progressbar import ProgressBar
from constants import *
from check_s3_bucket import *


def run_comb_perm_search(num_chars, string_options, print_bucket_names):
    num_comb_perm = get_num_comb_perm(num_chars, string_options)

    #Create progressbar to show how many searches have been done, removing eta
    progressbar = ProgressBar(num_comb_perm)
    progressbar.fmt = '''%(percent)3d%% %(bar)s %(current)s/%(total_items)s   %(items_per_sec)s   %(run_time)s'''

    buckets_found = get_comb_perm_buckets_found()

    for item in itertools.product(string_options, repeat=num_chars):
        bucket_name = "".join(item)

        #Just in case the bucket has been found, don't try again.
        #Not storing all to prevent massive memory usage.
        if bucket_name not in buckets_found:
            url = "{base_url}{bucket_name}".format(base_url=base_url, bucket_name=bucket_name)
            if check_s3_bucket(url):
                buckets_found.append(bucket_name)
                log_bucket_found(bucket_name)

            #Increment progress and sleep                
            progressbar()
            if print_bucket_names:
                print bucket_name
            progressbar.total_items += 1
            time.sleep(sleep_sec_between_attempts)


def get_comb_perm_buckets_found():
    bucket_names = []
    with open("found/comb_perm_found.txt", 'r') as f:
        for line in f:
            if line.strip():
                bucket_names.append(line.strip())
    return bucket_names


def log_bucket_found(bucket_name):
    """Writes potentially open buckets to a file"""
    f = open("found/comb_perm_found.txt", "a")
    f.write("{bucket_name}\n".format(bucket_name=bucket_name))
    f.close()


def get_num_comb_perm(num_chars, string_options):
    num_comb_perm = 0
    for item in itertools.product(string_options, repeat=num_chars):
        num_comb_perm += 1
    return num_comb_perm
