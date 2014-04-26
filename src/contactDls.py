#!/usr/bin/python


import os, sys, errno

import requests
import logging
import stat
class ContactDls:
    ' Class to communicate with Directory Listing Service'

    def __init__(self, dlsUrl):
        self.dls = dlsUrl
    
    def _responce_to_stat(self, responce):
        "Converts dls responce to stat dict"

        #st structure as per Unix standard given by stat(2) man pages
        st = {}
        for attr in ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_uid', 'st_gid',
                'st_rdev', 'st_size', 'st_blksize', 'st_blocks', 'st_atime', 'st_mtime',
                'st_ctime'):
            st.setdefault(attr, None)
        #For ends
        logging.debug("----- _responce_to_st function starts ----")
        #dls responce keys mapping to st attributes
        #print "If File is directory: ", responce.has_key("dir")
        permission = 777
        if responce.has_key("perms"):
            permission = int(responce["perms"])

        if responce.has_key("dir") and responce["dir"]:
            logging.debug("File is directory")
            st['st_mode'] = stat.S_IFDIR
        else:
            logging.debug("File is regular file")
            st['st_mode'] = stat.S_IFREG
        
        #Set file perimissions
        st['st_mode'] |= permission
        
        if responce.has_key("owner"):
            st['st_uid'] = responce['owner']
        if responce.has_key("group"):
            st['st_gid'] = responce['group']

        if responce.has_key("mdtm"):
            st['st_mtime'] = responce['mdtm']
            
        logging.debug("--- returning from _responce_to_st---- function")
        return st


    def get_responce(self, path):
        logging.debug("---- get_responce starts -----")
        logging.debug("Passed path:%s", path)
        #path = self.remoteServer+path
        logging.debug("Complete path:%s", path)
        payload = {"URI":path}
        http_responce = requests.get(self.dls, params=payload)
        logging.debug("-------- get_responce returns responce as dict ----")
        print (http_responce.json())
        #st = self._responce_to_stat(http_responce.json())
        return http_responce.json()
        #return st
#End of ContactDls

def main():
    print "Testing ContactDls class"
    #dlsUrl = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
    remoteServer = "ftp://ftp.freebsd.org"
    dlsClient = ContactDls(dlsUrl)
    jsonResponce = dlsClient.get_responce(remoteServer)
    #print "json responce\n", jsonResponce
    print "------------------------"
    for key in jsonResponce.keys():
        print "%s\t"%(key), jsonResponce[key]
        

if __name__ == '__main__':
    main()
	
