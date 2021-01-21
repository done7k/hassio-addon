## 
import requests 
import json
#import datetime
import sys
#from bs4 import BeautifulSoup


panel_status = {}
ps = {}
#    "rssi": -120,
#    "error": 0,
#}

if len(sys.argv) == 1:
    print('No parameter. Give Konnected board IP address..')
    ps["error"] = "no parameters"
    ps["rssi"] = -120
    panel_status = json.dumps(ps)
    sys.exit(1)
else: 
    URL = sys.argv[1] 


try:
    r = requests.get(url = URL)
    r.raise_for_status()
    
except requests.exceptions.RequestException as e:
#    raise SystemExit(dir(e.args[0].reason))
#    raise SystemExit(e.args[0].reason.str)
    panel_status["error"] = str(e.args[0].reason)
    panel_status["rssi"] = -120
    print(json.dumps(panel_status))
    raise SystemExit(0)
#    print(e)



if r.status_code == 200:
    jsonr = r.json()
    p = json.dumps( jsonr )
    ps = json.loads(p)
    ps.update( {"error": str(r.status_code)} )
    panel_status = json.dumps(ps)

print(panel_status) 