#!/usr/bin/env python
import random, requests, time, re
from constants import base_url

no_bucket_responses = [
                        "NoSuchBucket",
                        "InvalidBucketName",
                       ]
denied_responses = [
                    "AccessDenied",
                    "AllAccessDisabled",
                   ]

def check_s3_bucket(bucket_name, redirect=False):
    bucket_result = {
                        "name":bucket_name,
                        "url":"{base_url}{bucket_name}".format(base_url=base_url, bucket_name=bucket_name),
                        "exists":False,
                        "public":None,
                        "empty":None,
                        "error":False,
                        "redirected":False,
                    }
    if redirect:
        bucket_result["redirected"] = True
        bucket_result["url"] = "https://{bucket_name}.s3.amazonaws.com".format(bucket_name=bucket_name)
   
    try:
        request = requests.get(bucket_result["url"], verify=False)
    except Exception as e:
        bucket_result["error"] = e
        return bucket_result

    for no_bucket_response in no_bucket_responses:
        if "<Code>{message}</Code>".format(message=no_bucket_response) in request.text:
            bucket_result["error"] = no_bucket_response
            return bucket_result

    for denied_response in denied_responses:
        if "<Code>{message}</Code>".format(message=denied_response) in request.text:
            bucket_result["exists"] = True
            bucket_result["public"] = False
            bucket_result["error"] = denied_response
            return bucket_result

    #If a redirect is seen, go to it
    if "<Endpoint>" in request.text:
        return check_s3_bucket(bucket_name=re.search("<Endpoint>(.+?)</Endpoint>", request.text).group(1).replace(".s3.amazonaws.com",""), redirect=True)
    #At this point the bucket exists, just seeing if it is empty
    else:
        bucket_result["exists"] = True
        bucket_result["public"] = True
        if "<Key>" in request.text:
            bucket_result["empty"] = False
            return bucket_result
        else:
            return bucket_result

