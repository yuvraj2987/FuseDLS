#!/usr/bin/env python

from errno import ENOENT
from stat import S_IFDIR, S_IFREG
from sys import argv, exit
from time import time
import logging
from fuse import FUSE, FuseOSError, Operations, fuse_get_context
#Custom modules
import cacheDls, contactDls

class FuseDLS(Operations):
    'FuseDLS for exporting Directory Listing Services a.k.a Stork Cloud Cache to Client as File System'
    
    def __init__(self, root):
        logging.info("----- Init FuseDLS FS---")
        self.root = root
        self.curpath = "/"
        dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
        self.dls = contactDls.ContactDls(dlsUrl)
        logging.debug("ContactDLS created")
        self.cache = cacheDls.Cache(self.dls.get_responce)
        logging.debug("Cache created")
        logging.debug("Mounting the DLS cache")
        mountResponce = self.dls.do_mount()
        cacheDls.add_mount_responce(self.cache, mountResponce)
        logging.debug("DLS cache mounted")
        logging.info("--------- FuseDLS Initialized ----------")
        
    # FileSystem Methods
    # -----------------------
    def getattr(self, path, fh=None):
        
        if path == '/':
            st = dict(st_mode=(S_IFDIR | 0755), st_nlink=2)
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
    logging.basicConfig(filename="log/fuseDls.log", filemode= "w", format="%(levelname)s::%(message)s", level=logging.DEBUG)
    logging.info("------------ FuseDLS Starts ---------")
    mountpoint = "/fuse_mount/dls"
    logging.info("mountpoint: %s ", mountpoint)
    fuse = FUSE(FuseDLS(mountpoint), mountpoint, foreground=False)
