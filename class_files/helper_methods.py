# Collection of helper methods

from platform import python_version

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
            print string
        else:
            print string+end
    elif(python_version().find('3.') > -1):
        if(end == "\n" or end == '\n'):
            print(string)
        else:
            print(string,end)
    else:
	    print("Compatibility Print for " + python_version() + " is not yet supported.")
