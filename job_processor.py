import job_update
import json
import os.path
import threading
import time

class JobState:
	''' Defubes states of the build.'''
	FAILED, UNSTABLE, SUCCESS = range(3)

# filename datafile to write back states
DATA_FILENAME = 'data.json'
	
class JobProcessor(threading.Thread):
	''' Processes through jobs and presents their feedback.'''

	def __init__(self, buildtool):
		threading.Thread.__init__(self)
		self.daemon = True
		self.buildtool = buildtool
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
		if (not os.path.isfile(DATA_FILENAME)):
			data = dict()
			self._write_jobstate()
			return data
		else:
			with open(DATA_FILENAME, 'r') as fp:
				return json.load(fp)
	
	def _write_single_jobstate(self, jobname, jobnumber, jobstate):
		self.job_data[jobname] = {'number': jobnumber, 'state': jobstate}
		self._write_jobstate()
	
	def _write_jobstate(self):
		# save to file
		with open(DATA_FILENAME, 'w') as fp:
			json.dump(self.job_data, fp)
	
	def check_jobs(self):

		for jobst in self.job_data.items():
			jobname = jobst[0]
			new_jobstate = self.buildtool.check_job(jobname)
			old_jobstate = jobst[1]['state']
			old_number = jobst[1]['number']
			
			committers = self.buildtool.get_committers(jobname)
			buildnumber = self.buildtool.get_buildnumber(jobname)
			
			# if nothing changed -> ok
			if (old_number == buildnumber):
				self.feedback.no_new_build(jobname)
				continue
				
			# if build running
			if (self.buildtool.is_running(jobname)):
				self.feedback.new_build_running(jobname)
				continue
	
			# previous build was green
			if (old_jobstate == JobState.SUCCESS):
				if (new_jobstate == JobState.SUCCESS):
					self.feedback.still_green(jobname, committers)
				elif (new_jobstate == JobState.UNSTABLE):
					self.feedback.green_to_yellow(jobname, committers)
				elif (new_jobstate == JobState.FAILED):
					self.feedback.green_to_red(jobname, committers)
					
			# preivous build was yellow
			elif (old_jobstate == JobState.UNSTABLE):
				if (new_jobstate == JobState.SUCCESS):
					self.feedback.yellow_to_green(jobname, committers)
				elif (new_jobstate == JobState.UNSTABLE):
					self.feedback.still_yellow(jobname, committers)
				elif (new_jobstate == JobState.FAILED):
					self.feedback.yellow_to_red(jobname, committers)
			
			# preivous build was red
			elif (old_jobstate == JobState.FAILED):
				if (new_jobstate == JobState.SUCCESS):
					self.feedback.red_to_green(jobname, committers)
				elif (new_jobstate == JobState.UNSTABLE):
					self.feedback.red_to_yellow(jobname, committers)
				elif (new_jobstate == JobState.FAILED):
					self.feedback.still_red(jobname, committers)
					
			# preivous build unknown
			else:
				if (new_jobstate == JobState.SUCCESS):
					self.feedback.to_green(jobname, committers)
				elif (new_jobstate == JobState.UNSTABLE):
					self.feedback.to_yellow(jobname, committers)
				elif (new_jobstate == JobState.FAILED):
					self.feedback.to_red(jobname, committers)
			# update the jobstate
			self._write_single_jobstate(jobname, buildnumber, new_jobstate)
			
	def run(self):
		while True:
			self.check_jobs()
			time.sleep(20)