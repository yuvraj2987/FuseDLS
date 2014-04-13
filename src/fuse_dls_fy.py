#!/usr/bin/python

# Import externam modules
import os, stat, errno
import fuse
from fuse import Fuse

fuse.fuse_python_api = (0, 2)

class FuseDLSFS(Fuse):
    ' Fuse DLS FS main class to define all neccessary File System calls'

    def readdir(self, path, offset):
        for r in '.', '..', 'hello':
            yield fuse.Direntry(r)


# FuseDLSFS class ends

def main():
    usage = """
    
        FS Client to Communicate with Directory Listing Service
    """
    server = FuseDLSFS(version="%prog " + fuse.__version__,usage=usage,dash_s_do='setsingle')
    server.parse(errex=1)
    server.main()
#End of main

if __name__ == '__main__':
    main()
