#!/usr/bin/env python3

"""
Queries VirusShare.com
Downloads MD5
Creates TXT File
"""

from __future__ import print_function
import argparse
import os
import ssl
import sys
import tqdm
from urllib.request import urlopen
import urllib.error


__version__ = '24.03.2019'


def main():
    # docstring
    """
    Input: none
    Description:
    -checks arguments
    -accesses webpage
    -downloads hashes
    -writes hashes to txt
    Output: hash.txt
    """

    # check output argument
    if not args.output.endswith('.txt'):
        print('Missing output-file (hash.txt)')
        sys.exit('Try again (path/hash.txt)')

    directory = os.path.dirname(args.output)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as err:
            print(args.output, 'could not be created')
            sys.exit('Try again')

    # setup variables
    url = 'https://virusshare.com/hashes.4n6'
    # create SSL context
    context = ssl._create_unverified_context()
    print('[+] Identifying hash set range from {}'.format(url))

    # # hash-counter
    hash_counter = 0

    # open the webpage
    try:
        # save webpage content to variable
        source_page = urlopen(url, context=context).read().decode('utf-8')
    except urllib.error.HTTPError as error:
        print('[-] Error accessing webpage - exiting...')
        sys.exit(1)
    else:
        print('[+] Web-Page successfully accessed')

    # identify latest hash list
    # <a href="hashes/VirusShare_00357.md5">357</a>

    # get int index of last hashlist
    latest_index = source_page.rfind(r'<a href="hashes/VirusShare_')
    # slice the string
    # 27 = a href="hashes/VirusShare_
    # 5 = 00357
    # lstrip removes leading 0s
    latest_page = int(source_page[latest_index + 27: latest_index + 27 + 5].lstrip('0'))

    # check if -s (start) flag is set
    # default value for args.start = 0
    if args.start == 0:
        # set start to 0
        start_page = args.start
    # if a start value was set
    else:
        # set start to user chosen value
        start_page = args.start

    # user info
    print('[+] MD5 Start-List:', str(start_page))
    print('[+] Latest MD5-List:', str(latest_page))

    # check if the start value is valid
    if start_page < 0 or start_page > latest_page:
        print('[-] Invalid MD5 Start-List:', str(start_page))
        sys.exit('Try again')
    # if start is valid
    else:
        print('[+] Creating MD5-Hashset from pages {} to {}'.format(start_page, latest_page))

    # process page per page; setup progress-bar
    for int_page in tqdm.trange(start_page, latest_page + 1, unit_scale=True, desc='Progress'):
        # create base URL
        # convert int_page nr to string in order to use it in the URL;
        # the page-number must have 5 digits, zfill() does the padding
        url_hash = 'https://virusshare.com/hashes/VirusShare_{}.md5'.format(str(int_page).zfill(5))

        # open, read, decode the hash lists
        try:
            # open each page
            hashes = urlopen(url_hash, context=context).read().decode('utf-8')

            # split each line; split() creates a list
            hashes_list = hashes.split('\n')
        except urllib.error.HTTPError as error:
            print('[-] Error accessing webpage for hash list {} - continuing...'.format(int_page))
            continue
        else:
            # write hashes to output file
            # open output-file; a+ = open for reading and writing
            with open(args.output, 'a+') as hashfile:
                # process hashes_list list
                for line in hashes_list:
                    # do not process lines that start with # or empty lines
                    if not line.startswith('#') and line != '':
                        # increment hash counter
                        hash_counter += 1
                        # write to output file
                        hashfile.write(line + '\n')

    # rename output-file
    old_name = args.output
    new_name = old_name[:-4] + '_' + str(latest_page) + '.txt'
    try:
        os.rename(old_name, new_name)
    except PermissionError as err:
        # user info
        print('[+] Finished downloading {} hashes into {}'.format(hash_counter, args.output))
        print('You may want to append the nr. of the latest MD5-List {} to {}'.format(latest_page, args.output))
    else:
        # user info
        print('[+] Finished downloading {} hashes into {}'.format(hash_counter, new_name))

    # exit
    sys.exit(0)


if __name__ == '__main__':
    """
    Input: none
    Description: argument parser; call main()
    Output: none
    """

    # define argparser:
    parser = argparse.ArgumentParser(description='VirusShare - MD5 Hash-List Generator; all arguments are optional',
                                     usage='./script.py -o hash.txt',
                                     epilog='Developed by ARR - v.24.03.2019')
    # output-file argument
    parser.add_argument('-o', '--output',  help='Output file (optional, default=hash.txt)', default='./hash.txt')

    # output-file argument
    parser.add_argument('-s', '--start', type=int,  help='Specify MD5 Start-List (optional, default=0)', default=0)

    # version
    parser.add_argument('-v', '--version', help='Displays Script Version', action='version', version=str(__version__))

    # parse the arguments
    args = parser.parse_args()

    # run the program
    main()