SWARM_CONFIG = {
	"includedFields": [
		{
			"fieldName": "timestamp",
			"fieldType": "datetime",
		},
		{
			"fieldName": "thread_id",
			"fieldType": "string",
		},
		{
			"fieldName": "event",
			"fieldType": "string",
	    },
	],
	"streamDef": {
		"info": "event",
		"version": 1,
		"streams": [
			{
				"info": "TwentyGithubTabs1967",
				"source": "file://data/TwentyGithubTabs1967.csv",
				"columns": [
					"*"
				]
			}
		]
	},
	"inferenceType": "TemporalAnomaly",
	"inferenceArgs": {
		"predictionSteps": [
			1
		],
		"predictedField": "event"
	},
	"swarmSize": "medium"
}


import os
import shutil
from nupic.swarming import permutations_runner

def swarm_over_data(swarm_config):
	permutations_runner.runWithConfig(swarm_config, {'maxWorkers': 1, 'overwrite': True})
	shutil.copyfile("model_0/model_params.py", "model_params.py")

if __name__ == "__main__":
	swarm_over_data(SWARM_CONFIG)
