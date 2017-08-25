#!/usr/bin/env python
import random, time
from progressbar import ProgressBar
from constants import *
from find_public_s3_buckets import try_random_link


def run_random_search(lower_bound, upper_bound, random_string_options):
    #Create progressbar to show how many searches have been done, removing eta
    progressbar = ProgressBar(1)
    progressbar.fmt = '''%(percent)3d%% %(bar)s %(current)s/%(total_items)s   %(items_per_sec)s   %(run_time)s'''

    buckets_found = get_random_buckets_found()

    while True:
        bucket_name = create_random_string(
                                            length=random.randint(lower_bound, upper_bound), 
                                            string_options=random_string_options
                                            )
        #Just in case the bucket has been found, don't try again.
        #Not storing all to prevent massive memory usage.
        if bucket_name not in buckets_found:
            url = "{base_url}{bucket_name}".format(base_url=base_url, bucket_name=bucket_name)
            if try_random_link(url):
                buckets_found.append(bucket_name)
                log_random_found(bucket_name)

            #Increment progress and sleep                
            progressbar()
            progressbar.total_items += 1
            time.sleep(sleep_sec_between_attempts)


def get_random_buckets_found():
    bucket_names = []
    with open("found/random_found.txt", 'r') as f:
        for line in f:
            if line.strip():
                bucket_names.append(line.strip())
    return bucket_names


def log_random_found(bucket_name):
    """Writes potentially open buckets to a file"""
    f = open("found/random_found.txt", "a")
    f.write("{bucket_name}\n".format(bucket_name=bucket_name))
    f.close()


def create_random_string(length, string_options):
    """Create a random string of the given length, with the given set of characters"""
    return ''.join(random.choice(string_options) for i in range(length))