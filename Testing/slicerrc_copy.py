## File that runs at the startup of 3D Slicer
## Author: Austin Kao

## Import essential packages
import os
import re
import math
import sys
import qt
import slicer


#import inspect
#from pathlib import Path

# import without destroying __file__
#   import sys;sys.path.append(r"h:\code\ndLibraryViewer");sys.path.append(r"h:\code\ndLibraryViewer\Testing");import slicerrc_copy
## Specify the path to the code and the path to the root ndLibrary in question
#codePath = r"h:\code\ndLibraryViewer"

#codePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
codePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#rootDir = r"D:\Libraries\040Human_Brainstem"
rootDir = r"D:\Libraries\010Rat_Brain\v2020-06-25"

## Find code and execute it
isPy2 = '2.7' in sys.version
print("setup code from "+codePath)
for file in os.listdir(codePath):
    if os.path.isdir(os.path.join(codePath, file)):
        continue
    if isPy2 and 'ndLibrary_Python3.py' in file:
        continue
    if not isPy2 and 'ndLibrary.py' in file:
        continue
    try:
    #if 1 :
        #import importlib.util
        #spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
        #spec = importlib.util.spec_from_file_location(file, os.path.join(codePath, file))
        #foo = importlib.util.module_from_spec(spec)
        #spec.loader.exec_module(foo)
        exec(open(os.path.join(codePath, file)).read())
    except:
        print("Couldn't open "+file+" from "+codePath)
        print("exec(open(r\""+os.path.join(codePath, file)+"\").read())")

## Initialize the ndLibrary viewer
initializeNDLibraryViewer(rootDir)
