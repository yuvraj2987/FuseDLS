#!/usr/bin/python


import os, sys, errno

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

    def __init__(self, dlsUrl):
        self.dls = dlsUrl
    
    def do_mount(self):
        logging.debug("--- mounting the dls server caches -----")
        payload={"domount":True}
        http_responce = requests.get(self.dls, params=payload)
        return json_to_dict(http_responce.json())

    def get_responce(self, path):
        logging.debug("---- get_responce starts -----")
        logging.debug("Passed path:%s"% (path))
        path = "ftp://"+path
        logging.debug("Appended path:%s")
        #path = self.remoteServer+path
        logging.debug("Complete path:%s"% (path))
        payload = {"URI":path}
        http_responce = requests.get(self.dls, params=payload)
        logging.debug("-------- get_responce returns responce as dict ----")
        #print (http_responce.json())
        return json_to_dict(http_responce.json())
#End of ContactDls

def main():
    print "Testing ContactDls class"
    #dlsUrl = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
    remoteServer = "ftp.freebsd.org"
    dlsClient = ContactDls(dlsUrl)
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
	
