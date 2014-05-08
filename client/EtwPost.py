import requests
from subprocess import Popen, PIPE
from datetime import datetime, timedelta

# Use this for live-streaming events to the server for online learning.
# I haven't consumed this yet.

DESTINATION = "http://localhost:8000/"

if __name__ == '__main__':
	p = Popen("EtwLiveLog.exe MarcusRealtime", stdout=PIPE)

	burstperiod = timedelta(seconds=2)
	currentburstcontents = ""
	nextbursttimestamp = datetime.now() + burstperiod

	for outputline in p.stdout:
		currentburstcontents += outputline

		if datetime.now() > nextbursttimestamp:
			requests.post(DESTINATION, data=currentburstcontents)
			print "Posted to %s" % currentburstcontents
			print "BEGIN BURST"
			print currentburstcontents
			print "END BURST"
			nextbursttimestamp = datetime.now() + burstperiod
			currentburstcontents = ""
