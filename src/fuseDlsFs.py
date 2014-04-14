#!/usr/bin/python

from __future__ import with_statement

import os, sys, errno

from fuse import FUSE, FuseOSError, Operations
import contactDls


#################### Classes ############################

class FuseDls(Operations):
    def __init__(self, root):
        self.root = root

    ## File System calls 
    def getattr(self, path, fh=None):








############ Main ########################################
def main():
    print "----- FuseDLS main starts -----"
    mountpoint = "/tmp/fuse"
    remote_server = "ftp://ftp.freebsd.org"
    dls_server = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    dls_client = contactDls.ContactDls(dls_server, remote_server)
    #responce = dls_client.get_responce("")
    #print responce
    FUSE(FuseDls(mountpoint), mountpoint, foreground=False)
    print "---- FuseDLS main ends ----"

if __name__ == "__main__":
    main()


