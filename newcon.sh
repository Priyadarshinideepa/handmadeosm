python3 /usr/share/sumo/tools/randomTrips.py -n handmade.net.xml -e 1000 -o handmade.trips.xml
duarouter -n handmade.net.xml --route-files handmade.trips.xml -o handmade.rou.xml --ignore-errors


