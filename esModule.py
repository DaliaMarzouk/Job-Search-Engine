from elasticsearch import Elasticsearch
from importData import *
import json
class esSearchEn:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.es = Elasticsearch([{'host': self.host, 'port': self.port}],retry_on_timeout=True)

	"""
	create a new index (data-base)
	indexName: the name of the created data-base
	"""
	def creatIndex(self,indexName):
		if self.es.indices.exists(indexName):
			res = self.es.indices.delete(index = indexName)
		request_body = {"settings" : {"number_of_shards": 1,"number_of_replicas": 0}}
		res = self.es.indices.create(index = indexName, body = request_body)

	"""
	create to index (push) a random percentage of data inside a csv file to a certain type(table) inside a certain index(data-base)
	fileName: the name of the csv file
	index: the name of the data-base
	docType: the name of the table
	percentage: number between 0 and 1 represents a random percentage of the file to be indexed
	"""
	def indexDocumentsPercentage(self, fileName, index, docType, percentage=0.1):
		docs = csvTojsonReadr(fileName, percentage) #readData
		for idx, doc in enumerate(docs):
			# print('______insert______')
			# print(json.loads(doc))
			self.es.index(index=index, doc_type=docType, id=idx, body=json.loads(doc))

	"""
	created to extract similar docs(rows) from a certain type(table) inside a certain index(data-base)
	index: the name of the data-base
	docType: the name of the table
	idsLs: a list of ids of documents to be quired
	fieldsToMatch: the fields that we should retrive similarities from them
	"""
	def retriveSimilarDocs(self, index, docType, idsLs, fieldsToMatch):
		docsList = [{"_index":index, "_type":docType, "_id":x} for x in idsLs]
		queryString = {'query':{
						"more_like_this" : {
												"fields" : fieldsToMatch,
        										"docs" : docsList,
										        "min_term_freq" : 1,
										        "max_query_terms" : 12
										     }
						}}
		# print(queryString)
		return self.es.search(index=index, body=queryString)
	
	def retriveSimlarDocs2(self, index, matchingString, fieldsToMatch):
		queryString = {"query": {
        							"more_like_this" : {
            											"fields" : fieldsToMatch,
            											"like" : matchingString,
            											"min_term_freq" : 1,
            											"max_query_terms" : 12
        											}
    							}
					}
		return self.es.search(index=index, body=queryString)

	"""created to delete a certain index(data-base)"""
	def deleteIndex(self, indexName):
		if self.es.indices.exists(indexName):
			res = self.es.indices.delete(index = indexName)
		# print(res)

	"""
	created to set mapping for a new type(table) inside index(data-base)
	fileName: the file that containes the data to be indexed
	indexName: the name of the data-base
	typeName: the name of the table
	"""
	def createMappings(self, fileName, indexName, typeName):
		fieldsName = getFieldsName(fileName)
		fieldsType = getFieldsType(fileName)
		assert len(fieldsName) == len(fieldsType), "error in readind fields' names or types"
		mappings = {}
		mapping = {}
		typeMapping = {}
		properties = {}
		for fieldIdx, fieldName in enumerate(fieldsType):
			if('float' in fieldsType[fieldIdx]):
				properties[fieldName] = {"type": "double"}
			elif('int' in fieldsType[fieldIdx]):
				properties[fieldName] = {"type": "long"}
			else:
				properties[fieldName] = {"type": "text",
										 "analyzer": "english"}
		typeMapping["properties"] = properties
		mapping[typeName] = typeMapping
		mappings["mapping"] = mapping 
		self.es.indices.create(index=indexName, ignore=400, body=mappings)

	"""
	created to search inside the index(database) for a document that exactly matches a certain criteria
	fieldsName: a list of fields to matche its values
	valuesToMatch: a list of values to match
	"""
	def findExactMatching(self,index, fieldsName, valuesToMatch):
		termDic = {}
		for idx,field in enumerate(fieldsName):
			termDic[field] = valuesToMatch[idx]
		query = {
		"query" : {
		"filter": [{"term" : termDic}]
		}
		}
		return self.es.search(index=index, body=query)

	def findExactMatching(self, index, docType, fieldsName, valuesToMatch):
		termDic = {}
		for idx,field in enumerate(fieldsName):
			termDic[field] = valuesToMatch[idx]
		query = {
		"query" : {
					"bool" : {
      							"must" : [
											{"term" : termDic},
											{"type" : {
            											"value" : docType
        											}}
        								]
        					}
				}
		}
		# print("******************************")
		# print(query)
		return self.es.search(index=index, body=query)







