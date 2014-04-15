#!/usr/bin/python

import requests
import logging
class ContactDls:
    ' Class to communicate with Directory Listing Service'

    def __init__(self, dlsUrl, serverUrl):
        self.dls = dlsUrl
        self.remoteServer = serverUrl

    def get_responce(self, path):
        logging.debug("---- get_responce starts -----")
        logging.debug("Passed path:%s", path)
        path = self.remoteServer+path
        logging.debug("Complete path:%s", path)
        payload = {"URI":path}
        http_responce = requests.get(self.dls, params=payload)
        logging.debug("-------- get_responce returns responce as dict ----")
        return http_responce.json()
#End of ContactDls

def main():
    print "Testing ContactDls class"
    dlsUrl = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    remoteServer = "ftp://ftp.freebsd.org"
    dlsClient = ContactDls(dlsUrl, remoteServer)
    jsonResponce = dlsClient.get_responce("")
    print "json responce\n", jsonResponce
    print "-----------------------"
    print "json key and values"
    for key in jsonResponce.keys():
        print "%s:\t"%(key), jsonResponce[key]

if __name__ == '__main__':
    main()
	
