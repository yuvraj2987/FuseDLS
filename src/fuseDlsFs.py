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

    ## File System calls 
    def getattr(self, path, fh=None):
        logging.debug("---- getattr called ---")
        logging.debug("path: %s \tFile Handle:%s", path, fh)
        logging.debug("---- getattr ends ----")
        dict_responce = dlsClient.get_responce(path)
        logging.debug("Responce from Dls: %s", dict_responce)




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


