
import sys
import os

dist_root = r"D:\Libraries\SimplifiedDistributions"
dest_lib = os.path.join(dist_root,r"HumanBrainstem_v2020-10-26")
# run with "dev" code.
sys.path.append(r"h:\code");
import ndLibrarySupport;
ndman=ndLibrarySupport.manager(dest_lib)
