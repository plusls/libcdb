#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import sys

from libcdblib.manage import add
from libcdblib.manage import delete
from libcdblib.manage import search

LIBCDBROOT = '/home/plusls/libcdbroot'

def main():
    argv = sys.argv[1:]
    if argv[0] == 'add':
        for i in range(1, len(argv)):
            add(LIBCDBROOT, argv[i])
            print('Add success!')
    elif argv[0] == 'delete':
        for i in range(1, len(argv)):
            delete(LIBCDBROOT, argv[i])
            print('Delete success!')
    elif argv[0] == 'search':
        libc_data = eval(argv[1])
        print(search(LIBCDBROOT, libc_data))

    #add('/home/plusls/libcdbroot', '/home/plusls/Desktop/libc.so.6')
    #add('/home/plusls/libcdbroot', '/home/plusls/Desktop/ctf/N1ctf/pwn/distrib/libc.so.6')
    #input()
    #delete('/home/plusls/libcdbroot', 'aad7dbe330f23ea00ca63daf793b766b51aceb5d')
    #delete('/home/plusls/libcdbroot', 'b5381a457906d279073822a5ceb24c4bfef94ddb')
    #print(search('/home/plusls/libcdbroot', {'system':284320, 'printf':353552}))
    #print(search('/home/plusls/libcdbroot', {'system':284320, 'printf':353552, 'puts':461088}))
    #print(ELF('/home/plusls/Desktop/libc.so.6').symbols['puts'])

if __name__ == '__main__':
    main()