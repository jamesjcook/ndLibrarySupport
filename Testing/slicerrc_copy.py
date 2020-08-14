## File that runs at the startup of 3D Slicer
## Author: Austin Kao

## Import essential packages
import os
import re
import math
import sys

## Specify the path to the code and the path to the root ndLibrary in question
codePath = "D:\CIVM_Apps\Slicer\\ndLibraryViewer"
#rootDir = r"D:\Libraries\040Human_Brainstem"
rootDir = r"D:\Libraries\010Rat_Brain\v2020-06-25"

## Find code and execute it
notPython3 = '2.7' in sys.version
for file in os.listdir(codePath):
    if os.path.isdir(os.path.join(codePath, file)):
        continue
    if notPython3 and 'ndLibrary_Python3.py' in file:
        continue
    if not notPython3 and 'ndLibrary.py' in file:
        continue
    exec(open(os.path.join(codePath, file)).read())

## Initialize the ndLibrary viewer
initializeNDLibraryViewer(rootDir)