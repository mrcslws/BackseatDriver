import requests

DESTINATION = "http://localhost:8000/"

CONTENTS = """
THIS
IS
MA
POST
"""

if __name__ == '__main__':
	requests.post(DESTINATION, data=CONTENTS)
	print "Posted to %s - %s" % (DESTINATION, CONTENTS)
