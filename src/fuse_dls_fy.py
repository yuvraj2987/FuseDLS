#!/usr/bin/python

# Import externam modules
import sys, os, stat, errno
import fuse
from fuse import Fuse
import contact_dls
from contact_dls import ContactDls

fuse.fuse_python_api = (0, 2)


class DLSStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0



class FuseDLSFS(Fuse):
    ' Fuse DLS FS main class to define all neccessary File System calls'
    def __init__(self, *args, **kw):
        #self.mountPoint=kw['mountpoint']
        #self.dlsClient =kw['dls']    
        Fuse.__init__(self, *args, **kw)

    def setMountPoint(self, mountpoint):
        self.root = mountpoint
    def setDlsClient(self, dlsClient):
        self.dlsClient = dlsClient
    #########
    # File System Related
    #######
    def getattr(self, path):
        responce = self.dlsClient.get_responce(path)
        if responce is None:
            return -errno.ENOENT
        st = DLSStat()
        st.st_mode= responce['perm']
        st.st_uid = responce['owner']
        st.st_gid = responce['group']
        st.st_mtime = responce['mdtm']
        return st

    def readdir(self, path, offset):
        responce = self.dlsClient.get_responce(path)
        files = responce['files']
        for dir in '.', '..', files:
            yield fuse.Direntry(dir)

    def open(self, path, flags):
        responce = self.dlsClient.get_responce(path)
        #If not a directory
        if not responce['dir']:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES



# FuseDLSFS class ends

def main():
    usage = """
    
        FS Client to Communicate with Directory Listing Service
    """+Fuse.fusage
    dlsUrl = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    remoteServer = "ftp://ftp.freebsd.org"
    dlsClient = ContactDls(dlsUrl, remoteServer)
    #server = FuseDLSFS(version="%prog " + fuse.__version__,usage=usage,dash_s_do='setsingle')
    server = FuseDLSFS(version="%prog " + fuse.__version__,usage=usage,dash_s_do='setsingle')
    server.setDlsClient(dlsClient)
    server.setMountPoint(sys.argv[1])
    server.parse(errex=1)
    server.main()
#End of main

if __name__ == '__main__':
    main()
