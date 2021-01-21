#!/usr/bin/python3

#  Program queries status of konnected panel fetching <ip:port>/status.
#   the program returns certan values in json format
#   ip:port is given as a program argument
  
import requests 
import json
import sys


panel_status = {}
ps = {}


if len(sys.argv) == 1:
    print('No parameter. Give Konnected board IP address..')
    ps["error"] = "no parameters given"
    ps["rssi"] = "unavailable"
    panel_status = json.dumps(ps)
    sys.exit(1)
else: 
    URL = sys.argv[1] 


try:
    r = requests.get(url = URL)
    r.raise_for_status()
    
except requests.exceptions.RequestException as e:
    panel_status["error"] = str(e.args[0].reason)
    panel_status["rssi"] = "unavailable"
    panel_status["device_class"] = "signal_strength"
    panel_status["icon"] = "mdi:wifi-off"
    panel_status["unit_of_measurement"] = "dBm"  
    print(json.dumps(panel_status))
    raise SystemExit(0)


if r.status_code == 200:
    jsonr = r.json()
    p = json.dumps( jsonr )
    ps = json.loads(p)
    ps.update( {"error": str(r.status_code)} )
    
    if jsonr["rssi"] >= -30:
        ps.update( {"icon": "mdi:wifi-strength-4"} )
        
    elif jsonr["rssi"] >= -50 and jsonr["rssi"] < -30:
        ps.update( {"icon": "mdi:wifi-strength-3"} )    
        
    elif jsonr["rssi"] >= -70 and jsonr["rssi"] < -50:
        ps.update( {"icon": "mdi:wifi-strength-2"} )
    
    elif  jsonr["rssi"] >= -100 and jsonr["rssi"] < -70:
        ps.update( {"icon": "mdi:wifi-strength-1"} )
    else:
        ps.update( {"icon": "mdi:wifi-strength-outline"} )
       
    ps.update( {"device_class": "signal_strength"} )
    ps.update( {"unit_of_measurement": "dBm"} )  
    panel_status = json.dumps(ps)

print(panel_status) 