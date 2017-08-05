# Purpose
For a given comapny name, try a large variety of permutations in order to guess AWS S3 bucket names, identifying those that are public.

# Reason
Companies, far too often, have public S3 buckets with client data or PII in them.  Details of my adventures are here: https://www.mattsvensson.com/nerdings/2017/7/27/amazon-s3-bucket-searching-and-scraping

# Use
#Single threaded scan of a given company name<br>
./find_public_s3_buckets.py -t 1 -s "This Company Name"

#Dual threaded scan of the example file (company_names.txt)<br>
./find_public_s3_buckets.py -t 2 -l comapny_names.txt

#Dual threaded scan of the example file (company_names.txt), starting after "Harris Corporation"<br>
./find_public_s3_buckets.py -t 2 -l comapny_names.txt -a "Harris Corporation"

#Dual threaded scan of the example file (company_names.txt), starting after the 3rd line (using line 1 as the first)<br>
./find_public_s3_buckets.py -t 2 -l comapny_names.txt -n 3

# Notes
- Open bucket URLs will be written to open_buckets.txt in the root folder
- I wanted to print the names of the buckets, as they were being scanned.  If you don't want to, and just want the progressbar, you can comment out line 84 of "find_public_s3_buckets.py"
- The "scanned" file contains any number of text documents that contain prior lists that you have scanned.  All names in these files will be skipped, to prevent re-running names on random lists you try.
- On an AWS EC2 t2.micro instance, I was able to search 30 names/sec per thread.
- If an item has already been scanned, the number of compelted scans will increment
