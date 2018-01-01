# Testing Code
# run by typing:
# python test.py

import sys
from platform import python_version
if (sys.platform.lower().startswith('linux')):
    my_platform = 'linux'
elif (sys.platform.lower().startswith('win')):
    my_platform = 'win'
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
    a = histogram('..\\input_files\\file_1.txt')
    #b = histogram('.Xauthority')
    #c = histogram('/home/luke')
    #d = histogram('//home//luke')
    #e = histogram('//home//luke//')
    #f = histogram('/home/luke/.XauthoRITY')
    #g = histogram('/home/luke/.Xauthority')
    #h = histogram('E:\\Coding\\Github\\Parse-Any-Human-Readable-Files\\input_files\\file_1.txt')
    #c.get_file_list()
    #print(len(c.file_list))
    #h.get_primary_key()
    #print h.file_list

else:
    print("Unknown OS")
