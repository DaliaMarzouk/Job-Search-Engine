Based on the available https://www.kaggle.com/WUZZUF/wuzzuf-job-posts; which is a sample of job posts and job applications; this search engine
was implemented. Here is a brief idea about the search engine.

The job search engine (JSE) is implemented in python. It mainly depends on two important python
libraries; pandas and elasticsearch.
Pandas library is used to import the data from the csv file in an optimized way for the computational
memory.
About the elasticsearch, it is a very powerful search engine based on Lucene. It has amazing
capabilities in indexing documents and perform search operations to obtained customized
information

Engine Modules
--------------
The engine is implemented in three modules. The first one is importData module which is used to
facilitate importing data from the csv files. The second module is esModule which is responsible
for the direct contact with the elasticsearch engine. This module members tends to be more generic
and easy to be understood and used. And finally there is the jobSearchEngine which implements
the upper-level functions for the job search engine

Available Features
------------------
There is a set of features available for the JSE. These features are important for job seekers and
recruiters both. This features are
1. jobSearch: it performs a job search process based on a search string that are typed by the
job-seeker
2. recommendFurtherJob: this feature is important for the job seekers as it generate further
jobs. These retrieved jobs are based on finding similar jobs like the job that the job seeker
applied for. Of course if there were available data about the job-seeker herself this feature
would be more effective and powerful. This feature should be edited in the future to
consider dates and job requirements. Also giving weights or boosting certain field would be
important for this function.
3. RecommendJobSeekers: this function recommend job seekers for the recruiters who may be
interested on that job. These recommended individuals are the applicants for the similar job
posts. Also considering dates would be important and sure further information about jobseekers would help.

