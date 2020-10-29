
## To run, type: exec(open(r"h:\code\ndLibrarySupport\Testing\ndLibrary_Test.py").read())
## Author: Austin Kao
import sys;import os;sys.path.append(r"h:\code");import ndLibrarySupport;
exec(open(os.path.join(ndLibrarySupport.codePath,"ndLibrary.py")).read())
f = ndLibrary(None, r"D:\Libraries\010Rat_Brain")
print("C"+len(f.children))
#f.children[0].conf_dir
lib=f.children[0]
len(lib.children)

lib=lib.children[0]
lib.volDict
for vol in lib.volDict:
    print(vol)

filter=lib.fields["FilePattern"]
pattern=lib.fields["FileAbrevPattern"]
match=lib.fields["FileAbrevMatch"]
lib.jumpToDir()
libEntries = [f for f in os.listdir(os.getcwd()) if re.match(r''+filter, f) and not os.path.isdir(os.path.join(os.getcwd(),f))]

#f = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-10-16\23Rat")
#f = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\23Rat")
#f = ndLibrary(None, r"D:\CIVM_Apps\Slicer\FiberCompareViewTestData\\090_Heritability")
#print("Testing loading of a conf file")
#f.loadConf(r"D:\Libraries\010Rat_Brain\lib.conf")
#print("Testing building children")
#f.buildChildren()
#print("Testing loading entire tree")
#f.loadEntire()
print("End of test")
