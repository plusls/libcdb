''' manage libc database '''
import os
import shutil
import copy
import json
from libcdblib.elf import ELF

def add(libcdb_root, libc_file):
    '''add libc 
    libcdb_root: libcdb的位置
    libc_file libc的位置'''
    libcdb_root = os.path.abspath(libcdb_root)
    libc_file = os.path.abspath(libc_file)
    libc = ELF(libc_file)
    
    # init libcdb
    _mkdir(libcdb_root)
    _mkdir('%s/%s' % (libcdb_root, libc.arch))
    _mkdir('%s/%s/libcdb' % (libcdb_root, libc.arch))
    _mkdir('%s/%s/libcdb/%s' % (libcdb_root, libc.arch, libc.buildid[:2]))
    if os.path.exists('%s/%s/libcdb/%s/%s.so' % (libcdb_root, libc.arch, libc.buildid[:2], libc.buildid[2:])) is True:
        print('This libc:%s has in libc-database.' % libc.buildid)
        return
    shutil.copyfile(libc_file, '%s/%s/libcdb/%s/%s.so' % (libcdb_root, libc.arch, libc.buildid[:2], libc.buildid[2:]))

    _add_fun_offset_data(libcdb_root, libc)
    print('Add %s %s!' % (libc.arch, libc.buildid))
    

def search(libcdb_root, arch, libc_data):
    '''search libc in database
    libcdb_root: libcdb root
    libc_data: libcdata
    return the list of build-id
    for example:
        search(libcdb_root, {'system', 0xaabb, 'printf', '0xccdd'})
    '''
    addr_list = []
    for fun, addr in libc_data.items():
        addr_list.append([fun, addr])
    addr_list.sort(key=lambda addr_data: addr_data[1])
    (result, base_addr_list) = _search_by_12bit(libcdb_root, arch, addr_list[0][0], addr_list[0][1] % 0x1000)
    #print(result)
    if not result:
        return []
    base_result = copy.deepcopy(result)
    result = set()
    for base_addr in base_addr_list:
        tmp_result = copy.deepcopy(base_result)
        for i in range(1, len(addr_list)):
            tmp_result &= _search_addr(libcdb_root, arch, addr_list[i][0], addr_list[i][1] - addr_list[0][1] + base_addr)
            #print('result=', result)
            #print(tmp_result, addr_list[i][0])
        result |= tmp_result
            
    return list(result)


def delete(libcdb_root, arch, buildid):
    '''delete libc'''
    libcdb_root = os.path.abspath(libcdb_root)
    libc_file = '%s/%s/libcdb/%s/%s.so' % (libcdb_root, arch, buildid[:2], buildid[2:])
    libc = ELF(libc_file)
    _delete_fun_dir(libcdb_root, libc)
    os.remove(libc_file)
    if not os.listdir('%s/%s/libcdb/%s' % (libcdb_root, arch, buildid[:2])):
        os.rmdir('%s/%s/libcdb/%s' % (libcdb_root, arch, buildid[:2]))
    if not os.listdir('%s/%s/libcdb' % (libcdb_root, arch)):
        os.rmdir('%s/%s/libcdb' % (libcdb_root, arch))
    if not os.listdir('%s/%s' % (libcdb_root, arch)):
        os.rmdir('%s/%s' % (libcdb_root, arch))
    if not os.listdir(libcdb_root):
        os.rmdir(libcdb_root)


def _search_addr(libcdb_root, arch, fun, addr):
    ''' search addr
    '''
    result = set()
    dst_path = '%s/%s/fun/%s.json' % (libcdb_root, arch, fun)
    
    if os.path.exists(dst_path) is False:
        return result
    fp = open(dst_path, 'r')
    offset_data = json.loads(fp.read())
    fp.close()
    for fun_addr in offset_data.keys():
        if int(fun_addr, 16) == addr:
            for buildid in offset_data[fun_addr]:
                result.add(buildid)
    return result

def _search_by_12bit(libcdb_root, arch, fun, addr):
    ''' search by 12bit
    '''
    result = [set(), []]
    dst_path = '%s/%s/fun/%s.json' % (libcdb_root, arch, fun)
    
    if os.path.exists(dst_path) is False:
        return result
    fp = open(dst_path, 'r')
    offset_data = json.loads(fp.read())
    fp.close()
    
    for fun_addr in offset_data.keys():
        if int(fun_addr, 16) % 0x1000 == addr:
            result[1].append(int(fun_addr, 16))
            for buildid in offset_data[fun_addr]:
                result[0].add(buildid)
    return result

def _delete_fun_dir(libcdb_root, libc):
    ''' delete fun offset data
    '''
    for fun, addr in libc.symbols.items():
        addr_hex = '%x' % addr
        fp = open('%s/%s/fun/%s.json' % (libcdb_root, libc.arch, fun), 'r')
        offset_data = json.loads(fp.read())
        fp.close()
        offset_data[addr_hex].remove(libc.buildid)
        if not offset_data[addr_hex]:
            del offset_data[addr_hex]
        if offset_data:
            fp = open('%s/%s/fun/%s.json' % (libcdb_root, libc.arch, fun), 'w')
            fp.write(json.dumps(offset_data))
            fp.close()
        else:
            os.remove('%s/%s/fun/%s.json' % (libcdb_root, libc.arch, fun))
    if not os.listdir('%s/%s/fun' % (libcdb_root, libc.arch)):
        os.rmdir('%s/%s/fun' % (libcdb_root, libc.arch))



def _add_fun_offset_data(libcdb_root, libc):
    ''' add fun offset data
    '''
    _mkdir('%s/%s/fun' % (libcdb_root, libc.arch))

    for fun, addr in libc.symbols.items():
        try:
            fp = open('%s/%s/fun/%s.json' % (libcdb_root, libc.arch, fun), 'r')
            offset_data = json.loads(fp.read())
            fp.close()
        except FileNotFoundError:
            offset_data = dict()
        addr_hex = '%x' % addr
        if addr_hex not in offset_data:
            offset_data[addr_hex] = []
        
        # 去重
        if libc.buildid not in offset_data[addr_hex]:
            offset_data[addr_hex].append(libc.buildid)
        fp = open('%s/%s/fun/%s.json' % (libcdb_root, libc.arch, fun), 'w')
        fp.write(json.dumps(offset_data))
        fp.close()

def _mkdir(path):
    ''' mkdir '''
    try:
        os.mkdir(path)
    except FileExistsError as e:
        if os.path.isdir(e.filename) is False:
            raise e
