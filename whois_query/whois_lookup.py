#!/usr/bin/python

import requests
import argparse
import sys
from rich.console import Console

console = Console()

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
    sys.exit(1)

if not args.apikey:
    parser.print_help()
    sys.exit(1)

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


def parse_whois(whoisRecord: dict, domainName: str):
    ''' Input whois record dict and return select fields to console '''

    # Custom dictionary
    limited_info = {}

    # There are some records mapped to organization itself, data structure is different, e.g. ebay.com
    registrarName = whoisRecord.get('registrarName')
    registryData = whoisRecord.get('registryData')
    registrant = whoisRecord.get('registrant')

    if registrant is None and registryData is None:
        console.print(f"[!] No registry/registrar information in Whois record for domain: [blue]{domainName}[/blue]", style="bold red")
        return False

    if registrant is None:
        registrant = registryData.get('registrant')

    if registrant is not None:
        organization = registrant.get('organization')
        state = registrant.get('state')
        country = registrant.get('country')
        country_code = registrant.get('countryCode')
    
        limited_info.update({'Registrar Name': registrarName})
        limited_info.update({'Country Code': country_code})
        limited_info.update({'Country': country})
        limited_info.update({'State': state})
        limited_info.update({'Organization': organization})

        return limited_info


def main():
    """ Main function """
    result = perform_request(
        domainName, apiKey, "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    )

    # Get JSON
    json_response = result.json()

    # for k,v in json_response.items():
    #     console.print(k,v)

    # If 401 remind user API key may be wrong
    if result.status_code == 401:
        console.print(f"[!] HTTP 401 Unauthorized - Verify your API key", style="bold red")
        sys.exit(1)

    # Parse the whois record
    whois_record = json_response.get('WhoisRecord')
    limited_info = parse_whois(whois_record, domainName)

    console.print(f"[+] Registrar for domain {domainName} is: [blue]{limited_info['Registrar Name']}[/blue]", style="bold green")
    console.print(f"[+] Registrant organization for domain {domainName} is: [blue]{limited_info['Organization']}[/blue]", style="bold green")
    console.print(f"[+] Registrant state for domain {domainName} is: [blue]{limited_info['State']}[/blue]", style="bold green")
    console.print(f"[+] Registrant country for domain {domainName} is: [blue]{limited_info['Country']}[/blue]", style="bold green")
    console.print(f"[+] Registrant country code for domain {domainName} is: [blue]{limited_info['Country Code']}[/blue]", style="bold green")




if __name__ == "__main__":
    main()
