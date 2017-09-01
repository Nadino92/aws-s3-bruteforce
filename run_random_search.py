#!/usr/bin/env python
import random, time
from progressbar import ProgressBar
from constants import *
from check_bucket import *
from logger import *


def run_random_search(search):
    #Create progressbar to show how many searches have been done, removing eta
    progressbar = ProgressBar(1)
    progressbar.fmt = '''%(percent)3d%% %(bar)s %(current)s/%(total_items)s   %(items_per_sec)s   Run time: %(run_time)s'''

    buckets_found = get_buckets_found(search.output_file)

    while True:
        #Create random bucket name
        if search.num_chars:
            bucket_name = ''.join(random.choice(search.string_options) for i in range(search.num_chars))
        elif search.num_chars_range:
            lower_bound, upper_bound = search.num_chars_range.split("-")
            lower_bound = int(lower_bound.strip())
            upper_bound = int(upper_bound.strip())
            bucket_name = ''.join(random.choice(search.string_options) for i in range(random.randint(lower_bound, upper_bound)))

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
            progressbar.total_items += 1
            time.sleep(sleep_sec_between_attempts)