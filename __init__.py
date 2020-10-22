
## Import essential packages
import os
import re
import math
import sys
import logging
import qt
import slicer

#import inspect
#from pathlib import Path

# import without destroying __file__
#   import sys;sys.path.append(r"h:\code");import ndLibrarySupport;ndman=ndLibrarySupport.manager(r"D:\Libraries\010Rat_Brain\v2020-06-25");ndman
#   import sys;sys.path.append(r"h:\code");import ndLibrarySupport;ndman=ndLibrarySupport.manager(r"D:\Libraries\010Rat_Brain\v2020-06-25");ndman;ndman=ndLibrarySupport.manager(r"D:\Libraries\040Human_Brainstem");ndman
#       
#   import sys;sys.path.append(r"h:\code\ndLibraryViewer");sys.path.append(r"h:\code\ndLibraryViewer\Testing");import slicerrc_copy
#rootDir = r"D:\Libraries\040Human_Brainstem"
#rootDir = r"D:\Libraries\010Rat_Brain\v2020-06-25"

#class ndLibraryViewer:
#def __init__(self,rootDir):
codePath = os.path.dirname(os.path.abspath(__file__))
## Find code and execute it
print("ndLibrarySupport: setup code from "+codePath)
for file in os.listdir(codePath):
    if '__init__' in file:
        continue
    if os.path.isdir(os.path.join(codePath, file)) or not re.match(r''+r".*[.]py$", file):
        continue
    #print("exec(open(r\""+os.path.join(codePath, file)+"\").read())")
    try:
        #import importlib.util
        #spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
        #spec = importlib.util.spec_from_file_location(file, os.path.join(codePath, file))
        #foo = importlib.util.module_from_spec(spec)
        #spec.loader.exec_module(foo)
        exec(open(os.path.join(codePath, file)).read())
        #print(".")
        pass
    except:
        print("Code start error in file "+file+" from "+codePath)
        #return
