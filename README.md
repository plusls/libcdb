# libcdb
a program to build libc-database



### How to Use 

First, edit your libcdbroot in libcdb.py.

#### Add:

Usage:

```bash
./libcdb.py add libc
```

Add libc to libc-database.

For example:

```bash
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py add ../libc.so.6 
Add amd64 aad7dbe330f23ea00ca63daf793b766b51aceb5d!
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py add ../libc.so.6 
This libc:aad7dbe330f23ea00ca63daf793b766b51aceb5d has in libc-database.
```

#### Delete:

Usage:

```bash
./libcdb.py delete arch buildid
```

Delete libc from libc-database.

For example:

```bash
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py delete amd64 aad7dbe330f23ea00ca63daf793b766b51aceb5d
Delete success!
```

#### Search:

Usage:

```bash
./libcdb.py search arch libcdata
```

Search libc from libc-database.

For example:

```bash
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py search powerpc64 "{'system':348160, 'printf':408704}"
['1061ed71d47749f42fcaa0f2ac39c3eaa8fffa26']
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py search powerpc64 "{'system':348160, 'printf':408704, 'puts':0}"
[]
```

#### Update

Usage:

```bash
./libcdb.py update
```

Libcdb will auto download all libc from ubuntu.

For example:

```bash
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py update
2018-03-30 02:33:28 URL:http://mirrors.ustc.edu.cn/ubuntu/pool/main/e/eglibc/libc6-amd64_2.15-0ubuntu10.18_i386.deb [4608566/4608566] -> "/home/plusls/libcdbroot/download/libc6-amd64_2.15-0ubuntu10.18_i386.deb" [1]
Add amd64 6a93e9450a6dba5b0d7ef2769c86430fcf231184!
2018-03-30 02:33:34 URL:http://mirrors.ustc.edu.cn/ubuntu/pool/main/e/eglibc/libc6-amd64_2.15-0ubuntu10_i386.deb [4469586/4469586] -> "/home/plusls/libcdbroot/download/libc6-amd64_2.15-0ubuntu10_i386.deb" [1]
Add amd64 ea980a054cfa815c1155319d035c197d282d785d!
......
Update Ubuntu libc success!
plusls@plusls-virtual-machine:~/Desktop/libcdb$ ./libcdb.py update
Update Ubuntu libc success!
```



### To do

Auto get libc from ~~Ubuntu~~, Debian, CentOS.

Write web UI.

