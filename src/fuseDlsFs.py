#!/usr/bin/env python

import errno, stat, os
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
        self.root = os.path.join(root)
        self.curpath = self.root
        dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
        self.dls = contactDls.ContactDls(dlsUrl, self.root)
        logging.debug("ContactDLS created")
        self.cache = cacheDls.Cache(self.dls.get_responce)
        logging.debug("Cache created")
        self.__mount__()

    def __mount__(self):
        logging.debug("-------- Mount Called ---------")
        logging.debug("Mounting the DLS cache")
        mountResponce = self.dls.do_mount()
        path = os.path.join(self.root, "")
        cacheDls.add_mount_responce(self.cache, mountResponce, path)
        logging.debug("DLS cache mounted")
        logging.info("--------- FuseDLS Initialized ----------")

    def _full_path(self, partial):
        logging.debug("------- Full path called --------")
        logging.debug("Passed path: %s", partial)
        if partial == "/":
            logging.debug("Partial is current dir")
            partial = ""
        elif partial.startswith("/"):
            logging.debug("Partial starts with /")
            partial = partial[1:]
        logging.debug("Create full os path")
        path = os.path.join(self.root, partial)
        logging.debug("Full path: %s", path)
        return path

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
        path = self._full_path(path)
        """if path == '/':
            st = dict(st_mode=(stat.S_IFDIR | 0755), st_nlink=2)
            st['st_ctime'] = st['st_mtime'] = st['st_atime'] = time.time()
        else:"""
        #raise FuseOSError(ENOENT)
        result = self.cache.get_cache(path)
        st = self._convert_to_stat(result)
        logging.debug("Stat for %s is %s", path, str(st))
        return st

    def readdir(self, path, fh):
        logging.debug("----- readdir called ------")
        path = self._full_path(path)
        result = self.cache.get_cache(path)
        if not result['dir']:
            raise FuseOSError(errno.EBADF)
        dirents = ['.', '..']
        fileList = result.get('files')
        for f in fileList:
            fileName = f.get('name')
            logging.debug("file: %s is directory? %s", fileName, f.get('dir'))
            if f.get('dir'):
                dirents.append(fileName)
        #End of for
        logging.debug("Dirents list: %s", str(dirents))
        return dirents

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
    fuse = FUSE(FuseDLS(mountpoint), mountpoint, foreground=False, nothreads=True)
