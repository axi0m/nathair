#!/usr/bin/env python3
# Ref: Inspiration from ARR on PythonistaCafe

import argparse
import os
import requests
import sys
import urllib.parse
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track

__version__ = '06.21.2021'

# Init rich console
console = Console()

# Base URL for VirusShare.com
base = 'https://virusshare.com/hashes'

def main(url):
    '''
    Write local text file of MD5 hashes for malware from virusshare.com
    '''

    try:
        # Create persistent HTTP session for requests
        s = requests.Session()
        # Generate response object for given URL
        r = s.get(url)
        console.print(f'[+] Identifying hash set range from {url}')
    except Exception as error:
        console.print(f'[-] Error encountered, exiting... {error}')
        sys.exit(1)
    else:
        console.print(f'[+] Page {url} successfully accessed')

    # Parse HTML from requests response content
    soup = BeautifulSoup(r.content, 'html.parser')

    # Init default hashset URL list
    hashset_urls = []

    # Define list of all links
    tags = soup.find_all('a')
    for tag in tags:
        # Iterate over all link tags looking for those with 'hashfiles' only
        if 'hashfiles' in tag.get('href'):
            # Ignore the 121MB unpacked to packed hash file
            if 'unpacked' in tag.get('href'):
                pass
            else:
                absolute_url = urllib.parse.urljoin(base, tag.get('href'))
                hashset_urls.append(absolute_url)

    console.print(f'[+] Unique hash set URLs: {len(hashset_urls)}')

    # Iterate over the list of hash URLs
    for link in track(hashset_urls, description="Downloading MD5 hashes..."):
        response = s.get(link, timeout=5)
        if response.status_code == 200:
            hashes_list = response.text.split('\n')

            with open(args.output, 'a+') as hashfile:
                for line in hashes_list:
                    if not line.startswith('#') and line != '':
                        # write to output file
                        hashfile.write(line + '\n')


if __name__ == '__main__':

    # define argparser:
    parser = argparse.ArgumentParser(description='VirusShare MD5 Hash List Generator; all arguments are optional',
                                     usage='./virus_md5.py -o hash.txt')
    # output argument
    parser.add_argument('-o', '--output',  help='Output file (optional, default=hash.txt)', default='./hash.txt')

    # version
    parser.add_argument('-v', '--version', help='Displays script version', action='version', version=str(__version__))

    # parse the arguments
    args = parser.parse_args()

    if os.path.exists(args.output):
        console.print(f'[!] Output file already exists, overwriting...')

    # run the program
    main(url='https://virusshare.com/hashes')