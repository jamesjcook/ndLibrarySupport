
import sys
import os

dist_root = r"D:\Libraries\SimplifiedDistributions"
dest_lib = os.path.join(dist_root,r"MouseBrain_v2020-11-02")
# run with "dev" code.
sys.path.append(r"h:\code");
import ndLibrarySupport;
ndman=ndLibrarySupport.manager(dest_lib)
