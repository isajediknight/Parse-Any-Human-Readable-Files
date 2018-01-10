# Testing Code
# run by typing:
# python test.py

import sys
from platform import python_version
if (sys.platform.lower().startswith('linux')):
    my_platform = 'linux'
elif (sys.platform.lower().startswith('win')):
    my_platform = 'win'
elif (sys.platform.lower().startswith('mac')):
    my_platform = 'mac'
else:
    my_platform = 'unknown'

if((my_platform == 'linux')):
    sys.path.insert(0,'../class_files/')
elif((my_platform == 'win')):
    sys.path.insert(0,'..\\class_files\\')
from histogram import *

from os import getcwd

if(my_platform == 'linux'):
    #a = histogram('/home/luke/')
    #b = histogram('.Xauthority')
    #c = histogram('/home/luke')
    #d = histogram('//home//luke')
    #e = histogram('//home//luke//')
    #f = histogram('/home/luke/.XauthoRITY')
    #g = histogram('/home/luke/.Xauthority')
    h = histogram('/home/luke/github/readitall/class_files/file_1.txt')
    #c.get_file_list()
    #print(len(c.file_list))
    print h.file_list
    
elif(my_platform == 'win'):
    #a = histogram('..\\input_files\\file_1.txt')
    #b = histogram('..\\input_files\\file_2.txt')
    #c = histogram('..\\input_files\\file_3.txt')
    #d = histogram('..\\..\\input_files\\file_1.txt')
    #e = histogram('..\\..\\..\\input_files\\good_times\\file_1.txt')
    #f = histogram('E:\\Coding\\Github\\Parse-Any-Human-Readable-Files\\input_files\\file_1.txt')
    a = histogram('..\\input_files\\commits_since_last_release_by_commit.input')
    b = histogram('..\\input_files\\commits_since_last_release_by_timestamp.input')
    c = histogram('..\\input_files\\parent_branches.txt')
    d = histogram('..\\input_files\\latest_commit.input')

    #a = f.attempt_to_read_file(f.path + f.filename,'_',' '.join(f.get_headers(f.path + f.filename)))
    #b = f.attempt_to_read_file(f.path + f.filename,',',' '.join(f.get_headers(f.path + f.filename,',')))
    #c = f.attempt_to_read_file(f.path + f.filename,'|',' '.join(f.get_headers(f.path + f.filename,'|')))
else:
    print("Unknown OS")
