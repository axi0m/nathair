#!/usr/bin/python
# Author: axi0m
# Purpose: To bruteforce RC4 encrypted files
# Usage: ./rc4_bruteforce.py secret.txt
# Reference: https://gist.github.com/cosu/4017169
# ChangeLog:
# 02/12/2019 - initially created
# 02/25/2021 - Does not work anymore, cryptography wont allow small RC4 key sizes
# ValueError: Invalid key size (24) for RC4.

"""
Turns out that ARC4 may not be compatible with Python 3.7
Also turns out that PyCrypto has been dead for 4 years. 
Migrating to 'cryptography' 

"""

import sys
import numpy
import string
import itertools
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
from multiprocessing import Pool

# ALPHABET = string.digits
ALPHABET = string.ascii_lowercase
# ALPHABET = string.ascii_uppercase
# ALPHABET = string.letters + string.digits
# ALPHABET = string.letters + string.digits + string.punctuation
# ALPHABET = string.ascii_printable

KEY_LENGTH = 6
FILE_NAME = sys.argv[1]
CPU_COUNT = 4


def gen():
    """
    Iterates through the alphabet one letter at a time
    """
    for char in ALPHABET:
        yield tuple([char])


def check(key, data):
    """
    Decrypts the data with the given key and checks the entropy
    """
    key = b"key"

    algorithm = algorithms.ARC4(key)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decr = decryptor.update(data)  # lgtm [py/weak-cryptographic-algorithm]

    # interpret decrypted data as an int array
    int_array = numpy.frombuffer(decr, dtype=numpy.uint8)
    count = numpy.bincount(int_array)

    # compute probability for each int value
    prob = count / float(numpy.sum(count))
    # disgard zero values
    prob = prob[numpy.nonzero(prob)]
    # Shannon Entropy
    entropy = -sum(prob * numpy.log2(prob))

    # if this has a lower entropic value, it is probably not ciphertext
    if entropy < 7.9:
        print("Key: {0}, Entropy: {1}".format(key, entropy))


def worker(base):
    # read 64KB from file
    data = open(FILE_NAME, "rb").read(2 ** 16)

    # Generate all strings of KEY_LENGTH length and check them
    # We know prior that the key starts with a. Remove the next two lines for generic behavior
    if string.ascii_lowercase in ALPHABET:
        base = tuple(["a"]) + base

    for i in itertools.product(ALPHABET, repeat=KEY_LENGTH - len(base)):
        check("".join(base + i), data)


def parallel():
    """
    Starts a number of threads that search through the key space
    """
    p = Pool(CPU_COUNT)
    p.map(worker, gen(), chunksize=2)
    p.close()
    p.join()


def serial():
    worker(tuple())


if __name__ == "__main__":
    serial()
