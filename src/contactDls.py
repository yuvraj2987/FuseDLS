#!/usr/bin/python


import os, sys, errno
import re
import requests
import logging


def json_to_dict(obJson):
    """ 
    Convert Json Object to standard python dictionary

    """
    py_dict = {}
    attr_list = ['files', 'group', 'name', 'perm', 'owner', 'dir', 'mdtm']
    for attr in attr_list:
        value = obJson.get(attr)
        py_dict[attr] = value
    
    if py_dict.get("perm") is None:
        py_dict["perm"] = "777"
    else:
        py_dict["perm"] = str(py_dict["perm"])

    py_dict["perm"] = int(py_dict["perm"], 8)#Convert to octal number

    logging.debug("Converted dictionary values\n%s"%str(py_dict))
    logging.debug("\n")
    return py_dict

class ContactDls:
    ' Class to communicate with Directory Listing Service'

    def __init__(self, dlsUrl, path):
        self.dls = dlsUrl
        self.mountPath = os.path.join(path)

    def __remote_path__(self, _path):
        logging.debug("--- remote path called ----")
        logging.debug("Original path:%s", _path)
        _path = re.sub(self.mountPath, "", _path, 1)
        logging.debug("Path after removing mountpoint:%s", _path)
        _path = "ftp:/"+_path
        logging.debug("Final path%s", _path)
        return _path
    
    def do_mount(self):
        try:
            logging.debug("--- mounting the dls server caches -----")
            payload={"domount":True}
            http_responce = requests.get(self.dls, params=payload, timeout=1)
            return json_to_dict(http_responce.json())
        except requests.exceptions.Timeout:
            logging.error("Could not connect to Dls server")
            

    def get_responce(self, path):
        try:
            logging.debug("---- get_responce starts -----")
            #logging.debug("Passed path:%s"% (path))
            #path = "ftp://"+path
            #logging.debug("Appended path:%s")
            #path = self.remoteServer+path
            #logging.debug("Complete path:%s"% (path))
            path = self.__remote_path__(path)
            payload = {"URI":path}
            http_responce = requests.get(self.dls, params=payload, timeout=1)
            logging.debug("-------- get_responce returns responce as dict ----")
            #print (http_responce.json())
            return json_to_dict(http_responce.json())
        except requests.exceptions.Timeout:
            logging.error("Could not connect to Dls server")
#End of ContactDls

def main():
    print "Testing ContactDls class"
    #dlsUrl = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    logging.basicConfig(filename="log/contactDls.log", filemode= "w", format="%(levelname)s::%(message)s", level=logging.DEBUG)
 
    dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
    remoteServer = "/fuse_mount/dls/ftp.freebsd.org"
    mountPath = "/fuse_mount/dls"
    dlsClient = ContactDls(dlsUrl, mountPath)
    #jsonResponce = dlsClient.get_responce(remoteServer)
    jsonResponce = dlsClient.do_mount()
    #print "json responce\n", jsonResponce
    print "------------------------"
    for key in jsonResponce.keys():
        print "%s\t"%(key), jsonResponce[key]
        
    jsonResponce = dlsClient.get_responce(remoteServer)
    print "------------------------"
    for key in jsonResponce.keys():
        print "%s\t"%(key), jsonResponce[key]
     

if __name__ == '__main__':
    main()
	
