# Collection of helper methods

from platform import python_version
import datetime, time

def find_all_return_generator(string, search_for):
    """
    Returns a generator of the found locations of search_for within string.
    It is sometimes helpful to cast this as a list
    """
    start = 0
    while True:
        start = string.find(search_for, start)
        if(start == -1): return
        yield start
        start += 1

# Will use the correct print command depending if you are using Python 2.x or 3.x
# Works with only major versions of Python.  IE: Python 2.4 print worked differently than 2.7
def compatibility_print(string,end="\n"):
    """
    Compatibility between 2.x and 3.x for print statements.  Yes isajediknight knows 3.x can print 2.x print statements however
    I've found it harder to read.
    """
    if(python_version().find('2.') > -1):
        if(end == "\n" or end == '\n'):
            print(string)
        else:
            print(string+end)
    elif(python_version().find('3.') > -1):
        if(end == "\n" or end == '\n'):
            print(string)
        else:
            print(string,end)
    else:
	    print("Compatibility Print for " + python_version() + " is not yet supported.")

def get_datetime_formats():
    datetime_formats = []

    #Date formats
    datetime_formats.append((('%d','%m','%y'),'Date'))
    datetime_formats.append((('%d','%m','%Y'),'Date'))
    datetime_formats.append((('%Y','%m','%d'),'Date'))
    datetime_formats.append((('%y','%m','%d'),'Date'))
    datetime_formats.append((('%m','%d','%Y'),'Date'))
    datetime_formats.append((('%m','%d','%y'),'Date'))

    #Datetime formats
    datetime_formats.append((('%d','%m','%Y %H:%M:%S'),'Datetime'))
    datetime_formats.append((('%d','%b','%Y %H:%M:%S'),'Datetime'))
    datetime_formats.append((('%Y','%m','%d %H:%M:%S'),'Datetime'))
    datetime_formats.append((('%m','%d','%Y %H:%M:%S'),'Datetime'))
    datetime_formats.append((('%m','%d','%y %H:%M:%S'),'Datetime'))

    datetime_formats.append((('%d','%m','%Y %H:%M:%S.%f'),'Datetime'))
    datetime_formats.append((('%d','%b','%Y %H:%M:%S.%f'),'Datetime'))
    datetime_formats.append((('%Y','%m','%d %H:%M:%S.%f'),'Datetime'))
    datetime_formats.append((('%m','%d','%Y %H:%M:%S.%f'),'Datetime'))
    datetime_formats.append((('%m','%d','%y %H:%M:%S.%f'),'Datetime'))

    datetime_formats.append((('%d','%m','%Y %H:%M:%S %p'),'Datetime'))
    datetime_formats.append((('%d','%b','%Y %H:%M:%S %p'),'Datetime'))
    datetime_formats.append((('%Y','%m','%d %H:%M:%S %p'),'Datetime'))
    datetime_formats.append((('%m','%d','%Y %H:%M:%S %p'),'Datetime'))
    datetime_formats.append((('%m','%d','%y %H:%M:%S %p'),'Datetime'))

    datetime_formats.append((('%d','%m','%Y %H:%M:%S.%f %p'),'Datetime'))
    datetime_formats.append((('%d','%b','%Y %H:%M:%S.%f %p'),'Datetime'))
    datetime_formats.append((('%Y','%m','%d %H:%M:%S.%f %p'),'Datetime'))
    datetime_formats.append((('%m','%d','%Y %H:%M:%S.%f %p'),'Datetime'))
    datetime_formats.append((('%m','%d','%y %H:%M:%S.%f %p'),'Datetime'))

    datetime_formats.append((('%Y','%m','%dT%H:%M:%S.%f'),'Datetime'))#ISO
    datetime_formats.append((('%Y','%m','%dT%H:%M:%S.%fZ'),'Datetime'))#ISO

    

    #Time formats
    datetime_formats.append((('%H:%M:%S'),'Time'))
    datetime_formats.append((('%H:%M:%S %p'),'Time'))
    datetime_formats.append((('%H:%M:%S.%f'),'Time'))
    datetime_formats.append((('%H:%M:%S.%f %p'),'Time'))
    #datetime_formats.append(((),'Time'))
    
    #datetime_formats.append()

    return datetime_formats


