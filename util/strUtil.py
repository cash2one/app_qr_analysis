# -*- coding=utf-8 -*-
import string
import hashlib
import random

UNICODE_ASCII_CHARACTERS = (string.ascii_letters.decode('ascii') +
                            string.digits.decode('ascii'))


def md5(str):
    m = hashlib.md5(str)
    m.digest()
    _password = m.hexdigest()
    return _password


def random_ascii_string(length):
    return ''.join([random.choice(UNICODE_ASCII_CHARACTERS) for x in xrange(length)])

if __name__ == '__main__':
    print UNICODE_ASCII_CHARACTERS
    print string.ascii_letters.decode('ascii')
    print string.digits.decode('ascii')
    # a = [random_ascii_string(32) for i in range(100000) ]
    #from collections import Counter
    #print Counter(a)

