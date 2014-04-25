#!/usr/bin/python

from __future__ import with_statement

import os, sys, errno
import logging, time
from fuse import FUSE, FuseOSError, Operations
import contactDls


#################### Classes ############################

class FuseDls(Operations):
    def __init__(self, root, dls):
        self.root = root
        self.dlsClient = dls
        self.curPath = "/"

    def _full_path(self, partial):
        logging.debug("-------- get full path called -----")

    def _responce_to_stat(self, responce):
        "Converts dls responce to stat dict"

        #stat structure as per Unix standard given by stat(2) man pages
        stat = {}
        for attr in ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_uid', 'st_gid',
                'st_rdev', 'st_size', 'st_blksize', 'st_blocks', 'st_atime', 'st_mtime',
                'st_ctime'):
            stat.setdefault(attr, None)
        #For ends
        logging.debug("----- _responce_to_stat function starts ----")
        #dls responce keys mapping to stat attributes
        if responce.has_key("dir") and responce[dir]:
            logging.debug("File is directory")
            stat['st_mode'] = os.stat.S_ISDIR
        else:
            logging.debug("File is regular file")
            stat['st_mode'] = os.stat.S_ISREG

        if responce.has_key("owner"):
            stat['st_uid'] = responce['owner']
        if responce.has_key("group"):
            stat['st_gid'] = responce['group']

        if responce.has_key("mdtm"):
            stat['st_mtime'] = responce['mdtm']
            
        logging.debug("--- returning from _responce_to_stat---- function")


    ## File System calls
    def access(self, path, mode):
        logging.debug("----- access called -----")
        dict_responce = self.dlsClient.get_responce(path)
        if dict_responce in None:
            raise FuseOSError(errno.EACCES)

    def getattr(self, path, fh=None):
        logging.debug("---- getattr called ---")
        logging.debug("path: %s \tFile Handle:%s", path, fh)
        dict_responce = self.dlsClient.get_responce(path)
        keys = dict_responce.keys()
        logging.debug("Received keys and values")
        for key in keys:
            logging.debug("dict{%s}:%s", key, dict_responce[key])
        st = _responce_to_stat(dict_responce)
        logging.debug("---- getattr ends ----")
        return st

    def readdir(self, path, fh):
        logging.debug("----- readdir called ---")
        logging.debug("path: %s \tFile Handle:%s", path, fh)
        dict_responce=self.dlsClient.get_responce(path)
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

    def opendir

############ Main ########################################
def main():
    print "----- FuseDLS main starts -----"
    logfile = "log/"+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))+".log"
    logging.basicConfig(filename=logfile, format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("----- Logging starts ----")
    mountpoint = "/tmp/fuse"
    remote_server = "ftp://ftp.freebsd.org"
    dls_server = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    dls_client = contactDls.ContactDls(dls_server, remote_server)
    logging.info("Local Mountpoint:%s", mountpoint)
    logging.info("Remote Server: %s", remote_server)
    logging.info("Dls Server: %s", dls_server)

    FUSE(FuseDls(mountpoint, dls_client), mountpoint, foreground=False)
    print "---- FuseDLS main ends ----"

if __name__ == "__main__":
    main()


