#!/usr/bin/python

import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--domain", nargs="?",
    action="store", dest="domain",
    help="The domain to lookup in Whois database."
)
parser.add_argument(
    "--apikey",
    nargs="?",
    action="store",
    dest="apikey",
    help="The secret API key",
)

# Parse our arguments provided at CLI
args = parser.parse_args()

# Verify the variables were provided or print help
if not args.domain:
    parser.print_help()
    exit(1)

if not args.apikey:
    parser.print_help()
    exit(1)

# Set to cleaner variable names for ease later on
apiKey = args.apikey
domainName = args.domain

def perform_request(domainName, apiKey, url):
    payload = {'domainName': domainName, 'apiKey': apiKey, 'outputFormat': 'JSON'}
    r = requests.get(url, params=payload)
    return r

def main():
    result = perform_request(domainName, apiKey, 'https://www.whoisxmlapi.com/whoisserver/WhoisService')

    json_response = result.json()

    print(f"Registrar for domain {domainName} is {json_response['WhoisRecord']['registrarName']}")

if __name__ == "__main__":
    main()