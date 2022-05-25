#!/usr/bin/env python3

import os, boto3, base64, json, requests
import urllib.parse
from signer import headers_for_signed_url

#assume AWS role with access to Conjur Secrets
client = boto3.client('sts')
awsRoleArn = os.environ['AWS_ROLE_ARN']
assumeConjurRole = client.assume_role(RoleArn=awsRoleArn, RoleSessionName='10001', DurationSeconds=900)

#get signed AWSv4 headers from STS GetCallerID Function
signed_headers = headers_for_signed_url(assumeConjurRole["Credentials"]["AccessKeyId"], 
    assumeConjurRole["Credentials"]["SecretAccessKey"], 
    assumeConjurRole["Credentials"]["SessionToken"],
    'us-east-1')

#declare and init Conjur variables
conjur_url = os.environ.get("CONJUR_APPLIANCE_URL")
conjur_acct = os.environ.get("CONJUR_ACCOUNT")
secretID = os.environ.get("SECRET_ID")
host = os.environ.get("CONJUR_AUTHN_LOGIN")
cert = os.environ.get("VALIDATE_CERT")
if cert == "false":
    cert = False
else:
    cert = True

#get authentication token by providing AWSv4 signature, Conjur will validate the signature against AWS
authenticate_url = "{conjur_appliance_url}/authn-iam/prod/{account}/{host}/authenticate".format(
                        conjur_appliance_url = conjur_url,
                        account = conjur_acct,
                        host = urllib.parse.quote_plus(host)
                    )
print("Authenticate URL: {}".format(authenticate_url))
authResponse = requests.post(authenticate_url, data=signed_headers, verify=cert)
print("Authentication Response: " + str(authResponse.status_code))
#convert auth token to base64
token_b64 = base64.b64encode(authResponse.text.encode('utf-8')).decode("utf-8")

#now we can retrieve secrets to our heart's content
retrieve_variable_url = "{conjur_appliance_url}/secrets/{account}/variable/".format(
                            conjur_appliance_url = conjur_url,
                            account = conjur_acct
                            )
password = requests.get(retrieve_variable_url + secretID,
                    headers={'Authorization' : "Token token=\"" + token_b64 + "\""}, verify=cert).text

result = 'password:' + password
print(result)
