from jobSearchEngine import jobSearchEngine

user_id='76fa79b1'
job_id="e9b78c6e"
app_id ="8411d41f"#"id": "8411d41f"
searchingString = "web development"
postsFileName = "wuzzuf-job-posts-2014-2016/Wuzzuf_Job_Posts_Sample.csv"
applicationsFileName = "wuzzuf-job-posts-2014-2016/Wuzzuf_Applications_Sample.csv"

#Intialize the JSE
sEng = jobSearchEngine(indexName='wuzzuf', postsFileName=postsFileName, applicationsFileName=applicationsFileName, postsTypeName='jobPosts', applicationsTypeName='jobApplications')

#Load a percentage of the history 
# sEng.loadHistory(False, postsPercentage=1, applicationsPercentage=1)

#list all applied jobs for a certain user
print("user "+user_id+" applied for the following job list: ")
print(sEng.getOtherApplications(user_id=user_id))
print("------------------------------------------------------------------------------")

#list all applicants for a certain job
print("the folowing users applied for the job: "+job_id)
print(sEng.showApplicants(job_id=job_id))
print("------------------------------------------------------------------------------")

#recommend further jobs like a certain job for the job seeker
# print ("**app_id: ",app_id)
furtherJobs = sEng.recommendFurtherJobs(app_id)
print("the following are further jobs recommended for the user of app: "+app_id)
print(furtherJobs)
evaluationRes = sEng.evaluateRecommededJobs(app_id, furtherJobs)
print("the evaluation of the retrived jobs is as following:")
print(evaluationRes)
print("------------------------------------------------------------------------------")

#recommend job-seekers for the recruters
jobSeekers = sEng.recommendJobSeekers(job_id=job_id)
print("the recommended job-seekers for "+job_id+" are:")
print(jobSeekers)
evaluationRes = sEng.evaluateRecommendedJobSeekers(job_id=job_id, recommendedApplicants=jobSeekers)
print("the evaluation of the retrived job-seekers is as following")
print(evaluationRes)
print("------------------------------------------------------------------------------")

#job search based on search string
recommendedJobs = sEng.jobSearch(searchingString)
print("the result of job search for: "+searchingString+" is:")
print(recommendedJobs)