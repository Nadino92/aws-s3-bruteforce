#!/usr/bin/env python
import threading
import Queue
import itertools
import random, time
from progressbar import ProgressBar
from constants import *
from check_bucket import *
from logger import *

def createStringGenerator(string_options, num_chars):
    for item in itertools.product(string_options, repeat=num_chars):
        yield "".join(item)


def run_comb_perm_search(search):
    #Create progressbar to show how many searches have been done, removing eta
    search.progressbar = ProgressBar(total_items=get_num_comb_perm(string_options=search.string_options, num_chars=search.num_chars))
    search.progressbar.fmt = '''%(percent)3d%% %(bar)s %(current)s/%(total_items)s   %(items_per_sec)s   ETA: %(eta)s'''

    #Get all public butets that have been found so far
    search.buckets_found = get_buckets_found(search.output_file)
    #Create a string generator
    search.string_generator = createStringGenerator(search.string_options, search.num_chars)

    #Check and see if a start after value was provided
    if search.start_after_value:
        search.start_after_found = False
    else:
        search.start_after_found = True

    #See if a stop at value is seen
    if search.stop_at_value:
        search.stop_at_found = False
    else:
        search.stop_at_found = False
    
    my_queue = Queue.Queue()
    for i in range(search.threads+1):
        t = threading.Thread(target=search_instance, args=(search, ))
        my_queue.put(t)

    #Run all of the threads
    while not my_queue.empty():
        my_queue.get().start()


def search_instance(search):
    #Run the search across all combinations/permutations
    while True:
        try:
            bucket_name = search.string_generator.next()

            #Check and see if you're at the stopping point
            if search.stop_at_value == bucket_name:
                search.stop_at_found = True
            if search.stop_at_value and search.stop_at_found:
                break

            #Check and see if the starting point exists or has been found
            if not search.start_after_found:
                if bucket_name == search.start_after_value:
                    search.start_after_found = True
                search.progressbar.total_items -= 1
                continue
            
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
                    print bucket_name
                time.sleep(sleep_sec_between_attempts)
        #Generator is empty...done
        except StopIteration:
            break
        #Generator is already running for another thread
        except ValueError:
            pass


def get_num_comb_perm(string_options, num_chars):
    """Gets the number of combintions/permutations for the given string and number of chars"""
    num_comb_perm = 0
    for item in itertools.product(string_options, repeat=num_chars):
        num_comb_perm += 1
    return num_comb_perm


