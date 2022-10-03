
## Import essential packages
import os
import re
import math
import sys
import logging
# would be good to make qt/slicer optional so we can make broader use of code.
# import qt
# import slicer

from manager import manager
from AtlasController import AtlasController
from DataPackageMenu import DataPackageMenu
from FiducialClickerMenu import FiducialClickerMenu
from conf import conf

# currently disabled because the update work is unfinished.
update_checking = False
"""
code_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(code_directory))
from ndLibrarySupport import *
"""

def update_check(code_directory,remote_name='origin'):
    try:
        import git
    except ImportError:
        print(" git unavailable, cannot check for updates of "+code_directory)
        return None
    try:
        repo = git.Repo(code_directory)
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

# TODO: this is the wrong way to setup the code library. learn how to
"""
## Find code and execute it
print("ndLibrarySupport: setup code from "+code_directory)
code_file=''
for code_file in os.listdir(code_directory):
    if '__init__' in code_file:
        continue
    if os.path.isdir(os.path.join(code_directory, code_file)) or not re.match(r''+r".*[.]py$", code_file):
        continue
    #print("exec(open(r\""+os.path.join(code_directory, code_file)+"\").read())")
    try:
        #import importlib.util
        #spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
        #spec = importlib.util.spec_from_file_location(file, os.path.join(code_directory, file))
        #foo = importlib.util.module_from_spec(spec)
        #spec.loader.exec_module(foo)
        print(code_file)
        if (sys.version_info > (3, 0)):
            exec(open(os.path.join(code_directory, code_file)).read())
        else:
            execfile(os.path.join(code_directory, code_file))
    except:
        print("Code start error in file "+code_file+" from "+code_directory)
print("ndLibrarySupport import complete")
if update_checking:
    try:
        update_available = update_check(code_directory)
        if update_available is not None:
            import git
            print("Code could be updated, installing buttons")
            ## add a toolbar
            ## add a button with text "Update ndLibrarySupport"
    except:
        # our update check should absolutely not prevent running, ever.
        pass
"""