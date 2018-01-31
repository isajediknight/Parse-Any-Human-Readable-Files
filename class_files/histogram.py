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

        python_key_words = ['False','class','finally','is','return','None','continue','for','lambda','try','True','def','from',
                            'nonlocal','while','and','del','global','not','with','as','elif','if','or','yield','assert','else',
                            'import','pass','break','except','in','raise']
        invalid_nt_field_chars = ['-']

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

                # Find all the up-one-directories
                double_dot_locs = list(find_all_return_generator(temp_path,'..'))

                # For dealing with python version compatibility
		self.python_version = python_version()
		
                if(sys.platform.lower().startswith('linux')):
			self.os_type = 'linux'
			temp_path_slash_locs = list(find_all_return_generator(temp_path,'/'))
                        self.filename = temp_path[temp_path_slash_locs[-1]+1:]

                        # If we are given a relative path make it an absolute path
                        if(len(double_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'/'))
                                self.path = getcwd()[:getcwd_slash_locs[-len(double_dot_locs)]] + temp_path[double_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '/'
                        else:
                                self.path = temp_path

                        # I am lazy - really lazy ...
                        # If the filename is at the end - remove it
                        self.path = self.path.replace(self.filename, '')

                        # Detect what we were given
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
                        if(len(double_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'\\'))
                                self.path = getcwd()[:getcwd_slash_locs[-len(double_dot_locs)]] + temp_path[double_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '\\'
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
                                # We shouldn't ever run into this.  Everything should be a file or a directory.
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
                        if(len(double_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'/'))
                                self.path = getcwd()[:getcwd_slash_locs[-len(double_dot_locs)]] + temp_path[double_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '/'
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

                # Get list of all files and directories from a path
                # Includes subdirectories recursively
                self.dirs_files_to_loop_through = []

                self.build_all_directory_file_list(self.path + ('' if self.filename == None else self.filename))

                # Master variable which will contain all the metadata about the directory or filename passed in
		self.file_list = {}

                # This will contain the data of the file if so desired
                self.file_data = {}

                # This will count the lines in the file
                self.file_line_count = {}

                # This contains uniqueness of data in the file
                self.file_histogram = {}

		# Save delimiter and Header attempts
		self.delimiter_header_attempts = {}

                #for each_object in self.dirs_files_to_loop_through:
                #        # Get basic data about the file / directory
                #        self.get_file_list(each_object)
                self.get_all_file_info()

		time_end = datetime.datetime.now()
		run_time = (time_end - time_begin).seconds
		compatibility_print("Initialized in: "+str(run_time)+" seconds.")

        # DAMNIT!!!!!!!!!!!!!!!
	def get_file_list(self,next_object):
                # Benchmark all the things!
		time_begin = datetime.datetime.now()

                if(next_filename == None or next_filename == ''):
                       next_path = self.path
                       next_filename = '' if self.filename == None else self.filename

                if(os.path.isdir(next_path + next_filename)):
                        which_type = 'directory'
                elif(os.path.isfile(next_path + next_filename)):
                        which_type = 'file'
                else:
                        which_type = 'error'

		# Data points we want to capture
		nt = namedtuple('file_attributes','filename accessed modified created directory raw_size type header filetype delimiter')
		
		if(which_type == 'file'):

                        # Need to add logic for filenames with no dot
                        dot_loc = list(find_all_return_generator(next_filename,'.'))[-1]

                        if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                                slash_loc = list(find_all_return_generator(next_filename,'/'))[-1]
                                if(dot_loc > slash_loc):
                                        file_type = next_filename[dot_loc+1:]
                                else:
                                        file_type = next_filename[slash_loc+1:]
                        elif(self.os_type == 'windows'):
                                try:
                                        slash_loc = list(find_all_return_generator(next_filename,'\\'))[-1]
                                except:
                                        slash_loc = -1
                                
                                if(dot_loc > slash_loc):
                                        file_type = next_filename[dot_loc+1:]
                                else:
                                        file_type = next_filename[slash_loc+1:]
                        else:
                                file_type = None
                                # Raise Error COME BACK AND WRITE ERROR MESSAGE

                        # NEED TO COME BACK AND ADD LOGIC FOR FILES THAT DONT EXIST
                        if((next_path + next_filename) not in self.delimiter_header_attempts):
                                self.get_header_and_delimiter(next_path + next_filename)

                        most_success_delimiter = ''
                        most_success_percentage = float(0.0)
                        most_success_header = ''

                        for attempt in range(len(self.delimiter_header_attempts[next_path + next_filename])):
                                if(self.delimiter_header_attempts[next_path + next_filename][attempt].success_percentage > most_success_percentage):
                                        most_success_delimiter = self.delimiter_header_attempts[next_path + next_filename][attempt].delimiter
                                        most_success_percentage = self.delimiter_header_attempts[next_path + next_filename][attempt].success_percentage
                                        most_success_header = self.delimiter_header_attempts[next_path + next_filename][attempt].headers
			
			file_info = os.stat(os.path.join(next_path,next_filename))
			self.file_list[next_path+next_filename] = nt(next_filename,
                                                       datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
                                                       datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
                                                       datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
                                                       next_path,
                                                       file_info.st_size,
                                                       'Directory' if os.path.isdir(next_path+next_filename) else 'File',
						       most_success_header,
                                                       file_type,
                                                       most_success_delimiter)
		elif(which_type == 'directory'):
			for filename in os.listdir(next_path):
				file_info = os.stat(os.path.join(next_path,filename))

                                if(os.path.isdir(next_path + filename) == False):
                                        dot_loc = list(find_all_return_generator(filename,'.'))[-1]

                                        if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                                                slash_loc = list(find_all_return_generator(filename,'/'))[-1]
                                                if(dot_loc > slash_loc):
                                                        file_type = filename[dot_loc+1:]
                                                else:
                                                        file_type = filename[slash_loc+1:]
                                        elif(self.os_type == 'windows'):
                                                try:
                                                        slash_loc = list(find_all_return_generator(filename,'\\'))[-1]
                                                except:
                                                        slash_loc = -1
                                
                                                if(dot_loc > slash_loc):
                                                        file_type = filename[dot_loc+1:]
                                                else:
                                                        file_type = filename[slash_loc+1:]
                                        else:
                                                file_type = None
                                                # Raise Error COME BACK AND WRITE ERROR MESSAGE

                                        # NEED TO COME BACK AND ADD LOGIC FOR FILES THAT DONT EXIST
                                        if((self.path + filename) not in self.delimiter_header_attempts):
                                                self.get_header_and_delimiter(next_path + filename)

                                        most_success_delimiter = ''
                                        most_success_percentage = float(0.0)
                                        most_success_header = ''

                                        try:
                                                for attempt in range(len(self.delimiter_header_attempts[next_path + filename])):
                                                        if(self.delimiter_header_attempts[self.path + filename][attempt].success_percentage > most_success_percentage):
                                                                most_success_delimiter = self.delimiter_header_attempts[next_path + filename][attempt].delimiter
                                                                most_success_percentage = self.delimiter_header_attempts[next_path + filename][attempt].success_percentage
                                                                most_success_header = self.delimiter_header_attempts[next_path + filename][attempt].headers
          
                                                self.file_list[next_path + filename] = nt(filename,
                                                                                          datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
                                                                                          datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
                                                                                          datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
                                                                                          next_path,
                                                                                          file_info.st_size,
                                                                                          'Directory' if os.path.isdir(next_path + filename) else 'File',
                                                                                          most_success_header,
                                                                                          file_type,
                                                                                          most_success_delimiter)
                                

                                        except KeyError:
                                                compatibility_print("Create new Error here.  self.path + filename has no non alphanumeric headers")
                                
                                # We're dealing with a directory
                                else:
                                        
                                        self.file_list[next_path + filename] = nt(filename,
                                                                                  datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
                                                                                  datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
                                                                                  datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
                                                                                  next_path,
                                                                                  file_info.st_size,
                                                                                  'Directory' if os.path.isdir(next_path + filename) else 'File',
                                                                                  None,
                                                                                  None,
                                                                                  None)
                                        
                                        
                                        
                                        

                                        
				
		else:
			self.caught_errors.append(7)
                        for error_message in self.error_codes[7]:
                                temp = error_message
                                temp = temp.replace('REPLACE_WITH_self.path',next_path)
                                temp = temp.replace('REPLACE_WITH_self.filename',next_filename)
                                compatibility_print(temp)

		time_end = datetime.datetime.now()
		run_time = (time_end - time_begin).seconds
		compatibility_print("Path parsed in: "+str(run_time)+" seconds.")

        def get_all_file_info(self):
                """
                Version 2 of this.  Decided to do the recursive search prior to reading in all the info.
                """
                if(len(self.dirs_files_to_loop_through) == 0):
                        build_all_directory_file_list(self.path)

                # Data points we want to capture
		nt = namedtuple('file_attributes','filename accessed modified created directory raw_size type header filetype delimiter success_percentage')

                for dir_or_file in self.dirs_files_to_loop_through:

                        if(len(list(find_all_return_generator(dir_or_file,'.'))) == 0):
                                # It's likely we're dealing with a directory
                                dot_loc = -1
                        else:
                                dot_loc = list(find_all_return_generator(dir_or_file,'.'))[-1]
                        
                        if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                                slash_loc = list(find_all_return_generator(dir_or_file,'/'))[-1]
                                if(dot_loc > slash_loc):
                                        file_type = dir_or_file[dot_loc+1:]
                                else:
                                        file_type = dir_or_file[slash_loc+1:]
                        elif(self.os_type == 'windows'):
                                try:
                                        slash_loc = list(find_all_return_generator(dir_or_file,'\\'))[-1]
                                except:
                                        slash_loc = -1
                                
                                if(dot_loc > slash_loc):
                                        file_type = dir_or_file[dot_loc+1:]
                                else:
                                        file_type = dir_or_file[slash_loc+1:]
                        else:
                                pass
                                # Raise Error

                        filename = '' if os.path.isdir(dir_or_file) else dir_or_file[slash_loc+1:]

                        # NEED TO COME BACK AND ADD LOGIC FOR FILES THAT DONT EXIST
                        if((dir_or_file) not in self.delimiter_header_attempts):
                                self.get_header_and_delimiter(dir_or_file)

                        most_success_delimiter = ''
                        most_success_percentage = float(0.0)
                        most_success_header = ''
                        
                        for attempt in range(len(self.delimiter_header_attempts[dir_or_file])):
                                if(self.delimiter_header_attempts[dir_or_file][attempt].success_percentage > most_success_percentage):
                                        most_success_delimiter = self.delimiter_header_attempts[dir_or_file][attempt].delimiter
                                        most_success_percentage = self.delimiter_header_attempts[dir_or_file][attempt].success_percentage
                                        most_success_header = self.delimiter_header_attempts[dir_or_file][attempt].headers

                        directory = dir_or_file[:slash_loc+1]
			
			file_info = os.stat(dir_or_file)
			self.file_list[dir_or_file] = nt(filename,
                                                         datetime.datetime.strptime(time.ctime(file_info.st_atime), "%a %b %d %H:%M:%S %Y"),
                                                         datetime.datetime.strptime(time.ctime(file_info.st_mtime), "%a %b %d %H:%M:%S %Y"),
                                                         datetime.datetime.strptime(time.ctime(file_info.st_ctime), "%a %b %d %H:%M:%S %Y"),
                                                         directory,
                                                         file_info.st_size,
                                                         'Directory' if os.path.isdir(dir_or_file) else 'File',
                                                         None if os.path.isdir(dir_or_file) else most_success_header,
                                                         None if os.path.isdir(dir_or_file) else file_type,
                                                         None if os.path.isdir(dir_or_file) else most_success_delimiter,
                                                         None if os.path.isdir(dir_or_file) else most_success_percentage)
                        

        def build_all_directory_file_list(self,next_check):
                for filename in os.listdir(next_check):
                        fail = '/' if(self.os_type == 'linux' or self.os_type == 'macintosh') else '\\'
                        absolute_path = next_check + fail + filename
                        if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                                absolute_path = absolute_path.replace('//','/')
                        elif(self.os_type == 'windows'):
                                absolute_path = absolute_path.replace('\\\\','\\')
                                
                        if(os.path.isdir(absolute_path) and (absolute_path) not in self.dirs_files_to_loop_through):
                        #if(os.path.isdir(next_check + filename) and (next_check + filename) not in self.dirs_files_to_loop_through):
                                self.build_all_directory_file_list(absolute_path)
                                #self.build_all_directory_file_list(next_check  + filename)
                        self.dirs_files_to_loop_through.append(absolute_path)
                        #print(absolute_path)
                        #self.dirs_files_to_loop_through.append(next_check + filename)

        def attempt_to_read_file(self,absolute_path_to_file,headers,delimiter=None,lines_to_read=10000):
                """
                Pass in the absolute path to the file and the delimiter and this will read the file and return:
                        success percentage
                        delimiter used

                Arbitrarily picked 10,000 lines to read in to test reading
                """
                # namedtuple for headers
                nt_read = namedtuple('file_data',headers)

                # namedtuple for delimiter success rate
		nt_ans = namedtuple('delimiter_success_ratios','success_percentage delimiter headers')

                # Save the data from the file to here as a namedtuple
                ans = []

		# Open the file for reading
		readfile = open(absolute_path_to_file,'r')

		# Count the lines we have read in
		counter = -1

		# Count successful inserts
		successful_insert = 0

		# Count failed inserts
		failure_insert = 0

		# Read in each line in the file
		for line in readfile:
                        # Skip Header Line
                        if(counter == -1):
                                pass
                        elif(counter > lines_to_read):
                                # Once we read in an arbitrary number of lines stop
                                # This method just tests how successful an attempt to read the file is
                                # We don't need to read in the whole file here
                                break
                        else:
                                try:
                                        # Attempt to insert the data in the namedtuple
                                        ans.append(nt_read(*line.split(delimiter)))

                                        # Increment Successes
                                        successful_insert += 1
                                except:
                                        # Increment Failures
                                        failure_insert += 1
                                        
                        # Increment line number
                        counter += 1
                try:
                        temp = (float(successful_insert))/float(counter)*100
                except ZeroDivisionError:
                        temp = float(0)

                readfile.close()

                return nt_ans(float("{0:.2f}".format(temp)),delimiter,headers)

        def read_file(self,absolute_path_to_file,delimiter,header):
                """
                Reads in the data from the file.
                """

                # namedtuple for headers
                nt_read = namedtuple('file_data',header)
                
                # Save the data from the file to here as a namedtuple
                ans = []

                # Open the file for reading
		readfile = open(absolute_path_to_file,'r')

		# Count successful inserts
		successful_insert = 0

		# Count failed inserts
		failure_insert = 0

                # count each header
                counter = 0

                nt_placeholder = []

		histogram_nt_header = ''
		for each_header in header.split(' '):
                        fix_start_with_underscore = '' if(len(each_header) == 0) else each_header + '_'
                        histogram_nt_header +=  fix_start_with_underscore + 'header_'+str(counter)+'_value_count header_' + str(counter) +'_duplicates '
                        nt_placeholder.append({})
                        nt_placeholder.append({})
                        counter += 1
                histogram_nt_header = histogram_nt_header.strip()

                nt_histogram = namedtuple('histogram',histogram_nt_header)

                histogram_ans = nt_histogram(*[x for x in nt_placeholder])

                # Count the lines we have read in
		counter = -1
		
		for line in readfile:
                        counter += 1
                        insert_status = False
                        if(counter == 0):
                                pass
                        else:
                                try:
                                        # Attempt to insert the data in the namedtuple
                                        #ans.append(nt_read(*line.strip().split(delimiter)))

                                        ans.append(nt_read(*[x.strip() for x in line.split(delimiter)]))

                                        # Increment Successes
                                        successful_insert += 1
                                        insert_status = True
                                        #print("Success",line)
                                except:
                                        # Increment Failures
                                        failure_insert += 1
                                        #print("Failure",line)

                                if(insert_status):
                                        #try:
                                        value_counter = 0
                                        for values in [x.strip() for x in line.split(delimiter)]:
                                                if(values in histogram_ans[value_counter]):
                                                        histogram_ans[value_counter - 1]['duplicate_count'] = histogram_ans[value_counter - 1]['duplicate_count'] + 1
                                                        histogram_ans[value_counter][values] = histogram_ans[value_counter][values] + 1
                                                else:
                                                        histogram_ans[value_counter][values] = 1
                                                        histogram_ans[value_counter - 1]['duplicate_count'] = 0
                                                value_counter += 2
                                        #except:
                                        #        #pass
                                        #        print([x.strip() for x in line.split(delimiter)])
                                
                                #try:
                                #        # Attempt to insert the data in the namedtuple
                                #        #ans.append(nt_read(*line.strip().split(delimiter)))
                                #        
                                #        ans.append(nt_read(*[x.strip() for x in line.split(delimiter)]))
                                #
                                #        value_counter = 0
                                #        for values in [x.strip() for x in line.split(delimiter)]:
                                #                if(values in histogram_ans[value_counter].keys()):
                                #                        histogram_ans[value_counter - 1] = histogram_ans[value_counter - 1] + 1
                                #                        histogram_ans[value_counter][values] = histogram_ans[value_counter][values] + 1
                                #                else:
                                #                        histogram_ans[value_counter][values] = 1
                                #                        histogram_ans[value_counter - 1] = 1
                                #                value_counter += 2
                                #
                                #        # Increment Successes
                                #        successful_insert += 1
                                #except:
                                #        # Increment Failures
                                #        failure_insert += 1
                                
                try:
                        temp = (float(successful_insert))/float(counter)*100
                except ZeroDivisionError:
                        temp = float(0)

                compatibility_print("File: "+absolute_path_to_file)
                compatibility_print("Percent Successful: "+str("{0:.2f}".format(temp))+'%')

                self.file_data[absolute_path_to_file] = ans
                self.file_line_count[absolute_path_to_file] = counter
                self.file_histogram[absolute_path_to_file] = histogram_ans

                readfile.close()

        def read_all_files(self):
                """
                Reads in the data from all the files in the directory
                """
                for file_key in self.file_list.keys():
                        if(self.file_list[file_key].type == 'File'):
                                self.read_file(self.file_list[file_key].directory + self.file_list[file_key].filename,self.file_list[file_key].delimiter,self.file_list[file_key].header)

        def get_header_and_delimiter(self,absolute_path_to_file,delimiter=None):
                """
                Recursive method if no delimiter is passed in.
                """
                if(os.path.isdir(absolute_path_to_file)):
                        self.delimiter_header_attempts[absolute_path_to_file] = []
                elif(delimiter == None):
                        readfile = open(absolute_path_to_file,'r')
                        header = readfile.readline().strip()
                        readfile.close()
                        del readfile

                        unique_chars_in_header = list(set(header))
                        count_chars = {}
                        for char in unique_chars_in_header:
                                count_chars[char] = 0
                        for char in header:
                                # Exclude a-z,A-Z and spaces from being considered as delimiters
                                if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or (ord(char) == 32)):
                                        pass
                                else:
                                        count_chars[char] = count_chars[char] + 1

                        temp = {}
                        # Remove the alphanumeric characters from consideration of being a delimiter
                        for key in count_chars:
                                if(count_chars[key] == 0):
                                        pass
                                else:
                                        temp[key] = count_chars[key]
                        count_chars = temp

                        for test_delimiter in count_chars:
                                self.get_header_and_delimiter(absolute_path_to_file,test_delimiter)
                        
                else:
                        readfile = open(absolute_path_to_file,'r')
                        header = readfile.readline()
                        readfile.close()
                        del readfile

                        fixed_headers = ''
                        temp_header = header.split(delimiter)
                        counter = 0
                        for each_column in temp_header:
                                if(each_column.isalpha()):
                                        
                                        # Remove Keywords used
                                        for key_word in self.python_key_words:
                                                if(each_column == key_word):
                                                        each_column = each_column.replace(key_word,'RENAMED_'+key_word+'_'+str(counter))
                                                        counter += 1
                                                        
                                        # Remove invlaid chars from namedtuple column names
                                        for invalid_char in self.invalid_nt_field_chars:
                                                if(invalid_char in each_column):
                                                        each_column = each_column.replace(invalid_char,'RENAMED_INVALID_CHAR_'+str(counter))
                                                        counter += 1
                                        
                                        fixed_headers += each_column + ' '
                                else:
                                        this_column = ''
                                        for each_char in each_column:
                                                if((ord(each_char) >= 48 and ord(each_char) <= 57)
                                                   or each_char.isalpha()
                                                   or (ord(each_char) >= 97 and ord(each_char) <= 122)
                                                   or (ord(each_char) == 95)):
                                                        this_column += each_char
                                                else:
                                                        pass
                                                        #compatibility_print(each_char + ' is invalid')
                                                        # Raise Error

                                        # Fix spaces
                                        this_column = this_column.replace(' ','_')

                                        # Remove Keywords used
                                        for key_word in self.python_key_words:
                                                if(this_column == key_word):
                                                        this_column = this_column.replace(key_word,'RENAMED_'+key_word+'_'+str(counter))
                                                        counter += 1

                                        if(len(this_column) > 0):
                                        
                                                # Make sure the beginning is a character and not a number or other character
                                                while(len(this_column) > 0 and this_column[0].isalpha() == False):
                                                        this_column = this_column[1:]
                                                        
                                        fixed_headers += this_column + ' '
                        fixed_headers = fixed_headers.strip()

                        if(absolute_path_to_file in self.delimiter_header_attempts):
                                self.delimiter_header_attempts[absolute_path_to_file].append(self.attempt_to_read_file(absolute_path_to_file,fixed_headers,delimiter))
                        else:
                                self.delimiter_header_attempts[absolute_path_to_file] = []
                                self.delimiter_header_attempts[absolute_path_to_file].append(self.attempt_to_read_file(absolute_path_to_file,fixed_headers,delimiter))

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
				ans.append(nt(my_line.split(self.delimiter)))
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

        
