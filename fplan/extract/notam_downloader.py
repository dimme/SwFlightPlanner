from time import sleep
import os
import urllib2
import random
from datetime import datetime

def download_notam():
    notamlist=[fname for fname in os.listdir("notams") if fname.isdigit() ]
    if len(notamlist)>0:    
        last=max(notamlist)
        print "Last notam"
        assert int(last)>=0
        lasttext=open("notams/%s"%(last,),"r").read()
    else:
        last=0
        lasttext=""       
    
    nextnotam=int(last)+1
    all_notams_but_seldom_updated=urllib2.urlopen(
                          "http://www.lfv.se/AISInfo.asp?TextFile=odinesaa.txt&SubTitle=&T=SWEDEN&Frequency=250").read()
    north=urllib2.urlopen("http://www.lfv.se/AISInfo.asp?TextFile=odinesun.txt&SubTitle=&T=SWEDEN%20-%20North&Frequency=250").read()
    mid=urllib2.urlopen(  "http://www.lfv.se/AISInfo.asp?TextFile=odinesos.txt&SubTitle=&T=SWEDEN%20-%20Middle&Frequency=250").read()
    south=urllib2.urlopen("http://www.lfv.se/AISInfo.asp?TextFile=odinesmm.txt&SubTitle=&T=SWEDEN%20-%20South&Frequency=250").read()
    
    finland_n=urllib2.urlopen("http://www.lfv.se/AISInfo.asp?TextFile=odinefps.txt&SubTitle=&T=Finland%20N&Frequency=250").read()
    finland_s=urllib2.urlopen("http://www.lfv.se/AISInfo.asp?TextFile=odinefes.txt&SubTitle=&T=Finland%20S&Frequency=250").read()
    finland_all=urllib2.urlopen("http://www.lfv.se/AISInfo.asp?TextFile=odinefin.txt&SubTitle=&T=Finland&Frequency=250").read()
    
    text="\n".join([north,mid,south,
        all_notams_but_seldom_updated,
        finland_n,finland_s,finland_all
        ])
    
    outfile="notams/%08d"%(nextnotam,)
    if lasttext!=text:        
        f=open(outfile,"w")
        f.write(text)
        f.close()    
        print "Downloaded notam (%d bytes) did differ from last stored (%d bytes)"%(len(text),len(lasttext))
        ret=os.system("fplan/lib/notam_db_update.py %s 1"%(outfile,))
        if ret:
            raise Exception("notam_db_update failed: %s"%(ret,))
    else:
        print "Downloaded notam (%d bytes) did not differ from last stored"%(len(text,))

def download_notams():
    if not os.path.exists("notams"):
        os.makedirs("notams")
    while True:
        try:
            download_notam()
        except Exception,cause:
            print "download failed:",cause
            raise
        print "Time now",datetime.utcnow()
        sleep(random.randrange(9000,10000))        
    


if __name__=="__main__":
    download_notams()
    
