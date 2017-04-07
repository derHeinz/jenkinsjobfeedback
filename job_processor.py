import jenkins_helper
import job_update
import json
import os.path
import threading
import time

# filename datafile to write back states
datafilename = 'data.json'
	
class JobProcessor(threading.Thread):
	''' Processes through jobs and presents their feedback.'''

	def __init__(self, url, username, password):
		threading.Thread.__init__(self)
		self.daemon = True
		self.jenkins = jenkins_helper.JenkinsJobHelper(url, username, password)
		self.feedback = job_update.JobUpdate() # empty default
		self.job_data = None

	def init_jobs(self, joblist):
		self.jobs = joblist # is a list
		
		# read in data
		# TODO file may not exist
		self.job_data = self._load_jobstate()
			
		# init data in case it's empty
		for j in self.jobs:
			if (j not in self.job_data):
				self.job_data[j] = {'number': None, 'state': None}
				
		self._write_jobstate()
		
	def init_feedback(self, feedback):
		self.feedback = feedback
		
	def _load_jobstate(self):
		if (not os.path.isfile(datafilename)):
			data = dict()
			self._write_jobstate()
			return data
		else:
			with open(datafilename, 'r') as fp:
				return json.load(fp)
	
	def _write_single_jobstate(self, jobname, jobnumber, jobstate):
		self.job_data[jobname] = {'number': jobnumber, 'state': jobstate}
		self._write_jobstate()
	
	def _write_jobstate(self):
		# save to file
		with open(datafilename, 'w') as fp:
			json.dump(self.job_data, fp)
	
	def check_jobs(self):

		for jobst in self.job_data.items():
			jobname = jobst[0]
			new_jobstate = self.jenkins.check_job(jobname)
			old_jobstate = jobst[1]['state']
			old_number = jobst[1]['number']
			
			committers = self.jenkins.get_committers(jobname)
			buildnumber = self.jenkins.get_buildnumber(jobname)
			
			# if nothing changed -> ok
			if (old_number == buildnumber):
				self.feedback.no_new_build(jobname)
				continue
				
			# if build running
			if (self.jenkins.is_running(jobname)):
				self.feedback.new_build_running(jobname)
				continue
	
			# previously the build was green
			if (old_jobstate == True):
				if (new_jobstate == True):
					# further success
					self.feedback.still_okay(jobname, committers)
				else:
					# new build broken
					self.feedback.build_broken(jobname, committers)
			# build was red
			else:
				if (new_jobstate == True):
					self.feedback.okay_again(jobname, committers)
				else:
					self.feedback.still_broken(jobname, committers)
			# update the jobstate
			self._write_single_jobstate(jobname, buildnumber, new_jobstate)
			
	def run(self):
		while True:
			self.check_jobs()
			time.sleep(20)