import csv

def allowed_file(filename):
	"""
	Return True if file within allowed extensions, False if not.
	"""
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           	
def load_csv(filename):
	with open(f'uploads/{filename}', newline='') as csvfile:
		filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
		rowCount = 0 
		tasksDict = {'tasks':[]}
		
		# Iterate through rows
		for row in filereader:
			taskEntry = {	'projectId':'',
				'taskDescription':'',
				'taskDate':'',
				'taskTime':'',
				'employeeId':''
				}
				
			# Start with the header row
			if rowCount == 0:
				for col in row[0].split(','):
					if col not in taskEntry.keys():
						print( "NOT CORRECT")
						return False
					taskEntry[col] = ''
				rowCount += 1
				
			# After header row, process entries 
			else:
				# Iterate through column values, map to dict
				for col in range(len(row)):
					keys = list(taskEntry.keys())
					taskEntry[keys[col]] = row[col]
				# Add the entry to the tasksDict
				tasksDict['tasks'].append(taskEntry)	
				
		# Return dict of all the tasks 
		return tasksDict

