import os
import csv
import dateutil

from nupic.frameworks.opf.modelfactory import ModelFactory
from model_params import MODEL_PARAMS
from marcus_output import MarcusFileOutput
from operator import itemgetter

import numpy
numpy.set_printoptions(threshold=numpy.nan)

IN_OUT_NAME = "TwentyGithubTabs1967_withBits"
IN_PATH = os.path.join("data", "%s.csv" % IN_OUT_NAME)
OUT_PATH = os.path.join("output", "%s.csv" % IN_OUT_NAME)

def run_experiment():
	import model_params
	model = ModelFactory.create(MODEL_PARAMS)
	model.enableInference({ "predictedField": "event" })

	with open(IN_PATH, "rb") as event_input, open(OUT_PATH, "w") as event_output:
		csv_writer = csv.writer(event_output)
		csv_writer.writerow(['timestamp', 'thread_id', 'event', 'anomalyScore', 'predictive_bits',
			'prediction1', 'likelihood1', 'prediction2', 'likelihood2'])

		csv_reader = csv.reader(event_input)
		# skip headers
		csv_reader.next()
		csv_reader.next()
		csv_reader.next()

		# the real data
		for row in csv_reader:
			timestamp = dateutil.parser.parse(row[0])
			thread_id = row[1]
			event = row[2]
			result = model.run({ "event": event, })

			tp = model._getTPRegion()
			tpOutput = tp.getSelf()._tfdr.infActiveState['t']
			patternNZ = tpOutput.reshape(-1).nonzero()[0]
			predictive_bits = numpy.array_str(patternNZ, max_line_width=1000)

			# Print to files / command line
			output_row = [timestamp, thread_id, event, result.inferences['anomalyScore'], predictive_bits]
			predictions = result.inferences['multiStepPredictions'][1]
			for prediction, likelihood in sorted(predictions.items(), key=itemgetter(1), reverse=True):
				output_row.append(prediction)
				output_row.append(likelihood)


			csv_writer.writerow(output_row)

			if csv_reader.line_num % 100 == 0:
				print 'Wrote %s lines of output...' % csv_reader.line_num


if __name__ == "__main__":
	run_experiment()
