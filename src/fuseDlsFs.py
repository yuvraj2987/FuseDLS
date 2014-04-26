#!/usr/bin/python

from __future__ import with_statement

import os, sys, errno
import logging, time
import re
from fuse import FUSE, FuseOSError, Operations
#import contactDls
from cacheDls import Cache
import contactDls 
#################### Classes ############################

class FuseDls(Operations):
    def __init__(self, root, cache, dlsClient):
        self.root = root
        self.cache = cache
        self.dlsClient = dlsClient
        self.curPath = "/"
        self._mount()

    def _mount(self):
        logging.debug("--- mounting dls ---")
        mountResponce = self.dlsClient.do_mount()
        self.cache.add("/", contactDls.json_to_dict(mountResponce))
        fileList = mountResponce.get("files")
        for f in fileList:
            _val = contactDls.json_to_dict(f)
            _key = _val.get("name")
            logging.debug("--- add %s to cache ---"%(_key))
            self.cache.add(str(_key), _val)
        logging.debug("---- mount done ----")

    def _set_path(self, path):
        logging.debug("--------set path called -----")
        logging.debug("Original Current Path:%s", self.curPath)        
        if path.startswith("/"):
            self.curPath = path
        else:
            self.curPath += "/"+path

        logging.debug("Final current path:%s", self.curPath)

    def _responce_to_stat(self, responce):
        "Converts dls responce to stat dict"

        #st structure as per Unix standard given by stat(2) man pages
        st = {}
        for attr in ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_uid', 'st_gid',
                'st_rdev', 'st_size', 'st_blksize', 'st_blocks', 'st_atime', 'st_mtime',
                'st_ctime'):
            st.setdefault(attr, None)
        #For ends
        logging.debug("----- _responce_to_stat function starts ----")
        #dls responce keys mapping to st attributes
        #print "If File is directory: ", responce.has_key("dir")
        permission = int(responce["perms"])

        if responce["dir"]:
            logging.debug("File is directory")
            st['st_mode'] = stat.S_IFDIR
        else:
            logging.debug("File is regular file")
            st['st_mode'] = stat.S_IFREG
        
        #Set file perimissions
        st['st_mode'] |= permission
        st['st_uid'] = responce['owner']
        st['st_gid'] = responce['group']
        st['st_mtime'] = responce['mdtm']
        logging.debug("--- returning from _responce_to_stat function------------")
        return st


    ## File System calls
    def access(self, path, mode):
        logging.debug("----- filesystem access called -----")
        #dict_responce = self.dlsClient.get_responce(path)
        self._set_path(path)
        dict_responce = self.cache(self.curPath)
        if dict_responce in None:
            raise FuseOSError(errno.EACCES)
        permissions = dict_responce["perm"]
        if type(permissions) is not int:
            raise FuseOSError(errno.EACCES)
        if permissions %10 < 4:
            raise FuseOSError(errno.EACCES)


    def getattr(self, path, fh=None):
        logging.debug("---- filesystem getattr called ---")
        logging.debug("path: %s \tFile Handle:%s", path, fh)
        self._set_path(path)
        logging.debug("current path set to: %s", self.curPath)
        #dict_responce = self.dlsClient.get_responce(path)
        dict_responce = self.cache(self.curPath)
        if dict_responce is None:
            logging.debug("%s is not found in cache"%(self.curPath))
        keys = dict_responce.keys()
        logging.debug("Received keys and values")
        for key in keys:
            logging.debug("dict{%s}:%s", key, dict_responce[key])
        st = _responce_to_stat(dict_responce)
        logging.debug("---- getattr ends ----")
        return st

    def readdir(self, path, fh):
        logging.debug("----- filesystem readdir called ---")
        logging.debug("path: %s \tFile Handle:%s", path, fh)
        self._set_path(path)
        #dict_responce=self.dlsClient.get_responce(path)
        dict_responce = self.cache(self.curPath)
        dirents = [".", ".."]
        list_files = dict_responce['files']
        #f is of type dict
        for f in list_files:
            logging.debug("file:%s", f['name'])
            if f is dict:
                logging.debug("f is a dictinory")
            name = f['name']
            dirents.append(name)

        for r in dirents:
            logging.debug("file: %s", r)
            yield r

    def opendir(self, path):
        logging.debug("-------- filesystem opendir called ------")



############ Main ########################################
def main():
    print "----- FuseDLS main starts -----"
    logfile = "log/"+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))+".log"
    logging.basicConfig(filename=logfile, format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("----- Logging starts ----")
    mountpoint = "/fuse_mount/dls"
    remote_server = "ftp://ftp.freebsd.org"
    #dls_server = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
    logging.info("Local Mountpoint:%s", mountpoint)
    logging.info("Remote Server: %s", remote_server)
    logging.info("Dls Server: %s", dlsUrl)
    dls_client = contactDls.ContactDls(dlsUrl)
    _cache = Cache(dls_client.get_responce)
    FUSE(FuseDls(mountpoint, _cache, dls_client), mountpoint, foreground=False)
    print "---- FuseDLS main ends ----"

if __name__ == "__main__":
    main()


