#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import sys

from libcdblib.manage import add
from libcdblib.manage import delete
from libcdblib.manage import search
from libcdblib.getlibc.get_ubuntu_libc import get_all_ubuntu_libc


LIBCDBROOT = '/home/plusls/libcdbroot'

def update():
    get_all_ubuntu_libc('/home/plusls/libcdbroot')


def main():
    argv = sys.argv[1:]
    if argv[0] == 'add':
        for i in range(1, len(argv)):
            add(LIBCDBROOT, argv[i])
    elif argv[0] == 'delete':
        for i in range(2, len(argv)):
            delete(LIBCDBROOT, argv[1], argv[i])
            print('Delete success!')
    elif argv[0] == 'search':
        libc_data = eval(argv[2])
        print(search(LIBCDBROOT, argv[1], libc_data))
    elif argv[0] == 'update':
        update()

if __name__ == '__main__':
    main()