def determine_if_datetime(datetime_data):
    possible_datetime_delimiters = ('-','/')

    datetime_formats = get_datetime_formats()
    
    datetime_delimiter_found = False
    datetime_delimiter = ''
    index = 0

    #Determining datetime delimiter
    for character in datetime_data:
        if datetime_delimiter_found == True:
            break
        else:
            for delimiter in possible_datetime_delimiters: 
                if possible_datetime_delimiters[index] == character:
                    datetime_delimiter = possible_datetime_delimiters[index]
                    datetime_delimiter_found = True
                    break
                else:
                    index += 1
        index = 0

    #EC-DM
    for datetime_format in get_datetime_formats():
        if datetime_format[1] != 'Time':
            if datetime_delimiter != '':
                datetime_string = datetime_delimiter.join(datetime_format[0])
                try: 
                    datetime.datetime.strptime(datetime_data, datetime_string)
                    #print(datetime_format[1])#DB-DM
                    return datetime_format[1]
                except ValueError as v:
                    if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                        #error_message = str(v.args[0]).replace('l','1') #INOC-DM
                        error_message = str(v.args[0])
                        error_value = str(error_message.replace('unconverted data remains: ','')).strip()
                        #print('new message:' + error_value) #DB-DM
                        try:
                            float_test = float(error_value)
                            #print('CAUGHT2')#DB-DM #RL
                            #print(datetime_format[1]) #DB-DM #RL
                            return datetime_format[1]
                        except:
                            #print('pass')#DB-DM
                            pass
                    else:                        
                        pass
            else:
                pass
            
        else:
            datetime_string = datetime_format[0]
            try:
                time.strptime(datetime_data, datetime_string)
                #print(datetime_format[1])#DB-DM
                return datetime_format[1]
            except ValueError as v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    #error_message = str(v.args[0]).replace('l','1') #unsure why the compiler returns Ls instead of 1s... #INOC-DM
                    error_value = str(error_message.replace('unconverted data remains: ','')).strip()
                    try:
                        float_test = float(error_value)
                        #print(datetime_format[1]) #DB-DM #RL
                        return datetime_format[1]
                    except:
                        pass
                else:                        
                    pass

        #print('No datetime format matched')#DB-DM
                                               

def determine_datatype(data):
    #print("**Determining data type of: ", data)

    #String test
    try:
        str(data)
        #print("Possibly a string")
        possible_str = True
    except:
        #print("Undetermined Data Type")
        possible_str = False
    
    #Int test
    try:
        if str.isdigit(str(abs(int(data)))) == True:
            possible_int = True
            #print("Possibly an integer")
        else:
            possible_int = False
            #print("Not an integer")
    except:
        #print("Not an integer ")
        possible_int = False
        
    #Float test
    try:
        float(abs(float(data)))
        #print("Possibly a float")
        possible_float = True
    except:
        #print("Not a float")
        possible_float = False
        
    #Bool test
    if str(data).lower() == "true" or str(data).lower() == "false":
        #print("Possibly a bool")
        possible_bool = True
    else:
        possible_bool = False

    #Tuple test
    left_paren_present = False
    right_paren_present = False
    data_string = str(data)
    for character in data_string:
        if str(data)[0] == '(':
            left_paren_present = True
        if str(data)[len(str(data)) - 1] == ')':
            right_paren_present = True
    if left_paren_present == True and right_paren_present == True:
        #print("Possibly a tuple")
        possible_tuple = True
    else:
        #print("Not a tuple")
        possible_tuple = False

    #Datetime test

    #Checks data for datetime delimiters to see if it's a possible datetime
    possible_datetime = False
    datetime_delimiters = ('/','-',':')
    datetime_delimiter_count = 0
    for character in data:
        if possible_datetime == True:
            break
        else:
            for delimiter in datetime_delimiters:
                if datetime_delimiter_count > 1:
                    possible_datetime = True
                    break
                else:
                    if character == delimiter:
                        datetime_delimiter_count += 1

    datetime_test_result = None

    #If data is a possible datetime, undergoes more tests to determine which datetime type it is specifically
    if possible_datetime:
        #print("EXECUTING DETERMINE_IF_DATETIME for: " + data)#DB-DM
        datetime_test_result = determine_if_datetime(data)
    
   # datetime_test_result = determine_if_datetime(data)
        
    if datetime_test_result == 'Datetime':
        #print("Possibly a datetime")
        possible_datetime = True
        possible_date = False
        possible_time = False
    elif datetime_test_result == 'Date':
        possible_date = True
        possible_datetime = False
        possible_time = False
    elif datetime_test_result == 'Time':
        possible_time = True
        possible_datetime = False
        possible_date = False
    else:
        possible_datetime = False
        possible_date = False
        possible_time = False


    #determining possibilities
    if possible_str == True:
        if possible_bool == True:
            #print("**Individual data reading completed for: " + data + "(bool)") #DB
            return type(True)
        elif possible_tuple == True:
            #print("**Individual data reading completed for: " + data + "(tuple)")#DB
            return type((0,1,3))
        elif possible_datetime == True:
            #print("**Individual data reading completed for: " + data + "(datetime)")#DB
            return type(datetime.datetime(2000,2,2))
        elif possible_date == True:
            #print("**Individual data reading completed for: " + data + "(date)")#DB
            return type(datetime.date(2000,2,2))
        elif possible_time == True:
            #print("**Individual data reading completed for: " + data + "(time)")#DB
            return type(datetime.time(5,30,2))
        elif possible_int == True:
            return type(1)
        elif possible_float == True:
            return type(0.3)
        else:
            #print("**Individual data reading completed for: " + data + "(string)")
            return type("")
    else:
        return None


