import shutil
import argparse
import csv
import dateutil.parser

def etw_row_to_nupic_row(etw_row):
	timestamp = dateutil.parser.parse(etw_row[0])
	thread_id = str(etw_row[1]).strip()
	provider_name = str(etw_row[2]).strip()
	task_name = str(etw_row[3]).strip()
	event_id = str(etw_row[4]).strip()
	opcode = str(etw_row[5]).strip()
	event_tuple = "(%s %s %s %s)" % (provider_name, task_name,
		event_id, opcode)
	return [timestamp, thread_id, event_tuple]

def etw_rows_to_output_file(row_stream, output_file_path):
	with open(output_file_path, "wb") as event_output:
		csv_writer = csv.writer(event_output)
		csv_writer.writerow(['timestamp', 'event'])
		csv_writer.writerow(['thread_id', 'string'])
		csv_writer.writerow(['datetime', 'string'])
		csv_writer.writerow(['', ''])

		csv_reader = csv.reader(row_stream)
		for row in csv_reader:
			csv_writer.writerow(etw_row_to_nupic_row(row))

def etw_file_to_output_file(input_file_path, output_file_path):
	etw_rows_to_output_file(open(args.inpath, "rb"), output_file_path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=
		'Reformat EtwLiveLog.exe output for NuPIC consumption')
	parser.add_argument('inpath', type=str, help='Path to the input file')
	parser.add_argument('outpath', type=str, help='Path to the output file')
	args = parser.parse_args()
	etw_file_to_output_file(args.inpath, args.outpath)
