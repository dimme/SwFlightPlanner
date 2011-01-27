import struct
import fplan.lib.mapper as mapper
from datetime import datetime
from fplanquick.fplanquick import decode_flightpath
from fplan.model import Recording

def parseRecordedTrip(user,inp,headers_only=False):
	
	def readShort():
		return struct.unpack(">H",inp.read(2))[0]
	def readInt():
		return struct.unpack(">I",inp.read(4))[0]
	def readLong():
		return struct.unpack(">Q",inp.read(8))[0]
	def readUTF():
		len=readShort()
		print "Read string of length %d"%(len,)
		data=inp.read(len)
		return unicode(data,"utf8")
	
	magic=readInt()
	print "magic",magic
	print "magic:",hex(magic)
	if magic!=0xfafafa01:
		raise Exception("Bad magic in uploaded file")
	version=readInt()
	if version!=2:
		raise Exception("Version not even supported by server:"+version)
	departure=readUTF()
	destination=readUTF()
	"""
	startpos=mapper.merc2latlon((readInt(),readInt()),17)
	startstamp=readLong()
	endpos=mapper.merc2latlon((readInt(),readInt()),17)
	lasthdg=readInt()
	print "lasthdg:",lasthdg
	lastrate=readInt()
	lastturn=readInt()
	laststamp=readLong()
	print datetime.utcfromtimestamp(laststamp/1000.0)
	laststampdelta=readInt()
	finished=readInt()
	print "finished",finished
	distance_milli=readLong()
	distance=distance_milli/1000.0
	print "Distance: %.1fNM"%(distance,)
	if not headers_only:
		binary=inp.read()
		print "Read binary of size ",len(binary)
		path=decode_flightpath(binary,version)
	else:
		path=None
	"""
	buf=inp.read()
	print "Read %d bytes to parse using c++ optimized triplog decoding routine"%(len(buf),)
	path=decode_flightpath(buf,version)
	startstamp=path['startstamp']
	endstamp=path['endstamp']
	startpos=path['startpos']
	endpos=path['endpos']
	distance=path['distance']
	path=path['path']
	print "uploaded stamp:",startstamp
	rec=Recording(user,datetime.utcfromtimestamp(startstamp/1000.0))
	rec.end=datetime.utcfromtimestamp(endstamp/1000.0)
	rec.duration=float(endstamp-startstamp)
	rec.distance=distance
	rec.depdescr=departure
	rec.destdescr=destination
	rec.trip=buf
						
	return rec				
				
"""
				start17.serialize(data);
				data.writeLong(startstamp);
				last17.serialize(data);
				data.writeInt(lasthdg);
				data.writeInt(lastrate);
				data.writeInt(lastturn);
				data.writeLong(laststamp);
				data.writeInt(laststampdelta);
				data.writeInt(finished ? 1 : 0);
				data.writeLong(distance_millinm);
				binbuf.serialize(data);
			
				data.flush();
				data.close();
	"""
