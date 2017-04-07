
class JobUpdate:
	''' Simple feedback interface ot receive updates for Job's updates.'''
	def __init__(self):
		pass

	def still_okay(self, jobname, authors):
		pass
		
	def okay_again(self, jobname, authors):
		pass
	
	def build_broken(self, jobname, authors):
		pass
		
	def still_broken(self, jobname, authors):
		pass
		
	def no_new_build(self, jobname):
		pass
		
	def new_build_running(self, jobname):
		pass
	