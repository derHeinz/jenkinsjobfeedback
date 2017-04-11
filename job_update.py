class JobUpdate:
	''' Simple feedback interface ot receive updates for Job's updates.'''
	def __init__(self):
		pass
		
	# green states
	
	def to_green(self, jobname, authors):
		pass
		
	def still_green(self, jobname, authors):
		pass
	
	def green_to_yellow(self, jobname, authors):
		pass
	
	def green_to_red(self, jobname, authors):
		pass
	
	# yellow states
	
	def to_yellow(self, jobname, authors):
		pass
	
	def still_yellow(self, jobname, authors):
		pass
	
	def yellow_to_green(self, jobname, authors):
		pass
	
	def yellow_to_red(self, jobname, authors):
		pass
	
	# red states
	
	def to_red(self, jobname, authors):
		pass
	
	def still_red(self, jobname, authors):
		pass
	
	def red_to_yellow(self, jobname, authors):
		pass
	
	def red_to_green(self, jobname, authors):
		pass
	
	# nothing new
	def no_new_build(self, jobname):
		pass
		
	# build running
	def new_build_running(self, jobname):
		pass
	