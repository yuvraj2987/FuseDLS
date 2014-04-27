#!/usr/bin/env python

from errno import ENOENT
from stat import S_IFDIR, S_IFREG
from sys import argv, exit
from time import time
import logging
from fuse import FUSE, FuseOSError, Operations, fuse_get_context


class FuseDLS(Operations):
    'FuseDLS for exporting Directory Listing Services a.k.a Stork Cloud Cache to Client as File System'

    def getattr(self, path, fh=None):
        uid, gid, pid = fuse_get_context()
        if path == '/':
            st = dict(st_mode=(S_IFDIR | 0755), st_nlink=2)
        elif path == '/uid':
            size = len('%s\n' % uid)
            st = dict(st_mode=(S_IFREG | 0444), st_size=size)
        elif path == '/gid':
            size = len('%s\n' % gid)
            st = dict(st_mode=(S_IFREG | 0444), st_size=size)
        elif path == '/pid':
            size = len('%s\n' % pid)
            st = dict(st_mode=(S_IFREG | 0444), st_size=size)
        else:
            raise FuseOSError(ENOENT)
        st['st_ctime'] = st['st_mtime'] = st['st_atime'] = time()
        return st


    # Disable unused operations:
    access = None
    flush = None
    getxattr = None
    listxattr = None
    open = None
    opendir = None
    release = None
    releasedir = None
    statfs = None


if __name__ == '__main__':
    
    print "--- FuseDLS FileSystem started ----"
    logging.basicConfig(filename="log/test.log", level=logging.DEBUG)
    logging.info("------------ FuseDLS Starts ---------")
    mountpoint = "/fuse_mount/dls"
    logging.info("mountpoint: %s ", mountpoint)
    fuse = FUSE(FuseDLS(), mountpoint, foreground=False, ro=True)
