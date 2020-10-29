
import sys
import os

# "rat lib" dev
dest_lib=r"D:\Libraries\010Rat_Brain"
dist_root = r"D:\Libraries\SimplifiedDistributions"
# "rat lib" dist
#dest_lib = os.path.join(dist_root,"RatBrain_v2020-10-16")
# "human brainstem" dev
dest_lib = os.path.join(dist_root,r"D:\Libraries\040Human_Brainstem")
# run with "dev" code.
sys.path.append(r"h:\code");
import ndLibrarySupport;
ndman=ndLibrarySupport.manager(dest_lib)
