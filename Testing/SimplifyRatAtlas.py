

import sys
import os
# moving torwards finalized build direct behavior where this script is given
# as a run argument to slicer instead of copy-paste called.
# run using   slicer.exe -c SimplifyRatAtlas.py
try:
# implicit path 
    aux_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(os.path.dirname(aux_dir)))
    import ndLibrarySupport
except:
    # in-dev path hard path
    print("DEV CODE PATH")
    sys.path.append(r"h:\code")
    import ndLibrarySupport

dev_root = r"D:\Libraries\010Rat_Brain"
dist_root = r"D:\Libraries\SimplifiedDistributions"
## ex simplify with auto-resolve internal name for master collection
#simplify_job = ndLibrarySupport.simplify(dev_root, dist_root, True)
## simplify with prescribed name for master collection
dest_lib = os.path.join(dist_root,"RatBrain_v2021-05-21")
simplify_job = ndLibrarySupport.simplify(dev_root, dest_lib)
## ex simplify "live run" direct from testing lib with prescribed output name 
#simplify_job = ndLibrarySupport.simplify(ndman.library, dest_lib)
#simplify_job.show_work_log()
simplify_job.run()

## load test the auto-resolved master collection
#import sys;sys.path.append(r"h:\code");import ndLibrarySupport;ndman=ndLibrarySupport.manager(r"D:\Libraries\SimplifiedDistributions\DataIndex_Rat_Brain_v2021-03-02")
## load test prescribed name collection
"""
import sys;sys.path.append(r"h:\code");import ndLibrarySupport;ndman=ndLibrarySupport.manager(dest_lib)
"""

# code syntax check line for copy paste fun while in development
# (due to inexperience) no-re-set and re-run while in same session
# must start fresh... i believe that is due to import, but I dont know things.
# exec(open(os.path.join(ndLibrarySupport.codePath,"simplify.py")).read())

