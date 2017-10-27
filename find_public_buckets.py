#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from arg_parser import args
from get_previous_scans import *
from generate_strings import *
from search_obj import *
from run_comb_perm_search import *
from run_name_perm_search import *
from run_random_search import *


if __name__ == "__main__": 
    #Search a given list of company names, permuting them
    if args.list:
        bucket_names = search_file(
                                    file_name = args.list,
                                    prefix_postfix_option = args.prefix_or_postfix,
                                    acronyms_only_option = args.acronyms_only,
                                    scanned_buckets = get_previous_scans(),
                                    start_after_value = args.start_after_value,
                                    start_after_line_num = args.start_after_line_num,
                                    threads = args.threads,
                                    print_bucket_names = args.print_bucket_names,
                                    output_file = args.output_file
                                  )
    #Search permutations of a string
    elif args.string:
        bucket_names = get_string_variations(args.string, args.prefix_or_postfix, args.acronyms_only)
        start_search(
                        SearchNames(
                                bucket_names = bucket_names, 
                                num_buckets = len(bucket_names),
                                threads = args.threads,
                                print_bucket_names = args.print_bucket_names,
                                output_file = args.output_file,
                              )
                      )
    #Search RANDOM combinations and permutations of a given set of characters for a given length or range of lengths
    elif args.random_string_options:
        if args.num_chars or args.num_chars_range:
            if args.num_chars_range and "-" not in args.num_chars_range:
                print '''\n*** Need to define the '-cr' option with a range, e.g. 3-4 ***\n'''
            else:
                run_random_search(
                                    SearchStrings(
                                        num_chars=args.num_chars,
                                        num_chars_range=args.num_chars_range,
                                        string_options = args.random_string_options,
                                        threads = args.threads,
                                        print_bucket_names = args.print_bucket_names,
                                        output_file = args.output_file,
                                        start_after_value = None,
                                        stop_at_value = None
                                    )
                                 )
        else:
            print '''\n*** Need to define the number of chars or range using the '-c' or '-cr' option ***\n'''
    #Search combinations and permutations of a set of characters for a given length
    elif args.all_comb_perm:
        if args.num_chars:
            run_comb_perm_search(
                                    SearchStrings(
                                        num_chars=args.num_chars,
                                        num_chars_range=args.num_chars_range,
                                        string_options = args.all_comb_perm,
                                        threads = args.threads,
                                        print_bucket_names = args.print_bucket_names,
                                        output_file = args.output_file,
                                        start_after_value = args.start_after_value,
                                        stop_at_value = args.stop_at_value
                                    )
                                )
        else:
            print '''\n*** Need to define the number of chars or range using the '-c' option ***\n'''
