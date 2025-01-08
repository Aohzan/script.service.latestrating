LOGDEBUG = 0
LOGINFO = 1
LOGWARNING = 2
LOGERROR = 3

def log(msg, level=LOGINFO):
    print(f"MOCK XBMC LOG: {msg}")

def sleep(ms):
    pass

def executeJSONRPC(command):
    return '{"result": {"movies": [], "tvshows": []}}'

def getCondVisibility(condition):
    return True

def translatePath(path):
    return path 