import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import job_state

class JenkinsJobHelper():
	''' This class is the accessor to jenkins. It acually uses jenkinsapi but could use the REST api directly'''
	
	def __init__(self, url, username, password):
		self.url = url
		self.username = username
		self.password = password
		self.jenkins = Jenkins(url, username, password)

	def _get_last_build(self, jobname):
		job = self.jenkins.get_job(jobname)
		return job.get_last_build()
		
	def check_job(self, jobname):
		last_build = self._get_last_build(jobname)
		if ('SUCCESS' == last_build.get_status()):
			return job_state.JobState.SUCCESS
		elif ('UNSTABLE' == last_build.get_status()):
			return job_state.JobState.UNSTABLE
		elif ('FAILURE' == last_build.get_status()):
			return job_state.JobState.FAILURE
		
	def get_committers(self, jobname):
		last_build = self._get_last_build(jobname)
		authors = []
		for i in last_build.get_changeset_items():
			author = i['author']
			authors.append(author['fullName'])
		return authors
	
	def is_running(self, jobname):
		last_build = self._get_last_build(jobname)
		return last_build.is_running()
		
	def get_buildnumber(self, jobname):
		last_build = self._get_last_build(jobname)
		return last_build.buildno
	