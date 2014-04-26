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
    #dls_server = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
    dls_client = contactDls.ContactDls(dls_server, remote_server)
    logging.info("Local Mountpoint:%s", mountpoint)
    logging.info("Remote Server: %s", remote_server)
    logging.info("Dls Server: %s", dls_server)

    FUSE(FuseDls(mountpoint, dls_client), mountpoint, foreground=False)
    print "---- FuseDLS main ends ----"

if __name__ == "__main__":
    main()


