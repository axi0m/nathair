#!/usr/bin/env python3
# Ref: Inspiration from ARR on PythonistaCafe

import argparse
import os
import sys
from requests_html import HTMLSession
from tqdm import tqdm


__version__ = '12.2020'
url = 'https://virusshare.com/hashes'


def main(url):
    '''
    Write local text file of MD5 hashes for malware from virusshare.com
    '''

    try:
        session = HTMLSession()
        r = session.get(url)
        print(f'[+] Identifying hash set range from {url}')
    except Exception as error:
        print(f'[-] Error encountered, exiting... {error}')
        sys.exit(1)
    else:
        print(f'[+] Page {url} successfully accessed')

    # Define list of all links
    absolute_urls = r.html.absolute_links
    
    # Init default hashset URL list
    hashset_urls = []

    # Process all URLs looking for those with 'hashfiles' in the URL
    for link in absolute_urls:
        if 'hashfiles' in link:
            hashset_urls.append(link)

    print(f'[+] Unique hash set URLs: {len(hashset_urls)}')

    # Establish range for tqdm context manager
    max_hash = len(hashset_urls)

    # Establish HTML Session object
    session2 = HTMLSession()

    with tqdm(total=max_hash, position=0, desc="Downloading MD5 hashes") as progress:
        for link in hashset_urls:
            response = session2.get(link)
            if response.status_code == 200:
                hashes_list = response.text.split('\n')
                progress.update(1)

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
        print(f'[!] Output file already exists, overwriting...')

    # run the program
    main(url='https://virusshare.com/hashes')