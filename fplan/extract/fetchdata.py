#!/usr/bin/python
import os
from datetime import datetime

def get_filedate(path):
    return datetime.fromtimestamp(os.path.getmtime(path))

def stripname(path):
    out=[]
    for c in path:
        if c.isalnum():
            out.append(c)
        else:
            out.append("_")
    return "".join(out)
def changeext(path,from_,to_):
    assert path.endswith(from_)
    path=path[:-len(from_)]
    return path+to_

def get_date(path):
    return get_filedate('/home/anders/lfv/www.lfv.se'+path)
def getrawdata(relpath):
    assert(relpath.startswith("/"))
    return open('/home/anders/lfv/www.lfv.se'+relpath).read()
    

def getxml(relpath):
    assert relpath.startswith("/")
    
    filedate=get_date(relpath)
    cachenamepdf="/tmp/lfv/"+stripname(relpath)
    cachenamexml="/tmp/lfv/"+stripname(relpath)+".xml"
    if os.path.exists(cachenamexml):
        cacheddate=get_filedate(cachenamexml)
        if cacheddate==filedate:
            print "Returning cached %s"%(relpath,)
            return open(cachenamexml).read()
    
    pdfdata=getrawdata(relpath)
    open(cachenamepdf,"w").write(pdfdata)
    if os.system("pdftohtml -xml -nodrm "+cachenamepdf)!=0:
        raise Exception("pdftohtml failed!")
    
    
    modt=int(filedate.strftime('%s'))
    os.utime(cachenamexml,(modt,modt))
    return open(cachenamexml).read() 


