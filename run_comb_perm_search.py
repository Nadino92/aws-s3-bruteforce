#!/usr/bin/env python
import itertools
import random, time
from progressbar import ProgressBar
from constants import *
from check_bucket import *
from logger import *

def run_comb_perm_search(search):
    #Create progressbar to show how many searches have been done, removing eta
    progressbar = ProgressBar(total_items=get_num_comb_perm(num_chars=search.num_chars, string_options=search.string_options))
    progressbar.fmt = '''%(percent)3d%% %(bar)s %(current)s/%(total_items)s   %(items_per_sec)s   ETA: %(eta)s'''

    #Get all public butets that have been found so far
    buckets_found = get_buckets_found(search.output_file)

    #Run the search across all combinations/permutations
    for item in itertools.product(search.string_options, repeat=search.num_chars):
        bucket_name = "".join(item)

        #Just in case the bucket has been found, don't try again.
        #Not storing all to prevent massive memory usage.
        if bucket_name not in buckets_found:
            bucket_response = check_s3_bucket(bucket_name)
            if bucket_response["exists"] == True:
                buckets_found.append(bucket_name)
                log_bucket_found(bucket_response=bucket_response, output_file=search.output_file)

            #Increment progress and sleep                
            progressbar()
            if search.print_bucket_names:
                print bucket_name
            time.sleep(sleep_sec_between_attempts)


def get_num_comb_perm(num_chars, string_options):
    """Gets the number of combintions/permutations for the given string and number of chars"""
    num_comb_perm = 0
    for item in itertools.product(string_options, repeat=num_chars):
        num_comb_perm += 1
    return num_comb_perm


