#!/usr/bin/python

import os

if __name__ == "__main__":
    
    status = os.system("fusermount -u /fuse_mount/dls")
    print "Umounted the fuse directory status code: ", status
    status = os.system("rm log/*")
    print "Deleted the log files"
