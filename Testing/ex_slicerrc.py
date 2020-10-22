
# run "rat lib" in dev
#import sys;sys.path.append(r"h:\code");import ndLibrarySupport;ndman=ndLibrarySupport.manager(r"D:\Libraries\010Rat_Brain")

# "rat lib" distribution 
#dest_lib=r"D:\Libraries\SimplifiedDistributions\DataIndex_Rat_Brain_v2020-10-16"
dist_root = r"D:\Libraries\SimplifiedDistributions"
dest_lib = os.path.join(dist_root,"RatBrain_v2020-10-16")
# run with "dev" code.
import sys;sys.path.append(r"h:\code");import ndLibrarySupport;ndman=ndLibrarySupport.manager(dest_lib)

# run "brainstem lib"
#import sys;sys.path.append(r"h:\code");import ndLibrarySupport;ndman=ndLibrarySupport.manager(r"D:\Libraries\040Human_Brainstem")
