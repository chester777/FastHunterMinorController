import json
import time
import httplib

deviceInfo = {
	"deviceNo": 1,
	"deviceType": "status",
	"timestamp": time.time()
}

deviceInfoToJson = json.dumps(deviceInfo)

headers = {
	"Content-type": "application/x-www-form-jsonencoded",
	"Accept": "json"
}

conn = httplib.HTTPConnection("40.74.138.192:80")
conn.request("POST", "json_get.php", deviceInfoToJson, headers)
response = conn.getresponse()

print response.status, response.reason

data = reason.read()
conn.close()