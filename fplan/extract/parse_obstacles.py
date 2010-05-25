#!/usr/bin/python
#encoding=utf8
import parse
import re
import fplan.lib.mapper as mapper
import sys,os
import math
from parse import uprint
obsttypes=[
"Wind turbine",
"Mast",
"Cathedral",
"Pylon",
"Building",
"Platform",
"Chimney",
"Mine hoist",
"Bridge pylon",
"Crane",
"W Tower",
"Church",
"Silo",
"City Hall",
"Gasometer",
"Tower",
"Bridge pylon, 60 per minute"]

def parse_obstacles():
    p=parse.Parser("/AIP/ENR/ENR 2/ES_ENR_5_4_en.pdf",lambda x: x)
    
    res=[]    
    for pagenr in xrange(0,p.get_num_pages()):
        page=p.parse_page_to_items(pagenr)
        
        items=page.get_by_regex(r"\bDesignation\b")
        print items
        assert len(items)==1
        ay1=items[0].y1
        ay2=100        
        in_rect=page.get_fully_in_rect(0,ay1,100,100)
        lines=page.get_lines(in_rect)
        for line in lines:
            if line.strip()=="within radius 300 m.":
                continue
            if line.strip()=="": continue
            if line.startswith("AMDT"):
                continue
            if line.startswith("Area No Designation"):
                continue
            if line.startswith("ft ft Character"):
                continue
            uprint("Matching line: %s"%(line,))
            m=re.match(r"\s*(?:\d{2}N \d{2}E)?\s*\d+\s*(.*?)(\d{6}\.?\d*N)\s*(\d{7}\.?\d*E)\s*(?:\(\*\))?\s*(\d+)\s*(\d+)\s*(.*)$",
                        line)
            if m:
                name,lat,lon,height,elev,more=m.groups()                
                uprint("Found match: %s"%(m.groups(),))
                light_and_type=re.match(r"(.*?)\s*("+"|".join(obsttypes)+")",more)
                if not light_and_type:
                    raise Exception(u"Unknown obstacle type:%s"%(more,))
                light,kind=light_and_type.groups()
                res.append(
                    dict(
                        name=name,
                        pos=mapper.parse_coords(lat,lon),
                        height=height,
                        elev=elev,
                        lighting=light,
                        kind=kind
                         ))
            else:
                raise Exception("Unparsed obstacle line: %s"%(line,))                
    return res

if __name__=='__main__':
    for obst in parse_obstacles():
        print obst
 