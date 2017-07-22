from esModule import esSearchEn
class jobSearchEngine:
	def __init__(self, indexName, postsFileName, applicationsFileName, postsTypeName, applicationsTypeName):
		self.indexName = indexName
		self.postsTypeName = postsTypeName
		self.applicationsTypeName = applicationsTypeName
		self.postsFileName = postsFileName
		self.applicationsFileName = applicationsFileName
		self.esEn = esSearchEn(host='localhost', port='9200')

	def loadHistory(self, deletePreviousHistory=False, postsPercentage=0.1, applicationsPercentage=0.1):
		#1- Delete previous History
		# if(deletePreviousHistory): self.esEn.deleteIndex(self.indexName)
		#2- create an index
		self.esEn.creatIndex(self.indexName)
		#3- create posts type mapping
		print("______________________________________")
		print("Create Mapping for posts type")
		print("______________________________________")
		self.esEn.createMappings(fileName=self.postsFileName, indexName=self.indexName, typeName=self.postsTypeName)
		#4- create applications type mapping
		print("______________________________________")
		print("Create Mapping for applications type")
		print("______________________________________")
		self.esEn.createMappings(fileName=self.applicationsFileName, indexName=self.indexName, typeName=self.applicationsTypeName)
		#5- index 0.1 of posts' history
		print("______________________________________")
		print("Index posts")
		print("______________________________________")
		self.esEn.indexDocumentsPercentage(fileName=self.postsFileName, index=self.indexName, docType=self.postsTypeName, percentage=postsPercentage)
		#6- index 0.1 of applications' history
		print("______________________________________")
		print("index applications")
		print("______________________________________")
		self.esEn.indexDocumentsPercentage(fileName=self.applicationsFileName, index=self.indexName, docType=self.applicationsTypeName, percentage=applicationsPercentage)

	def getOtherApplications(self, user_id):
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.applicationsTypeName, fieldsName=["user_id"], valuesToMatch=[user_id])
		retrivedDocs = result["hits"]["hits"]
		appliedJobs = [x["_source"]["job_id"] for x in retrivedDocs]
		return appliedJobs

	def showApplicants(self, job_id):
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.applicationsTypeName, fieldsName=["job_id"], valuesToMatch=[job_id])
		# print(result)
		retrivedDocs = result["hits"]["hits"]
		applicants = [x["_source"]["user_id"] for x in retrivedDocs]
		return applicants

	def getJobIDofApp(self, app_id):
		# print ("app_id: ",app_id)
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.applicationsTypeName, fieldsName=["id"], valuesToMatch=[app_id])
		# print(result)
		job_id = result["hits"]["hits"]
		if(len(job_id)>0):
			job_id = job_id[0]["_source"]["job_id"]
		else:
			job_id = None
		
		return job_id

	def getUserIDofApp(self, app_id):
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.applicationsTypeName, fieldsName=["id"], valuesToMatch=[app_id])
		# print result
		user_id = result["hits"]["hits"]
		if(len(user_id)>0):
			user_id = user_id[0]["_source"]["user_id"]
		else:
			user_id = None
		return user_id

	def recommendFurtherJobs(self, app_id):
		#1- get job_id
		job_id = self.getJobIDofApp(app_id)
		# print(job_id)
		#2- get job_post Doc id in postsType
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.postsTypeName, fieldsName=["id"], valuesToMatch=[job_id])
		retrivedDoc = result["hits"]["hits"]
		# print(retrivedDoc)
		docID = retrivedDoc[0]["_id"]
		#3- get similarDocuments
		similarretrivedDocsRes = self.esEn.retriveSimilarDocs(index=self.indexName, docType=self.postsTypeName, idsLs=[docID], fieldsToMatch=["job_title","job_description","job_requirements"])
		similarJobs = [x["_source"] for x in similarretrivedDocsRes["hits"]["hits"]]
		# print similarJobs
		return [{"id": x["id"], "job_title":x["job_title"]} for x in similarJobs]

	def recommendJobSeekers(self, job_id):
		#1- retrive similar jobs
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.postsTypeName, fieldsName=["id"], valuesToMatch=[job_id])
		retrivedDoc = result["hits"]["hits"]
		# print(retrivedDoc)
		docID = retrivedDoc[0]["_id"]
		similarretrivedDocsRes = self.esEn.retriveSimilarDocs(index=self.indexName, docType=self.postsTypeName, idsLs=[docID], fieldsToMatch=["job_title","job_description","job_requirements"])
		similarJobs = [x["_source"] for x in similarretrivedDocsRes["hits"]["hits"]]
		similarJobs = [{"id": x["id"], "job_title":x["job_title"]} for x in similarJobs]
		recommendedApplicants = set()
		for job in similarJobs:
			# print(self.showApplicants(job["id"]))
			recommendedApplicants = recommendedApplicants.union(set(self.showApplicants(job["id"])))
			# print(recommendedApplicants)
		return list(recommendedApplicants)

	def jobSearch(self, searchingString):
		searcgRes = self.esEn.retriveSimlarDocs2(index=self.indexName, matchingString=searchingString, fieldsToMatch=["job_title","job_description","job_requirements"])
		resultedJobs = [x["_source"] for x in searcgRes["hits"]["hits"]]
		return [{"id": x["id"], "job_title":x["job_title"]} for x in resultedJobs]

	def evaluateJobSearch(self, user_id, recomendedJobs):
		#1- get the actual applied for jobs
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.applicationsTypeName, fieldsName=["user_id"], valuesToMatch=[user_id])
		applications = [x["_source"] for x in result["hits"]["hits"]]
		applications = [{"id": x["id"], "job_title": x["job_title"]} for x in applications]
		intersection = set(recomendedJobs).intersection(set(applications))
		percision = float(len(intersection))/float(len(recomendedJobs))
		recall = float(len(intersection))/float(len(applications))
		return {"percision":percision, "recall":recall}

	def evaluateRecommendedJobSeekers(self, job_id, recommendedApplicants):
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.applicationsTypeName, fieldsName=["job_id"], valuesToMatch=[job_id])
		applicants = [x["_source"] for x in result["hits"]["hits"]]
		applicants = [x["user_id"] for x in applicants]
		intersection = set(applicants).intersection(set(recommendedApplicants))
		percision = float(len(intersection))/float(len(recommendedApplicants))
		recall = float(len(intersection))/float(len(applicants))
		return {"percision":percision, "recall":recall}

	def evaluateRecommededJobs(self, app_id, recomendedJobs):
		user_id = self.getUserIDofApp(app_id)
		# print user_id
		result = self.esEn.findExactMatching(index=self.indexName, docType=self.applicationsTypeName, fieldsName=["user_id"], valuesToMatch=[user_id])
		applications = [x["_source"] for x in result["hits"]["hits"]]
		applications = [ x["id"] for x in applications]
		recomendedJobs = [x["id"] for x in recomendedJobs]
		intersection = set(applications).intersection(set(recomendedJobs))
		percision = float(len(intersection))/float(len(recomendedJobs))
		recall = float(len(intersection))/float(len(applications))
		return {"percision":percision, "recall":recall}



