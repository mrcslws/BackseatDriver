import requests
import shutil
from etw_to_nupic_input import etw_rows_to_output_file
from subprocess import check_call, Popen, PIPE
from datetime import datetime
from threading import Thread

PATH_TO_XPERF = "C:\\xperf\\xperf.exe"
SESSION_NAME = "Marcus%s" % datetime.now().isoformat()
XPERF_START_COMMAND = "%s -start %s -on Microsoft-IEFRAME -realtime -BufferSize 1024" % (PATH_TO_XPERF,SESSION_NAME)
XPERF_STOP_COMMAND = "%s -stop %s" % (PATH_TO_XPERF,SESSION_NAME)
ETWLIVELOG_COMMAND = "EtwLiveLog.exe %s" % SESSION_NAME
OUTPUT_FILENAME = "%s.csv" % SESSION_NAME.replace(":", ".")

def process_output(p):
	print "Writing events to %s" % OUTPUT_FILENAME
	etw_rows_to_output_file(p.stdout, OUTPUT_FILENAME)


def go():
	check_call(XPERF_START_COMMAND)
	p = Popen(ETWLIVELOG_COMMAND, stdout=PIPE)
	thread_storing_output = Thread(target = process_output, args = (p,))
	thread_storing_output.start()
	raw_input("Press [ENTER] to end the trace\n")
	check_call(XPERF_STOP_COMMAND)
	thread_storing_output.join()


if __name__ == '__main__':
	go()
