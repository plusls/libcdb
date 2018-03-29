# libcdb
a program to build libc-database



### How to Use 

First, edit your libcdbroot in libcdb.py



Add:

```bash
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py add '/home/plusls/Desktop/libc.so.6' '/home/plusls/Desktop/ctf/N1ctf/pwn/distrib/libc.so.6'
Add success!
Add success!
```



Delete:

```bash
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py delete b5381a457906d279073822a5ceb24c4bfef94ddb
Delete success!
```



Search:

```bash
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py search "{'system':284320, 'printf':353552}"
['aad7dbe330f23ea00ca63daf793b766b51aceb5d']
```



### To do

Auto get libc from Ubuntu, Debian, CentOS

