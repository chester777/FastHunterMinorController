import json
import time
import httplib
import urllib
import blescan
import sys
import bluetooth._bluetooth as bluez
import re
import sqlite3

macRegEx = r"[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}:[a-zA-Z0-9]{2}"
deviceUuidRegEx = r"[a-zA-Z0-9]{32}"

if __name__ == '__main__' :
	dev_id = 0
	try:
		sock = bluez.hci_open_dev(dev_id)
		print "ble thread started"

	except:
		print "error accessing bluetooth device..."
		sys.exit(1)

	blescan.hci_le_set_scan_parameters(sock)
	blescan.hci_enable_le_scan(sock)

	conn = sqlite3.connect("recvBlePacket.db")
	cur = conn.cursor()

	while True:
		returnedList = blescan.parse_events(sock, 1)
		print "----------"
		for beacon in returnedList:

			MAC_ADDR = beacon.split(",")[0]
			UUID = beacon.split(",")[1]
			MAJOR = beacon.split(",")[2]
			MINOR = beacon.split(",")[3]

			cur.execute("SELECT deviceNo, deviceName FROM deviceInfo")

			rows = cur.fetchall()
			for row in rows :
				if row != None :

					currentTime = time.time()
					cur.execute("INSERT INTO log VALUES(" + str(row[0]) + "," + str(currentTime) + "," + str(MAJOR) + "," + str(MINOR) +")")

					deviceInfo["deviceNo"] = row[0]
					deviceInfo["deviceName"] = row[1]
					deviceInfo["timestamp"]	= currentTime

					if row[0] == 1 : deviceInfo["status"] = int(MAJOR)
					elif row[0] == 2 : deviceInfo["status"] = int(MAJOR)
					elif row[0] == 3 : deviceInfo["value"] = int(MINOR)
					elif row[0] == 4 : deviceInfo["value"] = int(MINOR)
					elif row[0] == 5 : deviceInfo["value"] = int(MINOR)
					elif row[0] == 6 : deviceInfo["status"] = int(MAJOR)
					elif row[0] == 7 : deviceInfo["value"] = int(MINOR)

					jsonServerUrl = "40.74.138.192"
					deviceInfoToJson = json.dumps(deviceInfo)
					deviceInfoToJson = urllib.quote(deviceInfoToJson)

					conn = httplib.HTTPConnection(jsonServerUrl)
					conn.request("GET", "/json.php?json=" + deviceInfoToJson)
					response = conn.getresponse()

					print "packet sened to server"