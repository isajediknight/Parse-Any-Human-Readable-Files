import os,time,datetime,sys,platform
from os import getcwd
from collections import namedtuple
from platform import python_version
from helper_methods import compatibility_print
class histogram:
	"""
	Goal is to create a class which will read in:
		1)  Data about a bunch of files in a directory or
		2)  Data in a single file.

	If 1)
		Will record paths and filenames as well as various useful metadata.

	If 2)
		It will tell the uniqueness of all values for all columns.

	Assumptions
		1)  The first line of the file contains headers.  This will be validated if the first line does not
		    contain any numbers in it.  Further validated if other lines in the file do contain numbers in
		    them.

	Considerations
		1)  

	Order of Operations
		1)  If only a single file is sent in it will open it and save it's data in a namedtuple
		2)  If a directory is sent in it will not read in any files but will return a dictionary of all files
		    that directory and all subsequent directories.
	"""

	def __init__(self,path):
		# Record the start time of the program
		time_begin = datetime.datetime.now()

		# Path we are dealing with
		self.path = path

		# Setting this to mark get_headers as not being run yet
		self.headers = None

		# Need to be able to hangle multiple datatypes being sent in
		if(type('') == type(self.path)):
			self.path_type = 'string'
		elif(type([]) == type(self.path)):
			self.path_type = 'list'
		elif(type({}) == type(self.path)):
			self.path_type = 'dict'
		else:
			self.path_type = 'unknown'

		# For dealing with python version compatibility
		self.python_version = python_version()

		if (sys.platform.lower().startswith('linux')):
			self.os_type = 'linux'
		elif(sys.platform.lower().startswith('win')):
			self.os_type = 'win'
		elif(sys.platform.lower().startswith('mac')):
			self.os_type = 'mac'
		else:
			self.os_type = 'unknown'
			# Raise Error

		# Are we dealing with one file, multiple files, or a directory?
		self.path_type = 'directory' if os.path.isdir(self.path) else 'unknown'
		if(self.path_type == 'unknown'):
			self.path_type = 'file' if os.path.isfile(self.path) else 'unknown'

		if(self.path_type == 'file'):
			compatibility_print(path,"is a file")
			self.root_object = 'file'
			self.is_file = True
			self.is_dir = False
			# try to detect file encoding here?
		elif(self.path_type == 'directory'):
			compatibility_print(path,"is a directory")
			self.root_object = 'directory'
			self.is_file = False
			self.is_dir = True
			# Loop through directory structure and get names of all files in all subfolders
		else:
			#print(path,"is not valid")
			# Raise Error
			# Need to come back and fix this better
			raise Exception("File Not Found: " , path)

		self.file_list = {}

		self.get_file_list()

		#print len(list(self.file_list.keys()))

		

		time_end = datetime.datetime.now()
		run_time = (time_end - time_begin).seconds
		compatibility_print("Initialized in: "+str(run_time)+" seconds.")

	def get_file_list(self):
		nt = namedtuple('file_attributes','filename accessed modified created directory raw_size type header')
		if(self.is_file):
			# Need come back and make sure that at this point we are dealing with all absolute paths
			# getcwd() will only work will only work when the file is being opened from the directory
			# the program is being run from
			file_info = os.stat(os.path.join(getcwd(),self.path))
			self.file_list[self.path] = nt(self.path,
                                                       datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
                                                       datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
                                                       datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
                                                       self.path,
                                                       file_info.st_size,
                                                       'Folder' if os.path.isdir(self.path) else 'File',
						       self.get_headers(self.path))
		elif(self.is_dir):
			for filename in os.listdir(self.path):
				file_info = os.stat(os.path.join(self.path,filename))
				# need to add logic to check if windows or linux to fix slashes
				self.file_list[filename] = nt(filename,
						              datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
						  	      datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
						  	      datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
						  	      self.path,
						  	      file_info.st_size,
						  	      'Folder' if os.path.isdir(self.path + filename) else 'File',
							      self.get_headers(filename))
				#compatibility_print(self.path + filename)
		else:
			pass
			# Raise Error

	def get_headers(self,key):
		if(self.is_dir):
			compatibility_print("[ <",self.path,">",'is a Directory ]')
			compatibility_print("There are no File Headers")
			return None
		elif(self.is_file):
			# open the file and count the lines in it
			#readfile = open(self.path + self.file_list[key],'r')
			readfile = open(key,'r')
			for line in readfile:
				header = line.strip()
				break
			readfile.close()

			# I forget why, but it's a good idea to delete file I/O when you are done with them
			del readfile

			unique_chars_in_header = list(set(header))
			count_chars = {}
			for char in unique_chars_in_header:
				count_chars[char] = 0
			for char in header:
				# Exclude a-z,A-Z and spaces from being considered as delimeters
				if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or (ord(char) == 32)):
					count_chars[char] = 1
				else:
					count_chars[char] = count_chars[char] + 1

			max_count = 0
			max_corresponding_key = unique_chars_in_header[0]
			for key in count_chars.keys():
				if(max_count < count_chars[key]):
					max_count = count_chars[key]
					max_corresponding_key = key

			header_to_return = ''
			for each_column in header.split(max_corresponding_key):
				header_to_return += each_column.strip().replace(' ','_') + ' '
			header_to_return = header_to_return.strip()
			self.headers = header_to_return
			self.delimeter = max_corresponding_key
			check_namedtuple_naming_conventions = header_to_return.split(' ')
			fixed_headers = []
			fixed_header_counter = 1
			for header in check_namedtuple_naming_conventions:
                                if((ord(header[0]) >= 65 and ord(header[0]) <= 90) or (ord(header[0]) >= 97 and ord(header[0]) <= 122) or (ord(header[0]) == 32)):
                                        fixed_headers.append(header)
                                else:
                                        fixed_headers.append('renamed_header_'+str(fixed_header_counter)+'_'+header)
                                        fixed_header_counter += 1
                                        compatibility_print("[ Caught Exception ]")
                                        compatibility_print("Error Code: 1 < Invalid Column Name In Input File >\n")
                                        compatibility_print("Character: '"+header[0]+"' in '"+header+"' is not a valid beginning character for a header.")
                                        compatibility_print("Please change the header column in "+self.path+" to start with a letter of the alphabet.")
                                        compatibility_print("Column has been renamed in order for program to continue.\n")
			#chars_that_nt_cannot_start_with = ['0','1','2','3','4','5','6','7','8','9','_']
                        self.headers = fixed_headers
			return fixed_headers

	# Does a Primary Key Exist?
	def get_primary_key(self,lines_to_check=9999):
		if(self.headers == None):
			self.get_file_list()
		else:
			nt = namedtuple('identify_primary_key',self.headers)
			ans = []
			readfile = open(key,'r')
			counter = -1
                        for line in readfile:
				counter += 1
                                my_line = line.strip()
				if(counter > lines_to_check):
                                	break
				ans.append(nt(my_line.split(self.delimeter)))
                        readfile.close()

                        # I forget why, but it's a good idea to delete file I/O when you are done with them
                        del readfile
			return ans

	# Try to determine what the names of the values should be
	def get_nt_values(self):
		pass

	# Returns number of rows or files
	def get_number_of_objects(self):
		if(self.is_file):
			pass
			# open file and count rows
		elif(self.is_dir):
			pass
			# iterate through files and count them
		else:
			pass
			# Raise Error

	def help(self,which=None):
		compatibility_print("\n[ Help Options for Histogram Class ]",'\n\n')
		if(which == None):
			compatibility_print("[ No Options passed in.  Please re-run. ]")
			compatibility_print(".help('vars')")
			compatibility_print(".help('methods')")
		elif(which == 'vars'):
			compatibility_print("[ Variables ]",'\n\n')
			compatibility_print(".is_file\n\tBoolean: True/False\n\tDescription is it file or not?",'\n\n')
			compatibility_print(".is_dir\n\tBoolean: True/False",'\n\n')
			compatibility_print(".root_object\n\tThe type of object passed to create the class",'\n\n')
			compatibility_print(".path\n\tThe path passed in when the Histogram object was created",'\n\n')
		elif(which == 'methods'):
			compatibility_print(" [ Methods ]",'\n\n')
			compatibility_print(".get_headers()\n\tAssigns Headers to .headers",'\n\n')
