#!/usr/bin/env python
import threading
import Queue
import random, time
from progressbar import ProgressBar
from constants import *
from check_bucket import *
from logger import *

def createStringGenerator(search):
    while True:
        if search.num_chars:
            yield ''.join(random.choice(search.string_options) for i in range(search.num_chars))
        elif search.num_chars_range:
            lower_bound, upper_bound = search.num_chars_range.split("-")
            lower_bound = int(lower_bound.strip())
            upper_bound = int(upper_bound.strip())
            yield ''.join(random.choice(search.string_options) for i in range(random.randint(lower_bound, upper_bound)))


def run_random_search(search):
    #Create progressbar to show how many searches have been done, removing eta
    search.progressbar = ProgressBar(1)
    search.progressbar.fmt = '''%(percent)3d%% %(bar)s %(current)s/%(total_items)s   %(items_per_sec)s   Run time: %(run_time)s'''

    buckets_found = get_buckets_found(search.output_file)


    #Get all public butets that have been found so far
    search.buckets_found = get_buckets_found(search.output_file)
    #Create a string generator
    search.string_generator = createStringGenerator(search)

    my_queue = Queue.Queue()
    for i in range(search.threads+1):
        t = threading.Thread(target=search_instance, args=(search, ))
        my_queue.put(t)

    #Run all of the threads
    while not my_queue.empty():
        my_queue.get().start()


def search_instance(search):
    while True:
        try:
            bucket_name = search.string_generator.next()

            #Just in case the bucket has been found, don't try again.
            #Not storing all to prevent massive memory usage.
            if bucket_name not in search.buckets_found:
                bucket_response = check_s3_bucket(bucket_name)
                if bucket_response["exists"] == True:
                    search.buckets_found.append(bucket_name)
                    log_bucket_found(bucket_response=bucket_response, output_file=search.output_file)

                #Increment progress and sleep                
                search.progressbar()
                if search.print_bucket_names:
                    search.progressbar.total_items += 1
                    print bucket_name
                time.sleep(sleep_sec_between_attempts)
        #Generator is empty...done
        except StopIteration:
            break
        #Generator is already running for another thread
        except ValueError:
            pass
