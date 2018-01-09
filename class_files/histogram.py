import os,time,datetime,sys,platform
from os import getcwd
from collections import namedtuple
from platform import python_version
from helper_methods import compatibility_print
from helper_methods import find_all_return_generator

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
		2)  Filename does not contain '..' except to indicate a relative path

	Considerations
		1)  

	Order of Operations
		1)  If only a single file is sent in it will open it and save it's data in a namedtuple
		2)  If a directory is sent in it will not read in any files but will return a dictionary of all files
		    that directory and all subsequent directories.
	"""

        # Variables here are common AND shared between all instances of this class

        # Dictionary of Error Codes
        error_codes = {}
        error_codes[1] = []
        error_codes[1].append("[ Caught Exception ]")
        error_codes[1].append("Error Code: 1 < Invalid Column Name In Input File >\n")
        error_codes[1].append("Character: 'REPLACE_WITH_replace_char' in 'REPLACE_WITH_header' is not a valid character for a header.")
        error_codes[1].append("Please change the header column in REPLACE_WITH_self.path to start with a letter of the alphabet.")
        error_codes[1].append("Column has been renamed in order for program to continue.\n")
        error_codes[2] = []
        error_codes[2].append("[ Caught Exception ]")
        error_codes[2].append("Error Code: 2 < Invalid OS and Path Combination >\n")
        error_codes[2].append("Detected OS: REPLACE_WITH_self.os_type")
        error_codes[2].append("Detected Path Type: REPLACE_WITH_self.path_type\n")
        error_codes[2].append("> This is a Fatal Error.  Program Exiting. <\n")
        error_codes[3] = []
        error_codes[3].append("[ Caught Exception ]")
        error_codes[3].append("Error Code: 3 < Beginning Or Ending Spaces Found In Path + Filename >\n")
        error_codes[3].append("Histogram Class Initialized With: >REPLACE_WITH_path<\n")
        error_codes[3].append("Trimmed Path: >REPLACE_WITH_temp_path<\n")
        # Error Code 4 is untested
        error_codes[4] = []
        error_codes[4].append("[ Caught Exception ]")
        error_codes[4].append("Error Code: 4 < Double // Found in Path >\n")
        error_codes[4].append("The Path: >REPLACE_WITH_path< has two '//' in it")
        error_codes[4].append("Adjusted to: >REPLACE_WITH_temp_path<\n")
        # Error Code 5 is untested
        error_codes[5] = []
        error_codes[5].append("[ Caught Exception ]")
        error_codes[5].append("Error Code: 5 < '..' Was Found In The Filename >\n")
        error_codes[5].append("Please rename <REPLACE_WITH_temp_path> to not include two successives dots")
        # Error Code 6 is untested
        error_codes[6] = []
        error_codes[6].append("[ Caught Exception ]")
        error_codes[6].append("Error Code: 6 < Operating System Not Supported >\n")
        error_codes[6].append("Supported Operating Systems are:\n * Windows\n * Linux\n * Macintosh\n")
        error_codes[7] = []
        error_codes[7].append("[ Caught Exception ]")
        error_codes[7].append("Error Code: 7 < Path + Filename Does Not Exist >")
        error_codes[7].append("REPLACE_WITH_self.pathREPLACE_WITH_self.filename\n")
        error_codes[8] = []
        error_codes[8].append("[ Caught Exception ]")
        error_codes[8].append("Error Code: 8 < Attempting to get Headers of a file from a Directory >")
        error_codes[8].append("Method: get_headers\n")
        error_codes[8].append("Was called with <absolute_path_to_file>: REPLACE_WITH_absolute_path_to_file\n")
        error_codes[8].append("REPLACE_WITH_absolute_path_to_file is invalid.  Rerun method by passing in a valid Path + Filename.\n")
        error_codes[9] = []
        error_codes[9].append("[ Caught Exception ]")
        error_codes[9].append("Error Code: 9 < Headers In File Contain Non-AlphaNumeric Characters >")
        error_codes[9].append("File <REPLACE_WITH_absolute_path_to_file>\n")
        error_codes[9].append("Contains the following Non-AlphaNumeric characters in it's Headers:")

	def __init__(self,path):
		# Benchmark all the things!
		time_begin = datetime.datetime.now()

                # List of errors caught
                self.caught_errors = []

                # Fix Path if needed
                if(len(path.strip()) != len(path)):
                        temp_path = path.strip()
                        self.caught_errors.append(3)
                        for error_message in self.error_codes[3]:
                                temp = error_message
                                temp = temp.replace('REPLACE_WITH_path',path)
                                temp = temp.replace('REPLACE_WITH_temp_path',temp_path)
                                compatibility_print(temp)
                else:
                        temp_path = path

                temp_path_dot_locs = list(find_all_return_generator(temp_path,'..'))

                # For dealing with python version compatibility
		self.python_version = python_version()
		
                if(sys.platform.lower().startswith('linux')):
			self.os_type = 'linux'
			temp_path_slash_locs = list(find_all_return_generator(temp_path,'/'))
                        self.filename = temp_path[temp_path_slash_locs[-1]+1:]

                        # If we are given a relative path make it an absolute path
                        if(len(temp_path_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'/'))
                                self.path = getcwd()[:getcwd_slash_locs[-len(temp_path_dot_locs)]] + temp_path[temp_path_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '/'
                        else:
                                self.path = temp_path

                        # I am lazy - really lazy ...
                        self.path = self.path.replace(self.filename, '')

                        if(os.path.isdir(self.path + self.filename)):
                                self.path_type = 'directory'
                                self.filename = None
                                # We're good.  We want the just the path - and not the filename here
                        elif(os.path.isfile(self.path + self.filename)):
                                self.path_type = 'file'
                                path_slash_locs = list(find_all_return_generator(self.path,'/'))
                                self.path = self.path[:path_slash_locs[-1]] + '/'
                        else:
                                self.path_type = 'invalid'
                                self.caught_errors.append(7)
                                for error_message in self.error_codes[7]:
                                        temp = error_message
                                        temp = temp.replace('REPLACE_WITH_self.path',self.path)
                                        temp = temp.replace('REPLACE_WITH_self.filename',self.filename)
                                        compatibility_print(temp)
                                
		elif(sys.platform.lower().startswith('win')):
			self.os_type = 'windows'
			
			temp_path_slash_locs = list(find_all_return_generator(temp_path,'\\'))
                        self.filename = temp_path[temp_path_slash_locs[-1]+1:]

                        # If we are given a relative path make it an absolute path
                        if(len(temp_path_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'\\'))
                                self.path = getcwd()[:getcwd_slash_locs[-len(temp_path_dot_locs)]] + temp_path[temp_path_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '\\'
                        else:
                                self.path = temp_path

                        # I am lazy - really lazy ...
                        self.path = self.path.replace(self.filename, '')

                        if(os.path.isdir(self.path + self.filename)):
                                self.path_type = 'directory'
                                self.filename = None
                                # We're good.  We want the just the path - and not the filename here
                        elif(os.path.isfile(self.path + self.filename)):
                                self.path_type = 'file'
                                path_slash_locs = list(find_all_return_generator(self.path,'\\'))
                                self.path = self.path[:path_slash_locs[-1]] + '\\'
                        else:
                                self.path_type = 'invalid'
                                self.caught_errors.append(7)
                                for error_message in self.error_codes[7]:
                                        temp = error_message
                                        temp = temp.replace('REPLACE_WITH_self.path',self.path)
                                        temp = temp.replace('REPLACE_WITH_self.filename',self.filename)
                                        compatibility_print(temp)
                                
		elif(sys.platform.lower().startswith('mac')):
			self.os_type = 'macintosh'
			temp_path_slash_locs = list(find_all_return_generator(temp_path,'/'))
                        self.filename = temp_path[temp_path_slash_locs[-1]+1:]

                        # If we are given a relative path make it an absolute path
                        if(len(temp_path_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'/'))
                                self.path = getcwd()[:getcwd_slash_locs[-len(temp_path_dot_locs)]] + temp_path[temp_path_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '/'
                        else:
                                self.path = temp_path

                        # I am lazy - really lazy ...
                        # This will remove the filename from the end of the path if it's there
                        self.path = self.path.replace(self.filename, '')

                        if(os.path.isdir(self.path + self.filename)):
                                self.path_type = 'directory'
                                self.filename = None
                                # We're good.  We want the just the path - and not the filename here
                        elif(os.path.isfile(self.path + self.filename)):
                                self.path_type = 'file'
                                path_slash_locs = list(find_all_return_generator(self.path,'/'))
                                self.path = self.path[:path_slash_locs[-1]] + '/'
                        else:
                                self.path_type = 'invalid'
                                self.caught_errors.append(7)
                                for error_message in self.error_codes[7]:
                                        temp = error_message
                                        temp = temp.replace('REPLACE_WITH_self.path',self.path)
                                        temp = temp.replace('REPLACE_WITH_self.filename',self.filename)
                                        compatibility_print(temp)
		else:
			self.os_type = 'invalid'
			self.caught_errors.append(6)
                        for error_message in self.error_codes[6]:
                                compatibility_print(error_message)

		if(3 in self.caught_errors):
                        compatibility_print("Corrected Path Without Spaces: >"+"<\n")

                if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                        pass
                elif(self.os_type == 'windows'):
                        pass

                # I think I don't want to tackle this
                # Preferreded route would be to call this class for each new directory instead of passing a list of directories
                ## Need to be able to hangle multiple datatypes being sent in
		##if(type('') == type(self.path)):
                ##        self.path_type = 'string'
		##elif(type([]) == type(self.path)):
		##	self.path_type = 'list'
		##elif(type({}) == type(self.path)):
		##	self.path_type = 'dict'
		##else:
		##	self.path_type = 'unknown'

                # Master variable which will contain all the metadata about the directory or filename passed in
		self.file_list = {}
		#self.get_file_list()

		time_end = datetime.datetime.now()
		run_time = (time_end - time_begin).seconds
		compatibility_print("Initialized in: "+str(run_time)+" seconds.")

	def get_file_list(self):
                # Benchmark all the things!
		time_begin = datetime.datetime.now()
		
		nt = namedtuple('file_attributes','filename accessed modified created directory raw_size type header filetype file_data')
		if(self.path_type == 'file'):
			# Need come back and make sure that at this point we are dealing with all absolute paths
			# getcwd() will only work will only work when the file is being opened from the directory
			# the program is being run from

                        dot_loc = list(find_all_return_generator(self.filename,'.'))[-1]

                        if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                                slash_loc = list(find_all_return_generator(self.filename,'/'))[-1]
                                if(dot_loc > slash_loc):
                                        file_type = self.filename[dot_loc+1:]
                                else:
                                        file_type = self.filename[slash_loc+1:]
                        elif(self.os_type == 'windows'):
                                slash_loc = list(find_all_return_generator(self.filename,'\\'))[-1]
                                if(dot_loc > slash_loc):
                                        file_type = self.filename[dot_loc+1:]
                                else:
                                        file_type = self.filename[slash_loc+1:]
                        else:
                                file_type = None
                                # Raise Error COME BACK AND WRITE ERROR MESSAGE
			
			file_info = os.stat(os.path.join(self.path,self.filename))
			self.file_list[self.path] = nt(self.path,
                                                       datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
                                                       datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
                                                       datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
                                                       self.path,
                                                       file_info.st_size,
                                                       'Directory' if os.path.isdir(self.path) else 'File',
						       self.get_headers(self.path + self.filename),
                                                       file_type,
                                                       None)
		elif(self.path_type == 'directory'):
			for filename in os.listdir(self.path):
				file_info = os.stat(os.path.join(self.path,filename))
				# need to add logic to check if windows or linux to fix slashes
				self.file_list[filename] = nt(filename,
						              datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
						  	      datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
						  	      datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
						  	      self.path,
						  	      file_info.st_size,
						  	      'Directory' if os.path.isdir(self.path + filename) else 'File',
							      self.get_headers(filename),
                                                              None,
                                                              None)
		else:
			self.caught_errors.append(7)
                        for error_message in self.error_codes[7]:
                                temp = error_message
                                temp = temp.replace('REPLACE_WITH_self.path',self.path)
                                temp = temp.replace('REPLACE_WITH_self.filename',self.filename)
                                compatibility_print(temp)

		time_end = datetime.datetime.now()
		run_time = (time_end - time_begin).seconds
		compatibility_print("Path parsed in: "+str(run_time)+" seconds.")

	def get_headers(self,absolute_path_to_file,hard_coded_delimeter=None):#,attempted_headers_and_success_rate=[],headers_yet_to_try=[]):
                """
                Assumptions
                        1)   Only alphanumeric characters will be used as headers.  Namedtuples cannot use strange characters as headers.

                attempted_headers_and_success_rate = []
                        [0] = ('_',0.7)
                        [1] = (',',0.98)
                        [2] = ('|',0.05)

                hard_coded_delimeter
                        Assign the delimeter to this if you know it or think the wrong delimeter will be chosen

                        This can also be used if your delimeter is an A-Z or a-z or ' ' as normally these are excluded from being headers
                """
		if(os.path.isdir(absolute_path_to_file)):
                        self.caught_errors.append(8)
                        for error_message in self.error_codes[8]:
                                temp = error_message
                                temp = temp.replace('REPLACE_WITH_absolute_path_to_file',absolute_path_to_file)
                                compatibility_print(temp)
			fixed_headers =  None
		elif(os.path.isfile(absolute_path_to_file)):
			# open the file and count the lines in it
			#readfile = open(self.path + self.file_list[key],'r')
			readfile = open(absolute_path_to_file,'r')
			for line in readfile:
				header = line.strip()
				break
			readfile.close()

			# I forget why, but it's a good idea to delete file I/O when you are done with them
			del readfile

                        if(hard_coded_delimeter == None):
                                unique_chars_in_header = list(set(header))
                                count_chars = {}
                                for char in unique_chars_in_header:
                                        count_chars[char] = 0
                                for char in header:
                                        # Exclude a-z,A-Z and spaces from being considered as delimeters
                                        if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or (ord(char) == 32)):
                                                pass
                                        else:
                                                count_chars[char] = count_chars[char] + 1

                                # Identify which delimeter occurs the most in the header
                                max_count = 0
                                max_corresponding_key = unique_chars_in_header[0]
                                for key in count_chars.keys():
                                        if(max_count < count_chars[key]):
                                                max_count = count_chars[key]
                                                max_corresponding_key = key

                                if((ord(max_corresponding_key) >= 65 and ord(max_corresponding_key) <= 90) or (ord(max_corresponding_key) >= 97 and ord(max_corresponding_key) <= 122) or (ord(max_corresponding_key) == 32)):
                                        # The files has only one column and the first line is the header
                                        max_corresponding_key = '21jk3jk,m,mf^ff_this_plain_simply_does_exist_zzxcoisdfmgksmn342k53mkfmdsk'

                                most_successful_delimeter = ''
                                most_successful_percentage = 0

                                # Remove the alphanumeric characters from consideration of being a delimeter
                                for key in count_chars:
                                        if(count_chars[key] == 0):
                                                del count_chars[key]

                                # Alternative approach where we calculate the success of finding the header
                                for key in count_chars:

                                        header_to_return = ''
                                        for each_column in header.split(max_corresponding_key):
                                                temp_header = each_column.strip().replace(' ','_') + ' '
                                                # Namedtuple cannot begin with an underscore
                                                while(temp_header[0] == '_'):
                                                        temp_header = temp_header[1:]
                                                header_to_return += temp_header
                                        header_to_return = header_to_return.strip()

                                        # i dont want to live on this planet anymore
                                        
                                        temp_success,temp_delimeter = self.attempt_to_read_file(absolute_path_to_file,key,header_to_return)
                                        if(temp_success > most_successful_percentage):
                                                most_successful_percentage = temp_success
                                                most_successful_delimeter = temp_delimeter
                                max_corresponding_key = most_successful_delimeter
                                
                        else:
                                max_corresponding_key = hard_coded_delimeter
                                most_successful_percentage = 0

			header_to_return = ''
			for each_column in header.split(max_corresponding_key):
                                temp = each_column.strip().replace(' ','_') + ' '
                                # Namedtuple cannot begin with an underscore
                                while(temp[0] == '_'):
                                        temp = temp[1:]
				header_to_return += temp
			header_to_return = header_to_return.strip()
			self.headers = header_to_return
			self.delimeter = max_corresponding_key
			check_namedtuple_naming_conventions = header_to_return.split(' ')
			fixed_headers = []
			fixed_header_counter = 0
			found_error = False
			for header in check_namedtuple_naming_conventions:
                                if(header.isalpha()):
                                        fixed_headers.append(header)
                                else:
                                        found_error = True
                                        invalid_chars = []
                                        found_invalid_header = False
                                        #Somewhere in here attmpt_to_fix header
                                        for char in header:
                                                if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or (ord(char) == 32)):
                                                        pass
                                                        # We're good
                                                else:
                                                        found_invalid_header = True
                                                        invalid_chars.append(char)
                                        fixed_header_counter += 1
                                        temp_fix_header = header
                                        for replace_char in invalid_chars:
                                                temp_fix_header = temp_fix_header.replace(replace_char,'')
                                        fixed_headers.append('renamed_header_'+str(fixed_header_counter)+'_'+temp_fix_header)
                                        fixed_header_counter += 1
                                        
                        if(found_error):
                                self.caught_errors.append(1)
                                for error_message in self.error_codes[1]:
                                        temp = error_message
                                        if('REPLACE_WITH_replace_char' in temp):
                                                for replace_char in invalid_chars:
                                                        temp += error_message.replace('REPLACE_WITH_replace_char',replace_char) + '\n'
                                        temp = temp.replace('REPLACE_WITH_header',header)
                                        temp = temp.replace('REPLACE_WITH_self.path',self.path)
                                        compatibility_print(temp)
			#chars_that_nt_cannot_start_with = ['0','1','2','3','4','5','6','7','8','9','_']
                        self.headers = fixed_headers
		else:
                        fixed_headers = None
                        max_corresponding_key = ''
                        most_successful_percentage = float(0.0)
                        self.caught_errors.append(7)
                        for error_message in self.error_codes[7]:
                                temp = error_message
                                temp = temp.replace('REPLACE_WITH_self.path',self.path)
                                temp = temp.replace('REPLACE_WITH_self.filename',self.filename)
                                compatibility_print(temp)

                # Check to make sure headers contain only alpha numeric characters
                
                return fixed_headers,max_corresponding_key,most_successful_percentage

        def attempt_to_read_file(self,absolute_path_to_file,delimeter,headers):
                """
                Pass in the absolute path to the file and the delimeter and this will read the file and return:
                        lines read correctly
                        lines excluded
                        success percentage
                """
                nt = namedtuple('file_data',headers)
		ans = []
		readfile = open(absolute_path_to_file,'r')
		counter = -1
		successful_insert = 0
		failure_insert = 0
		compatibility_print(headers)
		for line in readfile:
                        # Skip Header Line
                        if(counter == -1):
                                pass
                        else:
                                try:
                                        ans.append(nt(*line.split(delimeter)))
                                        successful_insert += 1
                                except:
                                        failure_insert += 1
                        counter += 1
                try:
                        temp = (float(successful_insert))/float(counter)*100
                except ZeroDivisionError:
                        temp = float(0)
                #print("{0:.2f}".format(temp)+"%")
                return float("{0:.2f}".format(temp)),delimeter
                #compatibility_print("Succeeded:",str(successful_insert))
                #compatibility_print("Failed   :",str(failure_insert))

	# Does a Primary Key Exist?
	def get_primary_key(self,lines_to_check=9999):

                # We can't get the Primary Keys unless we know what we need to get the Primary Keys of
		if(len(self.file_list.keys()) == 0):
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
	def save_for_later():
                # Are we dealing with one file, multiple files, or a directory?
		self.path_type = 'directory' if os.path.isdir(path) else 'unknown'
		if(self.path_type == 'unknown'):
			self.path_type = 'file' if os.path.isfile(path) else 'unknown'

		if(self.path_type == 'file'):
			self.root_object = 'file'
			self.is_file = True
			self.is_dir = False
			# try to detect file encoding here?
		elif(self.path_type == 'directory'):
			self.root_object = 'directory'
			self.is_file = False
			self.is_dir = True
			# Loop through directory structure and get names of all files in all subfolders
		else:
                        self.root_object = 'unknown'
			self.is_file = False
			self.is_dir = False
			#print(path,"is not valid")
			# Raise Error
			# Need to come back and fix this better
			raise Exception("File Not Found: " , path)

		# Path we are dealing with
		if((self.os_type == 'linux' and self.path_type == 'file') or (self.os_type == 'macintosh' and self.path_type == 'file')):
                        folder_locs = find_all_return_generator(path,'')
                elif((self.os_type == 'linux' and self.path_type == 'directory') or (self.os_type == 'macintosh' and self.path_type == 'directory')):
                        pass
                elif(self.os_type == 'windows' and self.path_type == 'file'):
                        pass
                elif(self.os_type == 'windows' and self.path_type == 'directory'):
                        pass
                else:
                        self.caught_errors.append(2)
                        for error_message in self.error_codes[2]:
                                temp = error_message
                                temp = temp.replace('REPLACE_WITH_self.os_type',self.os_type)
                                temp = temp.replace('REPLACE_WITH_self.path_type','unknown')#self.path_type)
                                compatibility_print(temp)
                        return None

		# Setting this to mark get_headers as not being run yet
		self.headers = None
