''' add libc to database '''
import os
import shutil

from libcdblib.elf import ELF

def add_libc(libcdb_root, libc_file):
    '''add libc 
    libcdb_root: libcdb的位置
    libc_file libc的位置'''
    libcdb_root = os.path.abspath(libcdb_root)
    libc_file = os.path.abspath(libc_file)
    libc = ELF(libc_file)
    
    # init libcdb
    _mkdir(libcdb_root)
    _mkdir(libcdb_root + '/libcdb')

    _mkdir('%s/libcdb/%s' % (libcdb_root, libc.buildid[:2]))
    shutil.copyfile(libc_file, '%s/libcdb/%s/%s.so' % (libcdb_root, libc.buildid[:2], libc.buildid[2:]))

    _build_fun_dir(libcdb_root, libc)


def _build_fun_dir(libcdb_root, libc):
    ''' build fun dir
    '''
    _mkdir(libcdb_root + '/fun')
    for fun, addr in libc.symbols.items():
        _mkdir('%s/fun/%s' % (libcdb_root, fun))
        _mkdir('%s/fun/%s/%x' % (libcdb_root, fun, addr))
        dst_file = '%s/fun/%s/%x/%s.so' % (libcdb_root, fun, addr, libc.buildid)
        source_file = '../../../libcdb/%s/%s.so' % (libc.buildid[:2], libc.buildid[2:])
        if  os.path.exists(dst_file) is True:
            os.remove(dst_file)
        os.symlink(source_file, dst_file)

def _mkdir(path):
    ''' mkdir '''
    try:
        os.mkdir(path)
        #print('mkdir:%s' % path)
    except FileExistsError as e:
        if os.path.isdir(e.filename) is False:
            raise e
