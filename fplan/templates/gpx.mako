<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="flightplanner" version="1.1">
  <rte>
    <name>${c.trip}</name>
    <cmt>${c.trip}</cmt>
    <desc>${c.trip}</desc>
    %for wp in c.waypoints:
    <rtept lat="${wp['lat']}" lon="${wp['lon']}">
      <name>${wp['name']}</name>
      <cmt>${wp['name']}</cmt>
      <desc>${wp['name']}</desc>
    </rtept>
    %endfor
  </rte>
</gpx>

