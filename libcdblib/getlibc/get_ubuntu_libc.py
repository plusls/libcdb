''' get ubuntu libc '''

import requests
import os
import re
import json
import subprocess
from libcdblib.manage import add
from libcdblib.elf import ELF


def get_all_ubuntu_libc(libcdb_root, source_url='http://mirrors.ustc.edu.cn/'):
    ''' get all ubuntu libc
    '''


    url1 = source_url + 'ubuntu/pool/main/e/eglibc/'
    deb_list1 = re.findall(r'>(libc6.+?\.deb)<', requests.get(url1).content.decode())
    url2 = source_url + 'ubuntu-ports/pool/main/e/eglibc/'
    deb_list2 = re.findall(r'>(libc6.+?\.deb)<', requests.get(url2).content.decode())
    url3 = source_url + 'ubuntu/pool/main/g/glibc/'
    deb_list3 = re.findall(r'>(libc6.+?\.deb)<', requests.get(url3).content.decode())
    url4 = source_url + 'ubuntu-ports/pool/main/g/glibc/'
    deb_list4 = re.findall(r'>(libc6.+?\.deb)<', requests.get(url4).content.decode())
    download_path = libcdb_root + '/download'

    _mkdir(libcdb_root)
    _mkdir(download_path)
    arch_list = os.listdir(libcdb_root)
    buildid_dict = dict()
    arch_dict = dict()
    for arch in arch_list:
        # 不是文件夹就继续
        if os.path.isdir('%s/%s' % (libcdb_root, arch)) is False:
            continue
        try:
            fp = open('%s/%s/build-id.json' % (libcdb_root, arch), 'r')
            buidid_json_str = fp.read()
            fp.close()
            arch_dict[arch] = json.loads(buidid_json_str)
            buildid_dict.update(arch_dict[arch])
        except FileNotFoundError:
            pass
    try:
        fp = open('%s/void-pkg.json' % (libcdb_root, ), 'r')
        buidid_json_str = fp.read()
        fp.close()
        arch_dict['void-pkg'] = json.loads(buidid_json_str)
        buildid_dict.update(arch_dict['void-pkg'])
    except FileNotFoundError:
        pass

    _download_deb(libcdb_root, url1, deb_list1, buildid_dict, arch_dict)
    _download_deb(libcdb_root, url2, deb_list2, buildid_dict, arch_dict)
    _download_deb(libcdb_root, url3, deb_list3, buildid_dict, arch_dict)
    _download_deb(libcdb_root, url4, deb_list4, buildid_dict, arch_dict)
    print('Update Ubuntu libc success!')
def _download_deb(libcdb_root, url, deb_list, buidid_dict, arch_dict):
    download_path = libcdb_root + '/download'
    # print(deb_list)
    for deb in deb_list:
        if deb not in buidid_dict:
            if os.system('wget -nvc %s%s -O %s/%s' % (url, deb, download_path, deb)) != 0:
                print('%s download faild!' % deb)
                continue
            _mkdir('%s/%s' % (download_path, deb[:-4]))
            if os.system('cd %s/%s && ar -x ../%s -o data.tar.gz 2>/dev/null && tar -xf data.tar.gz 2>/dev/null' % (download_path, deb[:-4], deb)) != 0:
                if os.system('cd %s/%s && ar -x ../%s -o data.tar.xz && tar -xf data.tar.xz' % (download_path, deb[:-4], deb)) != 0:
                    print('%s unpack faild!' % deb)
                    continue
            libc_path_list = subprocess.check_output(['find', '%s/%s' % (download_path, deb[:-4]), '-name', 'libc-*.so']).decode().split('\n')

            # 记录空包
            if len(libc_path_list) == 1:
                if 'void-pkg' not in arch_dict:
                    arch_dict['void-pkg'] = dict()
                arch_dict['void-pkg'][deb] = []
                fp = open('%s/void-pkg.json' % (libcdb_root, ), 'w')
                fp.write(json.dumps(arch_dict['void-pkg']))
                fp.close()
            
            # 循环添加libc
            for libc_path in libc_path_list:
                if libc_path == '':
                    continue
                add(libcdb_root, libc_path)
                libc = ELF(libc_path)
                if libc.arch not in arch_dict:
                    arch_dict[libc.arch] = dict()
                if deb not in arch_dict[ELF(libc_path).arch]:
                    arch_dict[libc.arch][deb] = []
                arch_dict[libc.arch][deb].append(libc.buildid)
                fp = open('%s/%s/build-id.json' % (libcdb_root, libc.arch), 'w')
                fp.write(json.dumps(arch_dict[libc.arch]))
                fp.close()

def _mkdir(path):
    ''' mkdir '''
    try:
        os.mkdir(path)
    except FileExistsError as e:
        if os.path.isdir(e.filename) is False:
            raise e
