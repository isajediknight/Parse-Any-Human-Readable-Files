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
    #c.get_file_list()'C:\\Users\\LB023593\\Documents\\Stories\\Public_Github\\Parse-Any-Human-Readable-Files\\input_files\\file_1.txt'
    #print(len(c.file_list))
    print h.file_list
    
elif(my_platform == 'win'):
    z = histogram('..\\input_files\\file_1.txt')
    z.read_file(z.file_list.keys()[0],z.file_list[z.file_list.keys()[0]].delimiter,z.file_list[z.file_list.keys()[0]].header)
    #b = histogram('..\\input_files\\file_2.txt')
    #c = histogram('..\\input_files\\file_3.txt')
    #d = histogram('..\\..\\input_files\\file_1.txt')
    #e = histogram('..\\..\\..\\input_files\\good_times\\file_1.txt')
    #f = histogram('E:\\Coding\\Github\\Parse-Any-Human-Readable-Files\\input_files\\file_1.txt')
    ##a = histogram('..\\input_files\\commits_since_last_release_by_commit.input')
    ##a.read_file(a.file_list.keys()[0],a.file_list[a.file_list.keys()[0]].delimiter,a.file_list[a.file_list.keys()[0]].header)
    #a.file_data[a.file_data.keys()[0]][1]

    ##b = histogram('..\\input_files\\commits_since_last_release_by_timestamp.input')
    ##b.read_file(b.file_list.keys()[0],b.file_list[b.file_list.keys()[0]].delimiter,b.file_list[b.file_list.keys()[0]].header)
    #b.file_data[b.file_data.keys()[0]][0]

    ##c = histogram('..\\input_files\\parent_branches.txt')
    ##c.read_file(c.file_list.keys()[0],c.file_list[c.file_list.keys()[0]].delimiter,c.file_list[c.file_list.keys()[0]].header)
    #c.file_data[c.file_data.keys()[0]][5]

    ##d = histogram('..\\input_files\\latest_commit.input')
    ##d.read_file(d.file_list.keys()[0],d.file_list[d.file_list.keys()[0]].delimiter,d.file_list[d.file_list.keys()[0]].header)
    #d.file_data[d.file_data.keys()[0]][0]

    #a = f.attempt_to_read_file(f.path + f.filename,'_',' '.join(f.get_headers(f.path + f.filename)))
    #b = f.attempt_to_read_file(f.path + f.filename,',',' '.join(f.get_headers(f.path + f.filename,',')))
    #c = f.attempt_to_read_file(f.path + f.filename,'|',' '.join(f.get_headers(f.path + f.filename,'|')))
else:
    print("Unknown OS")
