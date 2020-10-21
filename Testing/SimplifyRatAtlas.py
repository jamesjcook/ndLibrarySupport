

import sys
import os
sys.path.append(r"h:\code")
import ndLibrarySupport

dev_root = r"D:\Libraries\010Rat_Brain"
dist_root = r"D:\Libraries\SimplifiedDistributions"
simplify_job = ndLibrarySupport.simplify(dev_root, dist_root, True)
simplify_job.show_work_log()

# no-re-set and re-run while working on the code, must start fresh... 
# i believe that is due to import
