#!/usr/bin/python

import requests

class ContactDls:
    ' Class to communicate with Directory Listing Service'

    def __init__(self, dlsUrl, serverUrl):
        self.dls = dlsUrl
        self.remoteServer = serverUrl

    def get_responce(self, path):
        path = self.remoteServer+path
        payload = {"URI":path}
        http_responce = requests.get(self.dls, params=payload)
        return http_responce.json()
#End of ContactDls

def main():
    print "Testing ContactDls class"
    dlsUrl = "http://ec2-184-73-223-158.compute-1.amazonaws.com:8080/DirectoryListingService/rest/dls/list"
    remoteServer = "ftp://ftp.freebsd.org"
    dlsClient = ContactDls(dlsUrl, remoteServer)
    jsonResponce = dlsClient.get_responce("")
    print "json responce\n", jsonResponce


if __name__ == '__main__':
    main()
	
