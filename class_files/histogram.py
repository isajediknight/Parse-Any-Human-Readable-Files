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
        # Need to come back and reake this error code
        #error_codes[2] = []
        #error_codes[2].append("[ Caught Exception ]")
        #error_codes[2].append("Error Code: 2 < Invalid OS and Path Combination >\n")
        #error_codes[2].append("Detected OS: REPLACE_WITH_self.os_type")
        #error_codes[2].append("Detected Path Type: REPLACE_WITH_self.path_type\n")
        #error_codes[2].append("> This is a Fatal Error.  Program Exiting. <\n")
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
        error_codes[7].append("REPLACE_WITH_my_pathREPLACE_WITH_my_filename\n")
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
                self.caught_errors_files_or_dirs = []

                # Fix Path if needed
                if(len(path.strip()) != len(path)):
                        temp_path = path.strip()
                        self.caught_errors.append(3)
                        for error_message in self.error_codes[3]:
                                temp = error_message
                                temp = temp.replace('REPLACE_WITH_path',path)
                                temp = temp.replace('REPLACE_WITH_temp_path',temp_path)
                                compatibility_print(temp)
                        path = temp_path
                else:
                        #temp_path = path
                        pass

                # For dealing with python version compatibility
                self.python_version = python_version()
		
                if(sys.platform.lower().startswith('linux')):
                        self.os_type = 'linux'
                elif(sys.platform.lower().startswith('mac')):
                        self.os_type = 'macintosh'
                elif(sys.platform.lower().startswith('win')):
                        self.os_type = 'windows'
                else:
                        self.os_type = 'invalid'
                        self.caught_errors.append(6)
                        for error_message in self.error_codes[6]:
                                compatibility_print(error_message)

                # Get list of all files and directories from a path
                # Includes subdirectories recursively
                self.dirs_files_to_loop_through = []

                ###-->my_path, my_filename = self.convert_relative_path_to_absolute(path)

                ###-->self.add_references_to_read(my_path + ('' if my_filename == None else my_filename))
                self.add_references_to_read(path)

                ###-->self.path = my_path + ('' if my_filename == None else my_filename)

                if(3 in self.caught_errors):
                        compatibility_print("Corrected Path Without Spaces: >"+"<\n")

                if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                        pass
                elif(self.os_type == 'windows'):
                        pass

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

                # We should make this be manually called so dirs_files_to_loop_through can be built
                #self.get_all_file_info()

                time_end = datetime.datetime.now()
                run_time = (time_end - time_begin).seconds
		#compatibility_print("Initialized in: "+str(run_time)+" seconds.")

        def get_all_file_info(self):
                """
                Version 2 of this.  Decided to do the recursive search prior to reading in all the info.
                """
                # Run this if we have no files or directories yet
                if(len(self.dirs_files_to_loop_through) == 0):
                        self.add_references_to_read(self.path)

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

                        if(dir_or_file in self.delimiter_header_attempts):
                                for attempt in range(len(self.delimiter_header_attempts[dir_or_file])):
                                        if((self.delimiter_header_attempts[dir_or_file][attempt].success_percentage > most_success_percentage)
                                           or ((self.delimiter_header_attempts[dir_or_file][attempt].success_percentage >= most_success_percentage)
                                               and (len(most_success_delimiter) < len(self.delimiter_header_attempts[dir_or_file][attempt].delimiter)))
                                           or ((self.delimiter_header_attempts[dir_or_file][attempt].success_percentage == most_success_percentage)
                                               and (self.delimiter_header_attempts[dir_or_file][attempt].delimiter == '{}'))):
                                        #if(
                                        #        (self.delimiter_header_attempts[dir_or_file][attempt].success_percentage > most_success_percentage)
                                        #        or ((self.delimiter_header_attempts[dir_or_file][attempt].success_percentage >= most_success_percentage)
                                        #   and (len(most_success_delimiter) <= len(self.delimiter_header_attempts[dir_or_file][attempt].delimiter))
                                        #            and self.delimiter_header_attempts[dir_or_file][attempt].delimiter == '{}')):
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
                        

        def add_references_to_read(self,next_check):
                """
                Call this method to add a file / directory / and subdirectories to be read in
                """

                # Make absolute_path_to_file an absolute path to the file if it's not ...
                my_path, my_filename = self.convert_relative_path_to_absolute(next_check)
                next_check = my_path + ('' if my_filename == None else my_filename)

                # If we pass in a single file
                if os.path.isfile(next_check):
                        fail = '/' if(self.os_type == 'linux' or self.os_type == 'macintosh') else '\\'
                        absolute_path = next_check
                        if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                                absolute_path = absolute_path.replace('//','/')
                        elif(self.os_type == 'windows'):
                                absolute_path = absolute_path.replace('\\\\','\\')
                        
                        if(absolute_path not in self.dirs_files_to_loop_through):
                                self.dirs_files_to_loop_through.append(absolute_path)
                        
                # If we pass in a directory
                elif os.path.isdir(next_check):
                        for filename in os.listdir(next_check):
                                fail = '/' if(self.os_type == 'linux' or self.os_type == 'macintosh') else '\\'
                                absolute_path = next_check + fail + filename
                                if(self.os_type == 'linux' or self.os_type == 'macintosh'):
                                        absolute_path = absolute_path.replace('//','/')
                                elif(self.os_type == 'windows'):
                                        absolute_path = absolute_path.replace('\\\\','\\')

                                if(self.os_type == 'windows' and (next_check + filename)[-1] != '\\'):
                                        add_ending_slahes = '\\' if self.os_type == 'windows' else '/'
                                elif((self.os_type == 'linux' or self.os_type == 'macintosh') and (next_check + filename)[-1] != '\\'):
                                        add_ending_slahes = '\\' if self.os_type == 'windows' else '/'
                                
                                #if(os.path.isdir(absolute_path) and ((absolute_path) not in self.dirs_files_to_loop_through)):
                                if(os.path.isdir(next_check + filename + add_ending_slahes) and ((next_check + filename + add_ending_slahes) not in self.dirs_files_to_loop_through)):
                                        #pass
                                        #self.add_references_to_read(absolute_path)
                                        self.add_references_to_read(next_check  + filename + add_ending_slahes)
                                
                                if(absolute_path not in self.dirs_files_to_loop_through):
                                        self.dirs_files_to_loop_through.append(absolute_path)
                                #print(absolute_path)
                                #self.dirs_files_to_loop_through.append(next_check + filename)
                else:
                        #my_path, my_filename = self.convert_relative_path_to_absolute(next_check)
                        #next_check = my_path + '' if(my_filename == None) else my_filename
                        if ((7 not in self.caught_errors) and (next_check not in self.caught_errors_files_or_dirs)):
                                        self.caught_errors.append(7)
                                        self.caught_errors_files_or_dirs.append(next_check)
                                        for error_message in self.error_codes[7]:
                                                temp = error_message
                                                temp = temp.replace('REPLACE_WITH_my_path',my_path)
                                                temp = temp.replace('REPLACE_WITH_my_filename',my_filename)
                                                compatibility_print(temp)

        def attempt_to_read_file(self,absolute_path_to_file,headers,delimiter=None,lines_to_read=10000,read_header=False):
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
                        if(counter == -1 and read_header == False):
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

        def attempt_to_read_parameter_file(self,absolute_path_to_file,lines_to_read=10000):
                """
                Function to read in all the paramters to then do cool stuff like execute queries.
                Last Update: 03/01/2017
                By: LB023593
                """
            
                from os import getcwd
                from collections import defaultdict

                # Initialize variables
                charset_locs = defaultdict(list)
                parameter = defaultdict(list)
                charset_all_parameters = []
                parameter_search = defaultdict(list)
                parameters = defaultdict(list)
                charset = list(set(''))

                # namedtuple for delimiter success rate
                nt_ans = namedtuple('delimiter_success_ratios','success_percentage delimiter headers')

                # Open the file for reading from input_files
                readfile = open(absolute_path_to_file,'r')

                # Counts the number of lines with invalid paramters
                successful_insert = 0
                failure_insert = 0

                # Counts the number of lines in the file
                line_counter = 0
            
                # Go through each line in the file
                for line in readfile:

                        if(line_counter >= lines_to_read):
                                break
                        
                        # Clear these variables for each line
                        del charset
                        del charset_locs

                        line_counter += 1
                        charset_locs = defaultdict(list)
                        charset = list(set(line))

                        # Loop through the charset
                        for x in range(len(charset)):
                                charset_locs[charset[x]] = list(find_all_return_generator(line,charset[x]))

                                # Test to see if parameters were correctly entered
                                try:
                                        parameter_name_begin = int(charset_locs['{'][0])
                                        parameter_name_end = int(charset_locs['}'][0])
                                except:
                                        parameter_name_end = -1
                                        parameter_name_begin = -1

                        # If a parameter was not entered correctly save the paramter as the line of the file
                        if((parameter_name_end == -1 or parameter_name_begin == -1) or (parameter_name_end < parameter_name_begin)):
                                failure_insert += 1
                                
                                # Let's not include invalid lines for now
                                #parameters['invalid_line_'+str(line_counter)] = line.strip('\n')

                        # Else save the paramter
                        else:
                                # Make
                                parameter_search[line[int(parameter_name_begin)+1:int(parameter_name_end)]] = charset_locs
                                parameters[line[int(parameter_name_begin)+1:int(parameter_name_end)]] = line[charset_locs['}'][0]+1:].strip('\n')
                                successful_insert += 1

                # Close the file
                readfile.close()

                ## Save the data
                ##self.file_data[absolute_path_to_file] = parameters
                ##self.file_line_count[absolute_path_to_file] = line_counter
                ##self.file_histogram[absolute_path_to_file] = {}#histogram_ans

                try:
                        temp = (float(successful_insert))/float(line_counter)*100
                except ZeroDivisionError:
                        temp = float(0)

                return nt_ans(float("{0:.2f}".format(temp)),'{}','')

        def read_file(self,absolute_path_to_file,delimiter,header,read_header=False):
                """
                Reads in the data from the file.
                """

                ###--># Make absolute_path_to_file an absolute path to the file if it's not ...
                ###-->my_path, my_filename = self.convert_relative_path_to_absolute(absolute_path_to_file)
                ###-->absolute_path_to_file = my_path + my_filename

                if(delimiter == '{}'):
                        self.read_parameter_file(absolute_path_to_file)
                else:
                        self.read_delimiter_file(absolute_path_to_file,delimiter,header,read_header)

        def read_delimiter_file(self,absolute_path_to_file,delimiter,header,read_header=False):
                """
                Reads in the data from a delimited file.
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
                        #fix_start_with_underscore = '' if(len(each_header) == 0) else each_header + '_'
                        #print(fix_start_with_underscore)
                        #histogram_nt_header +=  fix_start_with_underscore + 'header_'+str(counter)+'_value_count header_' + str(counter) +'_duplicates '
                        histogram_nt_header +=  each_header + ' ' + each_header +'_duplicate_count '
                        nt_placeholder.append({})
                        nt_placeholder.append({'duplicate_count':0})
                        counter += 1
                histogram_nt_header = histogram_nt_header.strip()

                nt_histogram = namedtuple('duplicates',histogram_nt_header)

                #histogram_ans = nt_histogram(*[x for x in nt_placeholder])
                histogram_ans = {}

                # Count the lines we have read in
                counter = -1
		
                for line in readfile:
                        counter += 1
                        insert_status = False
                        if(counter == 0 and read_header == False):
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

                                                #print(str(value_counter),values,histogram_ans.keys())

                                                try:
                                                        if(header.split(' ')[value_counter] in histogram_ans):
                                                                histogram_ans[header.split(' ')[value_counter]][values] += 1
                                                                histogram_ans[header.split(' ')[value_counter] + '_duplicate_counter'] += 1
                                                        else:
                                                                histogram_ans[header.split(' ')[value_counter]] = {}
                                                                histogram_ans[header.split(' ')[value_counter]][values] = 1
                                                                histogram_ans[header.split(' ')[value_counter] + '_duplicate_counter'] = 0
                                                except:
                                                        histogram_ans[header.split(' ')[value_counter]][values] = 1
                                                        #print("Errored on:",values)
                                                        #print("Keys:")
                                                        #print(histogram_ans[header.split(' ')[value_counter]].keys())
                                                        #failll = raw_input("")

                                                value_counter += 1
                                                
                                                ###if(values in histogram_ans[value_counter]):
                                                ###        #if(value_counter == 0):
                                                ###        #        compatibility_print('Increment: ' + values + ' ' + str(histogram_ans[value_counter - 1]['duplicate_count']))
                                                ###        histogram_ans[value_counter][values] = histogram_ans[value_counter][values] + 1
                                                ###        histogram_ans[value_counter + 1]['duplicate_count'] = histogram_ans[value_counter + 1]['duplicate_count'] + 1
                                                ###
                                                ###else:
                                                ###        #if(value_counter == 0):
                                                ###        #        compatibility_print('Initialize: ' + values)
                                                ###        if(values not in histogram_ans[value_counter].keys()):
                                                ###                histogram_ans[value_counter][values] = 1

                                                #if(value_counter == 0):
                                                #        compatibility_print('Duplicate Count ' + str(histogram_ans[value_counter - 1]['duplicate_count']))
                                                ###value_counter += 2
                                        #except:
                                        #        #pass
                                        #        print([x.strip() for x in line.split(delimiter)])
                                
                try:
                        temp = (float(successful_insert))/float(counter)*100
                except ZeroDivisionError:
                        temp = float(0)

                self.file_data[absolute_path_to_file] = ans
                self.file_line_count[absolute_path_to_file] = counter
                self.file_histogram[absolute_path_to_file] = histogram_ans

                readfile.close()

        def read_all_files(self):
                """
                Reads in the data from all the files in the directory
                """
                time_begin = datetime.datetime.now()
		
                for file_key in self.file_list.keys():
                        if(self.file_list[file_key].type == 'File' and self.file_list[file_key].delimiter == '{}'):
                                self.read_parameter_file(self.file_list[file_key].directory + self.file_list[file_key].filename)
                                
                        elif(self.file_list[file_key].type == 'File'):
                                self.read_file(self.file_list[file_key].directory + self.file_list[file_key].filename,self.file_list[file_key].delimiter,self.file_list[file_key].header)

                time_end = datetime.datetime.now()
                run_time = (time_end - time_begin).seconds
		
                if(len(self.file_list.keys()) == 1):
                        compatibility_print("1 file read in: "+str(run_time)+" seconds.")
                else:
                        compatibility_print(str(len(self.file_list.keys())) + " files read in: "+str(run_time)+" seconds.")

        def read_parameter_file(self,absolute_path_to_file):
                """
                Function to read in all the paramters to then do cool stuff like execute queries.
                Last Update: 03/01/2017
                By: LB023593
                """

                from os import getcwd
                from collections import defaultdict

                # Initialize variables
                charset_locs = defaultdict(list)
                parameter = defaultdict(list)
                charset_all_parameters = []
                parameter_search = defaultdict(list)
                parameters = defaultdict(list)
                charset = list(set(''))

                # Open the file for reading from input_files
                readfile = open(absolute_path_to_file,'r')

                # Counts the number of lines with invalid paramters
                successful_insert = 0
                failure_insert = 0

                # Counts the number of lines in the file
                line_counter = 0
            
                # Go through each line in the file
                for line in readfile:
                        
                        # Clear these variables for each line
                        del charset
                        del charset_locs

                        line_counter += 1
                        charset_locs = defaultdict(list)
                        charset = list(set(line))

                        # Loop through the charset
                        for x in range(len(charset)):
                                charset_locs[charset[x]] = list(find_all_return_generator(line,charset[x]))

                                # Test to see if parameters were correctly entered
                                try:
                                        parameter_name_begin = int(charset_locs['{'][0])
                                        parameter_name_end = int(charset_locs['}'][0])
                                except:
                                        parameter_name_end = -1
                                        parameter_name_begin = -1

                        # If a parameter was not entered correctly save the paramter as the line of the file
                        if((parameter_name_end == -1 or parameter_name_begin == -1) or (parameter_name_end < parameter_name_begin)):
                                failure_insert += 1
                                parameters['invalid_line_'+str(line_counter)] = line.strip('\n')

                        # Else save the paramter
                        else:
                                # Make
                                parameter_search[line[int(parameter_name_begin)+1:int(parameter_name_end)]] = charset_locs
                                parameters[line[int(parameter_name_begin)+1:int(parameter_name_end)]] = line[charset_locs['}'][0]+1:].strip('\n')
                                #compatibility_print(line[charset_locs['}'][0]+1:].strip('\n'))
                                successful_insert += 1

                # Close the file
                readfile.close()

                # Save the data
                self.file_data[absolute_path_to_file] = parameters
                self.file_line_count[absolute_path_to_file] = line_counter
                self.file_histogram[absolute_path_to_file] = {}#histogram_ans

                try:
                        temp = (float(successful_insert))/float(line_counter)*100
                except ZeroDivisionError:
                        temp = float(0)

        def get_header_and_delimiter(self,absolute_path_to_file,delimiter=None):
                """
                Recursive method if no delimiter is passed in.
                """

                ###--># Make absolute_path_to_file an absolute path to the file if it's not ...
                ###-->my_path, my_filename = self.convert_relative_path_to_absolute(absolute_path_to_file)
                ###-->absolute_path_to_file = my_path + '' if my_filename == None else my_filename

                if(os.path.isdir(absolute_path_to_file)):
                        self.delimiter_header_attempts[absolute_path_to_file] = []
                elif(delimiter == None):
                        readfile = open(absolute_path_to_file,'r')
                        header = readfile.readline().strip()
                        readfile.close()
                        del readfile

                        # Default the file format to delimiter
                        # If any case below matches update it to desired format
                        file_format = 'delimiter'

                        # Check for filetypes that cannot be read in with a delimiter
                        if(len(header) == 0):
                                compatibility_print(absolute_path_to_file)
                                compatibility_print("Has no header")
                                file_format = 'unknown'
                        elif(('<?xml' in header) or (header[0] == '<' and header[-1] == '>')):
                                compatibility_print(absolute_path_to_file)
                                compatibility_print('Is an XML file and is not yet supported')
                                file_format = 'xml'
                        elif(('{"' in header) or ('{' == header)):
                                compatibility_print(absolute_path_to_file)
                                compatibility_print('Is a JSON file and is not yet supported')
                                file_format = 'json'
                        elif(('{' == header[0]) and ('}' in header)):
                                try:
                                        parameter_file_type_check = header[header.find('{')+1:header.find('}')]
                                        unique_chars_in_header = list(set(header))
                                        for char in list(set(header)):
                                                # Exclude a-z,A-Z,' ', '-', '_', or a number
                                                if((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or (ord(char) == 32)
                                                   or (ord(char) == 45) or (ord(char) == 95) or ((ord(char) >= 48) and (ord(char) <= 57))):
                                                        pass
                                                else:
                                                        parameter_file_type_check = False
                                                        break
                                        parameter_file_type_check = True
                                except:
                                        parameter_file_type_check = False

                                if(parameter_file_type_check):
                                        file_format = 'parameter'

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
                        # All alphanumeric chars will have a count of 0
                        for key in count_chars:
                                if(count_chars[key] == 0):
                                        pass
                                else:
                                        temp[key] = count_chars[key]
                        count_chars = temp

                        if(file_format == 'parameter'):
                                count_chars['{}'] = 1

                        # The below code could probably be in some kind of loop but hardcoding 2x to 5x seems decent enough for now
                        # Come back and check to see how many of the same character appear next to each other in a loop rather than hardcoded

                        # See if any double character is a delimiter
                        temp_additional_delimiter_dict = {}
                        for key in count_chars:
                                if key + key in header:
                                        temp_additional_delimiter_dict[key + key] = len(list(find_all_return_generator(header,key + key)))
                        for key in temp_additional_delimiter_dict:
                                count_chars[key] = temp_additional_delimiter_dict[key]

                        # See if any triple character is a delimiter
                        temp_additional_delimiter_dict = {}
                        for key in count_chars:
                                if key + key + key in header:
                                        temp_additional_delimiter_dict[key + key + key] = len(list(find_all_return_generator(header,key + key + key)))
                        for key in temp_additional_delimiter_dict:
                                count_chars[key] = temp_additional_delimiter_dict[key]

                        # See if any quadruple character is a delimiter
                        temp_additional_delimiter_dict = {}
                        for key in count_chars:
                                if key + key + key in header:
                                        temp_additional_delimiter_dict[key + key + key + key] = len(list(find_all_return_generator(header,key + key + key + key)))
                        for key in temp_additional_delimiter_dict:
                                count_chars[key] = temp_additional_delimiter_dict[key]

                        # See if any quintuple character is a delimiter
                        temp_additional_delimiter_dict = {}
                        for key in count_chars:
                                if key + key + key in header:
                                        temp_additional_delimiter_dict[key + key + key + key + key] = len(list(find_all_return_generator(header,key + key + key + key + key)))
                        for key in temp_additional_delimiter_dict:
                                count_chars[key] = temp_additional_delimiter_dict[key]

                        # Somewhere around right here check if another file_format besides delimiter was found
                        # Write method to record it's success ratio for it to be considered when reading in the file

                        # Recursively call this method
                        # Record each delimiter attempt and it's success ratio
                        # The most successful delimiter will be used to read in the whole file
                        for test_delimiter in count_chars:
                                self.get_header_and_delimiter(absolute_path_to_file,test_delimiter)
                                
                elif(delimiter == '{}'):

                        if(absolute_path_to_file in self.delimiter_header_attempts):
                                self.delimiter_header_attempts[absolute_path_to_file].append(self.attempt_to_read_parameter_file(absolute_path_to_file))
                        else:
                                self.delimiter_header_attempts[absolute_path_to_file] = []
                                self.delimiter_header_attempts[absolute_path_to_file].append(self.attempt_to_read_parameter_file(absolute_path_to_file))
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

        def convert_relative_path_to_absolute(self,path):
                """
                Return the Path and Filename from {path}

                Assumptions
                1)  Filenames with two dots '..' are not supported except to represent going up a directory
                """

                # Initialize for return values - mainly needed if self.os_type is 'invalid'
                my_filename = ''
                my_path = ''

                # Find all the up-one-directories
                double_dot_locs = list(find_all_return_generator(path,'..'))
                
                if(self.os_type == 'linux'):
                        temp_path = path.replace('//','/')
                        temp_path_slash_locs = list(find_all_return_generator(temp_path,'/'))
                        my_filename = temp_path[temp_path_slash_locs[-1]+1:]

                        # If we are given a relative path make it an absolute path
                        if(len(double_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'/'))
                                my_path = getcwd()[:getcwd_slash_locs[-len(double_dot_locs)]] + temp_path[double_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '/'
                        else:
                                my_path = temp_path

                        # I am lazy - really lazy ...
                        # If the filename is at the end - remove it
                        my_path = my_path.replace(my_filename, '')

                        # Detect what we were given
                        if(os.path.isdir(my_path + my_filename)):
                                my_path_type = 'directory'
                                my_filename = None
                                # We're good.  We want the just the path - and not the filename here
                        elif(os.path.isfile(my_path + my_filename)):
                                my_path_type = 'file'
                                path_slash_locs = list(find_all_return_generator(my_path,'/'))
                                my_path = my_path[:path_slash_locs[-1]] + '/'
                        else:
                                my_path_type = 'invalid'
                                if ((7 not in self.caught_errors) and ((my_path + my_filename) not in self.caught_errors_files_or_dirs)):
                                        self.caught_errors.append(7)
                                        self.caught_errors_files_or_dirs.append(my_path + my_filename)
                                        for error_message in self.error_codes[7]:
                                                temp = error_message
                                                temp = temp.replace('REPLACE_WITH_my_path',my_path)
                                                temp = temp.replace('REPLACE_WITH_my_filename',my_filename)
                                                compatibility_print(temp)
                                
                elif(self.os_type == 'windows'):
                        # If the file in on a Network Share add back the second set of double slashes
                        if(path[0:2] == '\\\\'):
                                temp_path = '\\' + path.replace('\\\\','\\')
                        else:
                                temp_path = path.replace('\\\\','\\')
                        #print('0',temp_path)
                        temp_path_slash_locs = list(find_all_return_generator(temp_path,'\\'))
			#print('1',temp_path_slash_locs)
                        my_filename = temp_path[temp_path_slash_locs[-1]+1:]
                        #print('2',my_filename)

                        # If we are given a relative path make it an absolute path
                        if(len(double_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'\\'))
                                my_path = getcwd()[:getcwd_slash_locs[-len(double_dot_locs)]] + temp_path[double_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '\\'
                        else:
                                my_path = temp_path

                        # I am lazy - really lazy ...
                        # This will remove the filename from the end of the path if it's there
                        my_path = my_path.replace(my_filename, '')

                        if(os.path.isdir(my_path + my_filename)):
                                my_path_type = 'directory'
                                my_filename = None
                                # We're good.  We want the just the path - and not the filename here
                        elif(os.path.isfile(my_path + my_filename)):
                                my_path_type = 'file'
                                path_slash_locs = list(find_all_return_generator(my_path,'\\'))
                                my_path = my_path[:path_slash_locs[-1]] + '\\'
                        else:
                                # Scenario to handle a directory or path which does not exist
                                my_path_type = 'invalid'
                                if((7 not in self.caught_errors) and (my_path + my_filename not in self.caught_errors_files_or_dirs)):
                                        self.caught_errors.append(7)
                                        self.caught_errors_files_or_dirs.append(my_path + my_filename)
                                        for error_message in self.error_codes[7]:
                                                temp = error_message
                                                temp = temp.replace('REPLACE_WITH_my_path',my_path)
                                                temp = temp.replace('REPLACE_WITH_my_filename',my_filename)
                                                compatibility_print(temp)
                                
                elif(self.os_type == 'macintosh'):
			
                        temp_path_slash_locs = list(find_all_return_generator(temp_path,'/'))
                        my_filename = temp_path[temp_path_slash_locs[-1]+1:]

                        # If we are given a relative path make it an absolute path
                        if(len(double_dot_locs) > 0):
                                getcwd_slash_locs = list(find_all_return_generator(getcwd(),'/'))
                                my_path = getcwd()[:getcwd_slash_locs[-len(double_dot_locs)]] + temp_path[double_dot_locs[-1]+2:temp_path_slash_locs[-1]] + '/'
                        else:
                                my_path = temp_path

                        # I am lazy - really lazy ...
                        # This will remove the filename from the end of the path if it's there
                        my_path = my_path.replace(my_filename, '')

                        if(os.path.isdir(my_path + my_filename)):
                                my_path_type = 'directory'
                                my_filename = None
                                # We're good.  We want the just the path - and not the filename here
                        elif(os.path.isfile(my_path + my_filename)):
                                my_path_type = 'file'
                                path_slash_locs = list(find_all_return_generator(my_path,'/'))
                                my_path = my_path[:path_slash_locs[-1]] + '/'
                        else:
                                my_path_type = 'invalid'
                                if ((7 not in self.caught_errors) and (next_check not in self.caught_errors_files_or_dirs)):
                                        self.caught_errors.append(7)
                                        self.caught_errors_files_or_dirs.append(next_check)
                                        for error_message in self.error_codes[7]:
                                                temp = error_message
                                                temp = temp.replace('REPLACE_WITH_my_path',my_path)
                                                temp = temp.replace('REPLACE_WITH_my_filename',my_filename)
                                                compatibility_print(temp)
                else:
                        self.caught_errors.append(6)
                        for error_message in self.error_codes[6]:
                                compatibility_print(error_message)

                return my_path, my_filename

        def show_unique_columns(self):
                for file_key in self.file_list.keys():
                        found = False
                        unique_columns = []
                        compatibility_print(file_key)
                        for column in self.file_list[file_key].header.split(' '):
                                if((len(self.file_list[file_key].delimiter) == 1) and (self.file_histogram[file_key][column + '_duplicate_counter'] == 0)):
                                        found = True
                                        unique_columns.append(column)
                        if(found):
                                compatibility_print("Has the following unique columns:")
                                for found_unique_column in unique_columns:
                                        compatibility_print(found_unique_column)
                        elif((found == False) and (self.file_list[file_key].delimiter == '{}')):
                                compatibility_print("Unique Columns Not Applicable")
                        else:        
                                compatibility_print("Has no unique columns")
                        compatibility_print("")

        def show_file_summary(self):
                for file_key in self.file_list.keys():
                        compatibility_print('[' + ('-'*78) + ']')
                        compatibility_print(file_key)
                        compatibility_print("Lines Read In:" + " "*(23 - len(str(self.file_line_count[file_key]))) + str(self.file_line_count[file_key]))
                        compatibility_print("Success Percentage:" + " "*(20 - len(str(self.file_list[file_key].success_percentage))) + str(self.file_list[file_key].success_percentage) + '%')
                        if(self.file_list[file_key].delimiter == '{}'):
                                pass
                        else:
                                compatibility_print("")
                                compatibility_print("Column" + " "*(50 - len("Column")) + "Duplicate Count" + " "*(25 - len("Duplicate Count")) + "Ratio")
                                compatibility_print("")
                                for each_header in self.file_list[file_key].header.split(' '):
                                        try:
                                                column_unique_ratio = (float(self.file_histogram[file_key][each_header + '_duplicate_counter']))/float(self.file_line_count[file_key])*100
                                        except ZeroDivisionError:
                                                column_unique_ratio = 0

                                        spacing_1 = len(each_header)
                                        spacing_2 = len(str(self.file_histogram[file_key][each_header + '_duplicate_counter']))
                                        spacing_3 = len(str(float("{0:.2f}".format(column_unique_ratio))))
                                
                                        compatibility_print(each_header
                                                            + " "*(50 - spacing_1)
                                                            +str(self.file_histogram[file_key][each_header + '_duplicate_counter']) + " "*(15 - spacing_2)
                                                            + " "*(15 - spacing_3) + str(float("{0:.2f}".format(column_unique_ratio))) + '%')
                        compatibility_print("")


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

        
