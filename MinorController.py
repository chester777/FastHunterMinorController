import json
import time
import urllib2

deviceInfo = {
	"deviceNo": 1,
	"deviceType": "status",
	"timestamp": time.time()
}

jsonServerUrl = "http://40.74.138.192/json.php"
deviceInfoToJson = json.dumps(deviceInfo)
headers = {
	'Content-Type': 'application/json'
}

request = urllib2.Request(jsonServerUrl, deviceInfoToJson, headers)
f = urllib2.urlopen(request)
response = f.read()

print response

f.close()