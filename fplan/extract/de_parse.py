import re
import fplan.lib.mapper as mapper
from fplan.lib.get_terrain_elev import get_terrain_elev
import csv

def parse_airspace():
    spaces=[]
    for input in [
        "fplan/extract/denmark.airspace",
        "fplan/extract/denmark.danger.airspace",
        ]:
        lines=[unicode(x,'latin1') for x in list(open(input)) if 
               not x.startswith("#") and
               not x.startswith("FIR boundary")           
               ]
        spaces.extend(parse_space(lines))
    return spaces

def parse_space(lines):    
    idx=[0]
    out=[]
    last=[None]
    translate=dict(
        ATS='TMA',
        TIA='TMA',
        TIZ='CTR',
        TMA='TMA',
        CTR='CTR',
        DANGER="R",
        RESTRICTED="R"
        )
    try:
        def getline():
            if idx[0]==len(lines):
                raise StopIteration()
            r=lines[idx[0]]
            idx[0]+=1
            last[0]=r
            return r
        def peek():
            if idx[0]==len(lines):
                raise StopIteration()
            r=lines[idx[0]]
            return r
        def get(what):
            splat=getline().split("=")
            if len(splat)!=2:
                raise Exception("Expected <%s=?>, got <%s>"%(what,splat))
            key,val=splat
            if key!=what:
                raise Exception("Expected <%s>, got <%s>"%(what,splat))
            assert key==what
            return val.strip()
        def isnext(what):
            line=peek()
            if line.startswith(what):
                return True
            return False
        while True:
            TYPE=get("TYPE")
            freqs=[]
            if isnext("SUBTYPE"):
                SUBTYPE=get("SUBTYPE")
            else:
                SUBTYPE=None
            if isnext("REF"):
                REF=get("REF")
                if isnext("ACTIVE"):
                    getline()     
                if isnext("TITLE"):                       
                    TITLE=get("TITLE")
                else:
                    TITLE=None
                CLASS=SUBTYPE=RADIO=None
                if TYPE=="DANGER":
                    name="D-"+REF+" [2010]"
                else:
                    name=REF+" [2010]"
                type_=translate[TYPE]
            else:
                if not SUBTYPE:
                    SUBTYPE=get("SUBTYPE")                
                type_=translate[SUBTYPE]
                CLASS=get("CLASS")
                RADIO=get("RADIO")
                REF=None
                notes=[]
                while isnext("NOTES"):
                    notes.append(get("NOTES"))
                TITLE=get("TITLE")
                name=" ".join([TITLE.strip(),SUBTYPE])+" [2010]"
                for radio in [RADIO]+notes:
                    radioname,freq=re.match("(.*?)\s*(\d{3}\.\d{3}\s*(?:and)?)+",radio).groups()
                    fr=re.findall(ur"\d{3}\.\d{3}",freq)
                    for f in fr:
                        if float(f)<200.0:
                            freqs.append((radioname,float(f)))
            if isnext("BASE"):
                BASE=get("BASE")
                TOPS=get("TOPS")            
            print freqs
            points=[]
            area=[]
            while True:
                if isnext("POINT"):
                    p=get("POINT")
                    area.append(p)
                    continue
                if isnext('CLOCKWISE'):
                    radius,center,dest=re.match(ur"CLOCKWISE RADIUS=(\d+\.?\d*) CENTRE=(\d+N \d+E) TO=(\d+N \d+E)",getline()).groups()
                    area.append(ur"clockwise) along an arc with radius %s centred on %s to the point %s"%(radius,center,dest))
                    continue
                if isnext('CIRCLE'):
                    l=getline()
                    radius,center=re.match(ur"CIRCLE RADIUS=(\d+\.?\d*) CENTRE=(\d+\.?\d*N \d+\.?\d*E)",l).groups()
                    area.append("A circle with radius %s NM centred on %s"%(radius,center))
                break
            points=mapper.parse_coord_str(" - ".join(area))
            if isnext("BASE"):
                BASE=get("BASE")
                TOPS=get("TOPS")            
            
            def elev(x):
                print x
                if x=="SFC": return "GND"
                if x=="UNL": return "UNL"
                if x.lower().startswith("fl"):
                    assert x[2:].isdigit()
                    return "FL%03d"%(int(x[2:]))
                assert x.isdigit()
                return "%d ft MSL"%(int(x),)
            floor=elev(BASE)
            ceiling=elev(TOPS)
            floorint=mapper.parse_elev(floor)
            ceilint=mapper.parse_elev(ceiling)
            if floorint>9500:
                continue
            out.append(
                dict(
                     name=name,
                     floor=floor,
                     ceiling=ceiling,
                     freqs=freqs,
                     points=points,
                     type=type_
                     ))            
    except StopIteration:
        pass
    except Exception:
        print "Last parsed:",last
        raise
    else:
        raise Exception("Unexpected erorr")
    return out

def parse_airfields():
    out=[]
    for item in csv.reader(open("fplan/extract/denmark.airfields.csv")):
        print item
        icao,empty,ICAO,name,d1,d2,pos,elev,owner,phone,d4,d5=item
        if not pos[-1] in ['E','W']:
            pos=pos+"E"
        print "ICAO:",icao
        assert icao.upper()==ICAO
        name=unicode(name,"latin1")
        lat,lon=mapper.from_str(mapper.parsecoord(pos))
        nasaelev=get_terrain_elev((lat,lon))
        if elev=='':
            elev=nasaelev        
        assert abs(float(elev)-nasaelev)<50
        ad=dict(
            icao=ICAO,
            name=name,
            pos=mapper.to_str((lat,lon)),
            elev=float(elev))
        out.append(ad)
    return out
def parse_denmark():
    
    airspace=parse_airspace()
    airfields=parse_airfields()
    print "Spaces:"
    for sp in airspace:
        print "Name:",sp['name']
        print "  Points:",sp['points']
        print "  Floor:",sp['floor']
        print "  Ceil:",sp['ceiling']
        print "  Freqs:",sp['freqs']
    for field in airfields:
        print "Name:",field['name']
        print "  Pos:",field['pos']
        print "  Elev:",field['elev']
    
    return dict(
        airspace=airspace,
        airfields=airfields)
if __name__=='__main__':
    parse_denmark()
    