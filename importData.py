"""
created to take a csvFile and return its data in form of json generator in an optimized way
fileName: the name of the csv file from which the data is imported
samplesSize: the percentage of read data
"""
def csvTojsonReadr(fileName, samplesSize=0.5):
	import pandas as pd
	import json
	import random
	if(samplesSize>1 or samplesSize<=0): raise ValueError("sampleSize should be a percentage between 0 and 1")
	chunkSize = 500
	chunkNo = 0
	#read the csvFile in chunks
	chunks = pd.read_csv(fileName, chunksize=chunkSize)
	for chunk in chunks:
		chunk = chunk.where((chunk.notnull()), None)
		#generate random indecies
		ids = []
		if(samplesSize==1):
			ids = list(range(chunkSize))
			random.shuffle(ids)
		else:
			ids = random.sample(range(1, chunkSize), int(chunkSize*samplesSize))
		cols = chunk.columns
		# print cols
		# print ids
		for idx in ids:
			try:
				yield json.dumps({colName:chunk[colName][idx+chunkNo*chunkSize] for colName in cols})
			except:
				return
		chunkNo = chunkNo + 1

"""
created to return the columns types indes a csv file in the most effeicient way in terms of memory and time
fileName: the name of the csv file
"""
def getFieldsType(fileName):
	import pandas as pd
	df = pd.read_csv(fileName, chunksize=1)
	for chunk in df:
		cols = chunk.columns
		return [(type(chunk[name][0])).__name__ for name in cols]

"""
created to return the columns names indes a csv file in the most effeicient way in terms of memory and time
fileName: the name of the csv file
"""
def getFieldsName(fileName):
	import pandas as pd
	df = pd.read_csv(fileName, chunksize=1)
	for chunk in df:
		return chunk.columns