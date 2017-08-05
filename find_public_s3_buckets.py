#!/usr/bin/env python
import random, requests, time, re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from progressbar import ProgressBar
import threading
import Queue
from constants import *
from get_previous_scans import *
from arg_parser import args
from generate_strings import *

def search_file(file_name, scanned_buckets, start_after_value, start_after_line_num, threads, print_bucket_names):
    """Searches through the names in the file, one by one (to save memory)"""

    #Create base search instance
    num_bucket_names = get_num_bucket_names(file_name, start_after_value, start_after_line_num)
    search = Search(bucket_names=[], num_buckets=num_bucket_names, threads=threads, print_bucket_names=print_bucket_names)

    found_start = True
    if start_after_line_num or start_after_value:
        found_start = False

    f = open(file_name, "r")
    for index, line in enumerate(f):
        line = line.strip()
        if not found_start:
            if start_after_line_num == (index + 1) or start_after_value == line:
                found_start = True
            continue
        else:
            if line and not any(scanned_bucket.strip() == line.strip() for scanned_bucket in scanned_buckets):
                search.bucket_names = get_string_variations(line)
                start_search(search)
                while search.bucket_names:
                    time.sleep(.5)
            else:
                print "Already scanned {line}".format(line=line)
                #Subtract the number of items skipped, to be sure #/sec isn't changed.
                search.progress.total_items -= len(get_string_variations(line))
                search.progress(num_compelted=0)


def get_num_bucket_names(file_name, start_after_value, start_after_line_num):
    """Calculates the number of buckets to scan, given the starting point that you want"""
    num_bucket_names = 0
    found_start = True
    if start_after_line_num or start_after_value:
        found_start = False

    f = open(file_name, "r")
    for index, line in enumerate(f):
        line = line.strip()
        if not found_start:
            if start_after_line_num == (index + 1) or start_after_value == line:
                found_start = True
            continue
        else:
            num_bucket_names += len(get_string_variations(line.strip()))
    return num_bucket_names


def start_search(search):
    """Run the specified number of threads of the searcher"""
    #Make the queue of all of the threads to run
    my_queue = Queue.Queue()
    for i in range(search.threads):
        t = threading.Thread(target=search_instance, args=(search, ))
        my_queue.put(t)

    #Run all of the threads
    while not my_queue.empty():
        my_queue.get().start()


def search_instance(search):
    """Run an threads of the s3 brute forcer"""
    while search.bucket_names:
        bucket_name = search.bucket_names.pop(0)       #Pops from start of array, use no param for end
        url = "{base_url}{bucket_name}".format(base_url=base_url, bucket_name=bucket_name)
        try_random_link(url)
        time.sleep(sleep_sec_between_attempts)
        search.progress()
        if search.print_bucket_names:
            print url


def try_random_link(url):
    """Try to get the URL, checking for bad strings"""
    try:
        request = requests.get(url, verify=False)
        if request.status_code < 400:
            for bad_response in bad_responses:
                if bad_response in request.text:
                    # print "\n\n{bad_response} -> {url}\n".format(bad_response=bad_response, url=url)
                    break
            else:
                #If a redirect is seen, go to it
                if "<Endpoint>" in request.text:
                    redirect_link = "https://{endpoint}".format(endpoint=re.search("<Endpoint>(.+?)</Endpoint>", request.text).group(1))
                    # print "-->> {url} redirected to {redirect_link}".format(url=url, redirect_link=redirect_link)
                    try_random_link(redirect_link)
                else:
                    print "\n\n*** {status_code} -> {url} ***\n".format(status_code=request.status_code, url=url)
                    log_bucket(file="open_buckets", url=url)
    except Exception as e:
        print "\n\nERROR - {url} - {error}\n".format(url=url, error=e)
        # log_bucket(file="error", url=url)


def log_bucket(file, url):
    """Writes potentially open buckets to a file"""
    f = open("{file}.txt".format(file=file), "a")
    f.write("{url}\n".format(url=url))
    f.close()


class Search():
    def __init__(self, bucket_names, num_buckets, threads, print_bucket_names):
        self.bucket_names = bucket_names
        self.num_buckets = num_buckets
        self.threads = threads
        self.print_bucket_names = print_bucket_names
        self.progress = ProgressBar(num_buckets)


if __name__ == "__main__": 
    #Either get the list from a file's list or the string provided via the command line
    if args.list:
        bucket_names = search_file(
                                    file_name = args.list, 
                                    scanned_buckets = get_previous_scans(),
                                    start_after_value = args.start_after_value,
                                    start_after_line_num = args.start_after_line_num,
                                    threads = args.threads,
                                    print_bucket_names = args.print_bucket_names
                                  )
    elif args.string:
        bucket_names = get_string_variations(args.string)
        start_search(
                        Search(
                                bucket_names = bucket_names, 
                                num_buckets = len(bucket_names),
                                threads = args.threads,
                                print_bucket_names = args.print_bucket_names,
                              )
                      )
