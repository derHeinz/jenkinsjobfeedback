import unittest
import job_update
import job_processor
import job_state

class TestBuildtool:
	''' Used to fake the feedback of the buildtool.'''
	
	def __init__(self):
		self.check_job_result = None
		self.check_job_called = 0
		self.get_committers_result = None
		self.is_running_result = None
		self.get_buildnumber_result = None

	def check_job(self, jobname):
		self.check_job_called = self.check_job_called + 1
		return self.check_job_result
		
	def get_committers(self, jobname):
		return self.get_committers_result
	
	def is_running(self, jobname):
		return self.is_running_result
		
	def get_buildnumber(self, jobname):
		return self.get_buildnumber_result

class TestJobProcessor(unittest.TestCase):

	def prepare_test(self, last_job_state, job_state, feedback):
		buildtool = TestBuildtool()
		proc = job_processor.JobProcessor(buildtool)
		proc.init_feedback(feedback)
		
		# prepare testcase
		jobname = 'Doesntmatter'
		proc.init_jobs([jobname])
		# prepare last build's state
		proc._write_single_jobstate(jobname, 0, last_job_state)
		buildtool.check_job_result = job_state
		# prepare current build's state
		buildtool.get_buildnumber_result = 1
		
		# return the prepared processor
		return [proc, buildtool]

	# ------------------- OLDSTATE = None -------------------
		
	def test_check_jobs_feedback_to_green(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def to_green(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(None, job_state.JobState.SUCCESS, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_to_yellow(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def to_yellow(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(None, job_state.JobState.UNSTABLE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_to_red(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def to_red(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(None, job_state.JobState.FAILURE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	# ------------------- Newstate = SUCCESS -------------------
		
	def test_check_jobs_feedback_still_green(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def still_green(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.SUCCESS, job_state.JobState.SUCCESS, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_yellow_to_green(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def yellow_to_green(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.UNSTABLE, job_state.JobState.SUCCESS, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_red_to_green(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def red_to_green(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.FAILURE, job_state.JobState.SUCCESS, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	# ------------------- Newstate = UNSTABLE -------------------
		
	def test_check_jobs_feedback_still_yellow(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def still_yellow(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.UNSTABLE, job_state.JobState.UNSTABLE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_green_to_yellow(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def green_to_yellow(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.SUCCESS, job_state.JobState.UNSTABLE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_red_to_yellow(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def red_to_yellow(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.FAILURE, job_state.JobState.UNSTABLE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	# ------------------- Newstate = FAILURE -------------------
		
	def test_check_jobs_feedback_still_red(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def still_red(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.FAILURE, job_state.JobState.FAILURE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_green_to_red(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def green_to_red(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.SUCCESS, job_state.JobState.FAILURE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
	def test_check_jobs_feedback_yellow_to_red(self):
		
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.state_updated_called = 0
		
			def yellow_to_red(self, jobname, authors):
				self.state_updated_called = self.state_updated_called + 1
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(job_state.JobState.UNSTABLE, job_state.JobState.FAILURE, feedback)
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(1, buildtool.check_job_called)
		self.assertEquals(1, feedback.state_updated_called)
		
		
	# check author parsed correctly
	def test_parse_committers(self):
		# init all the stuff
		class TestFeedback(job_update.JobUpdate):
			def __init__(self):
				self.committers = None
		
			def to_green(self, jobname, authors):
				self.committers = authors
				
		feedback = TestFeedback()
		proc, buildtool = self.prepare_test(None, job_state.JobState.SUCCESS, feedback)
		
		buildtool.get_committers_result = ["bla", "blubb"]
		
		
		# check job called and green called
		proc.check_jobs()
		self.assertEquals(feedback.committers, buildtool.get_committers_result)
		
if __name__ == '__main__':
	unittest.main()