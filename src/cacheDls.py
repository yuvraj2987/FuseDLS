import logging, time

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
        return value
### class ends
def tmp(key):
    if type(key) != type(str()):
        logging.debug("------- key is not string type ---", key)
    
    return key.upper()

if __name__ == "__main__":
    logfile = "log/"+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))+".log"
    logging.basicConfig(filename=logfile, format='%(levelname)s:%(message)s', level=logging.DEBUG)

    cache = Cache(tmp)
    for c in ["pub", "linux", "pub"]:
        print (c, cache(c))
    


