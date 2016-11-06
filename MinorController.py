import json
import time
import httplib
import urllib

deviceInfo = {
	"deviceNo": 1,
	"deviceType": "status",
	"timestamp": time.time()
}

jsonServerUrl = "40.74.138.192"
deviceInfoToJson = json.dumps(deviceInfo)
deviceInfoToJson = urllib.quote

conn = httplib.HTTPConnection(jsonServerUrl)
conn.request("GET", "/json.php?json" + deviceInfoToJson)
response = conn.getresponse()

print response.read()