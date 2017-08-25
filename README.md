# Purpose
For a given comapny name, try a large variety of permutations in order to guess AWS S3 bucket names, identifying those that are public, printing them to the screen and open_buckets.txt.

For a given set of chars (e.g. abc123) and a number range (e.g. 3-5), generate random strings within the length range, using the given set of chars, to find public buckets, printing them to the screen and open_buckets.txt.

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

#Dual threaded scan of the example file (company_names.txt), printing every guessed bucketname <br>
./find_public_s3_buckets.py -t 2 -l comapny_names.txt -p

#Single thread, random strings with lowercase letters, 3-5 chars long.
./find_public_s3_buckets.py -t 1 -r abcdefghijklmnopqrstuvwxyz -c 3-5

# Output - List of names
Without the -p modifier, you will see a progressbar, like below<br>
  0% [&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 28/21,147   3/sec   eta 1h 40m 22s

With the -p modifier, you will see the same progress bar printed (with updated) and every guessed name you try.<br>
  0% [&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 1/1,064   1/sec   eta 10m 49s     https://s3.amazonaws.com/Test<br>
  0% [&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 2/1,064   1/sec   eta 16m 16s     https://s3.amazonaws.com/Test-Company<br>
  0% [&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 3/1,064   1/sec   eta 12m 15s     https://s3.amazonaws.com/Test-Company-archive<br>
  0% [&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 4/1,064   1/sec   eta 10m 13s     https://s3.amazonaws.com/Test-Company-backup<br>
  0% [&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 5/1,064   1/sec   eta 9m 4s     https://s3.amazonaws.com/Test-Company-bak<br>
  0% [&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 6/1,064   2/sec   eta 8m 14s     https://s3.amazonaws.com/Test-Company-beta<br>

# Notes
- On lists, I would recommend running this inside of tmux or screen with the -p option so that you can see the current comapny being scanned in case an error is thrown and it stops or you want to manually stop it.
- Open bucket URLs will be written to open_buckets.txt in the root folder
- The "scanned" folder contains prior lists that you have scanned.  All names (by line) in these files will be skipped during the scan, to prevent re-running names on random lists you try.
- On an AWS EC2 t2.micro instance, I was able to search 30 names/sec per thread.
