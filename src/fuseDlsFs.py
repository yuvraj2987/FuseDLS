#!/usr/bin/env python

from errno import ENOENT
#from stat import S_IFDIR, S_IFREG
import stat
from sys import argv, exit
import time
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
    #End of __init__
    def _convert_to_stat(self, responce):
        logging.debug("Get stat values")
        st = dict()
        if responce['dir']:
            logging.debug("%s is directory", responce['name'])
            st['st_mode'] = stat.S_IFDIR
            st['st_nlink'] = 2
        else:
            logging.debug("%s is file", responce['name'])
            st['st_mode'] = stat.S_IFREG
        
        st['st_mode'] = (st['st_mode'] | responce['perm'])
        st['st_ctime'] = st['st_mtime'] = st['st_atime'] = time.time()
        return st 

    # FileSystem Methods
    # -----------------------
    def getattr(self, path, fh=None):
        logging.debug("------- getattr called --------")
        logging.debug("Original path:%s", path)
        """if path == '/':
            st = dict(st_mode=(stat.S_IFDIR | 0755), st_nlink=2)
            st['st_ctime'] = st['st_mtime'] = st['st_atime'] = time.time()
        else:"""
        #raise FuseOSError(ENOENT)
        result = self.cache.get_cache(path)
        st = self._convert_to_stat(result)
        logging.debug("Stat for %s is %s", path, str(st))
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
