import logging, time
import contactDls

########## Global Function ###########
def add_mount_responce(cache, mountResponce, mount):
    logging.debug("---- Adding mountResponce to cache ----")
    cache.add(mount, mountResponce)
    fileList = mountResponce.get("files")
    logging.debug("File List size:%d", len(fileList))
    for f in fileList:
        logging.debug("File:%s", str(f))
        _val = contactDls.json_to_dict(f)
        _key = _val.get("name")
        cache.add(_key, _val)

    logging.debug("@@@@ Cache View @@@@\n%s", str(cache.mapping))
    logging.debug("---- mountResponce added to cache")



class Cache:

    def __init__(self, funct, maxsize=1024):
        self.org_function = funct
        self.maxsize = maxsize
        self.mapping = {}

    def get_cache(self, *args):
        mapping = self.mapping
        key = args[0] #only 1 parameters expected
        value = mapping.get(key)
        if value is not None:
            logging.debug("------ cache Hit for %s"%(str(key)))
            value = self.update_cache(key, value)
            logging.debug("vaule update_cache done")
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

    def update_cache(self, keyStr, value):
        """
            update_cache is called when path is already present in the cache
            if path is present and path is a directory and files == None then get the files from the dls
        """
        mapping = self.mapping
        logging.debug("Check if update is required")
        if value['dir'] and value['files'] is None:
            logging.debug("Update required")
            update = self.org_function(keyStr)
            logging.debug("Update responce is %s", str(update))
            logging.debug("Update values parameter")
            value['files'] = update['files']
            mapping[keyStr] = value
        else:
            logging.debug("Update not required")

        return value
        
    def add(self, *args):
        mapping = self.mapping
        key = args[0]
        value = args[1]
        logging.debug("adding %s into cache"%(key))
        mapping[key] = value
        #logging.debug("@@@@@@ Cache view @@@@@@@@@")
        #logging.debug(mapping)
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
    logging.info("----------- Cache DLS started -----------------")
    #remoteServer = "ftp://ftp.freebsd.org"
    remoteServer = "ftp.freebsd.org"
    dlsClient = contactDls.ContactDls(dlsUrl, "/fuse_mount/dls")
    cache = Cache(dlsClient.get_responce)
    mountResponce = dlsClient.do_mount()
    #print "mount responce: ", mountResponce
    logging.debug("mount responce %s", str(mountResponce))
    add_mount_responce(cache, mountResponce, "/fuse_mount/dls")
    print "-- cache added ----"
    value = cache.get_cache(remoteServer) 
    print "value returned by the cache"
    print (value)
    logging.info("----------- Cache DLS Ends --------------")

