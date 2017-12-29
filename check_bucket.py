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


#S3 Connector
from boto.s3.connection import S3Connection

explained = {
    'READ': 'readable',
    'WRITE': 'writable',
    'READ_ACP': 'permissions readable',
    'WRITE_ACP': 'permissions writeable',
    'FULL_CONTROL': 'Full Control'
}
groups_to_check = {
    'http://acs.amazonaws.com/groups/global/AllUsers': 'Everyone',
    'http://acs.amazonaws.com/groups/global/AuthenticatedUsers': 'Authenticated AWS users'
}


def check_s3_bucket(bucket_name, access_key, secret_key, redirect=False):
    bucket_result = {
                        "name":bucket_name,
                        "url":"{base_url}{bucket_name}".format(base_url=base_url, bucket_name=bucket_name),
                        "exists":False,
                        "public":None,
                        "authenticated_access":False,
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

    if access_key and secret_key:
        for denied_response in denied_responses:
            if "<Code>{message}</Code>".format(message=denied_response) in request.text:
                bucket_result["exists"] = True
                bucket_result["public"] = False
                bucket_result["error"] = denied_response
                if denied_response == "AccessDenied":
                    try:
                        conn = S3Connection(access_key, secret_key)
                        bucket = conn.get_bucket(bucket_name)
                        issues = check_acl(bucket)
                        if issues:
                            print '''
************************************************************************************
AUTHENTICATED ACCESS - %s
************************************************************************************
''' % (bucket_result["url"])
                            # This is how you can get the keys if you want it
                            # for key in bucket.list():
                                # print key
                            bucket_result["authenticated_access"] = True
                        return bucket_result
                    except Exception as e:
                        # print e
                        return bucket_result

    #If a redirect is seen, go to it
    if "<Endpoint>" in request.text:
        return check_s3_bucket(
                                bucket_name=re.search("<Endpoint>(.+?)</Endpoint>", request.text).group(1).replace(".s3.amazonaws.com",""), 
                                access_key=access_key, 
                                secret_key=secret_key,
                                redirect=True
                              )

    #At this point the bucket exists, just seeing if it is empty
    else:
        bucket_result["exists"] = True
        bucket_result["public"] = True
        if "<Key>" in request.text:
            bucket_result["empty"] = False
        else:
            bucket_result["empty"] = True

    return bucket_result


def check_acl(bucket):
    issues = []
    acp = bucket.get_acl()
    for grant in acp.acl.grants:
        if grant.type == 'Group' and grant.uri in groups_to_check:
            issues.append(
                            {
                                "permission" : grant.permission,
                                "explained" : explained[grant.permission],
                                "grantee" :  groups_to_check[grant.uri]
                            }
                         )
    return issues
