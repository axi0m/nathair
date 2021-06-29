#!/usr/bin/python

import requests
import argparse
from colorama import Fore, init

init(autoreset=True)

# https://user.whoisxmlapi.com/products <- view usage limits
# default is 500 API queries per month for free API key
# TODO: Add a way to check usage limits before making requests, if we hit a soft limit (say 100 left) warn the user
# TODO: Use a local cache to reduce the number of API requests we submit

parser = argparse.ArgumentParser()
parser.add_argument(
    "--domain",
    nargs="?",
    action="store",
    dest="domain",
    help="The domain to lookup in Whois database.",
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
    """ HTTP Request to domain with specific headers and payload parameters """

    # We set UA to MacOS Firefox browser traffic
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:86.0) Gecko/20100101 Firefox/86.0"
    }

    # Set parameters as required by the WhoisXMLAPI
    payload = {"domainName": domainName, "apiKey": apiKey, "outputFormat": "JSON"}

    # Make the request passing in our headers and parameters
    r = requests.get(url, params=payload, headers=headers)

    return r


def main():
    """ Main function """
    result = perform_request(
        domainName, apiKey, "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    )

    # Get JSON
    json_response = result.json()
    # print(json_response)

    # Parse out the items of interest
    whois_record = json_response.get("WhoisRecord")
    registrar = whois_record.get("registrarName")
    registryData = json_response.get("registryData")

    print(Fore.GREEN + "Registrar for domain {} is : {}".format(domainName, registrar))

    if registryData is not None:
        registrant = registryData.get("registrant")

        if registrant is not None:
            organization = registrant.get("organization")
            state = registrant.get("state")
            country = registrant.get("country")
            country_code = registrant.get("countryCode")

            print(
                f"Registrant organization for domain {domainName} is : {organization}"
            )
            print(f"Registrant state for domain {domainName} is : {state}")
            print(f"Registrant country for domain {domainName} is : {country}")
            print(
                f"Registrant country code for domain {domainName} is : {country_code}"
            )
        else:
            print(
                f"[!] Registrant key was not found in registry data for domain: {domainName}"
            )
    else:
        registrant = whois_record.get("registrant")
        """ SAMPLE RESPONSE 
        {'name': 'Domain Administrator', 'organization': 'eBay Inc.', 'street1': '2145 Hamilton Avenue,', 'city': 'San Jose', 'state': 'CA', 'postalCode': '95125', 'country': 'UNITED STATES', 'countryCode': 'US', 'email': 'hostmaster@ebay.com', 'telephone': '14083769801', 'rawText': 'Registrant Name: Domain Administrator\nRegistrant Organization: eBay Inc.\nRegistrant Street: 2145 Hamilton Avenue,\nRegistrant City: San Jose\nRegistrant State/Province: CA\nRegistrant Postal Code: 95125\nRegistrant Country: US\nRegistrant Phone: +1.4083769801\nRegistrant Email: hostmaster@ebay.com'}
        """

        organization = registrant.get("organization")
        state = registrant.get("state")
        country = registrant.get("country")
        country_code = registrant.get("countryCode")

        print(f"Registrant organization for domain {domainName} is : {organization}")
        print(f"Registrant state for domain {domainName} is : {state}")
        print(f"Registrant country for domain {domainName} is : {country}")
        print(f"Registrant country code for domain {domainName} is : {country_code}")


if __name__ == "__main__":
    main()
