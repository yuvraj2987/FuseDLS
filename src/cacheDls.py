import logging, time
import contactDls

class Cache:

    def __init__(self, funct, maxsize=1024):
        self.org_function = funct
        self.maxsize = maxsize
        self.mapping = {}

    def __call__(self, *args):
        mapping = self.mapping
        key = args[0] #only 1 parameters expected
        value = mapping.get(key)
        if value is not None:
            logging.debug("------ cache Hit for %s"%(str(key)))
            return value

        logging.debug("--- cache miss for %s"%(str(key)))
        value = self.org_function(key)
        mapping[str(key)] = value
        fileList = value.get("files")
        if fileList is not None:
            for f in fileList:
                _val = contactDls.json_to_dict(f)
                _key = _val.get("name")
                _key = key+"/"+_key
                mapping[str(_key)] = _val

        logging.debug("@@@@@@ Cache view @@@@@@@@@")
        logging.debug(mapping)
        return value

    def add(self, *args):
        mapping = self.mapping
        key = args[0]
        value = args[1]
        logging.debug("adding %s into cache"%(key))
        mapping[key] = value
        logging.debug("@@@@@@ Cache view @@@@@@@@@")
        logging.debug(mapping)
        return
### class ends
def tmp(key):
    if type(key) != type(str()):
        logging.debug("------- key is not string type ---", key)
    
    return key.upper()

if __name__ == "__main__":
    logfile = "log/cache.log"
    print "log file name: ", logfile
    logging.basicConfig(filename=logfile, filemode = "w", format='%(levelname)s:%(message)s', level=logging.DEBUG)
    dlsUrl = "http://didclab-ws8.cse.buffalo.edu:8080/DirectoryListingService/rest/dls/list"
    #remoteServer = "ftp://ftp.freebsd.org"
    remoteServer = "ftp.freebsd.org"
    dlsClient = contactDls.ContactDls(dlsUrl)
    cache = Cache(dlsClient.get_responce)
    mountResponce = dlsClient.do_mount()
    print "mount responce: ", mountResponce
    fileList = mountResponce.get("files")
    for f in fileList:
        _val = contactDls.json_to_dict(f)
        _key = _val.get("name")
        cache.add(_key, _val)
    print "-- cache added ----"
    value = cache(remoteServer) 
    print "value returned by the cache"
    print (value)

