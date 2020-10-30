
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


def update_check(codePath,remote_name='origin'):
    try:
        import git
    except ImportError:
        print(" git unavailable, cannot check for updates of "+codePath)
        return None
    try:
        repo = git.Repo(codePath)
    except:
        return None
    # git fetch
    try:
        origin=repo.remote(remote_name)
    except:
        return None
    repo.origin=origin
    fetch_res=repo.origin.fetch()
    repo.fetch_res=fetch_res
    #commits_behind = repo.iter_commits('master..origin/master')
    local_name=str(repo.heads[0])
    remote_name=str(origin.refs[0])
    commits_behind = repo.iter_commits(local_name,remote_name)
    bcount = sum(1 for c in commits_behind)
    #commits_ahead = repo.iter_commits('origin/master..master')
    commits_ahead = repo.iter_commits(remote_name,local_name)
    acount = sum(1 for c in commits_ahead)
    if acount > 0:
        print("Cool! you've made some changes! If you feel like they should be integrated, feel free to fork and issue a pull request!")
    if bcount > 0:
        return repo
    return None

def code_update(repo):
    # git 
    return

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
        if (sys.version_info > (3, 0)):
            exec(open(os.path.join(codePath, file)).read())
        else:
            execfile(os.path.join(codePath, file))
        #print(".")
        pass
    except:
        print("Code start error in file "+file+" from "+codePath)
        #return

try:
    update_available = update_check(codePath)
    if update_available is not None:
        import git
        print("Code could be updated, installing buttons")
        ## add a toolbar
        ## add a button with text "Update ndLibrarySupport"
except:
    # our update check should absolutely not prevent running, ever.
    pass



