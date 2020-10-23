
import sys
import os

testing_dir = os.path.dirname(os.path.abspath(__file__))
dist_root = os.path.dirname(os.path.dirname(testing_dir))

sys.path.append(dist_root)
import ndLibrarySupport
ndman=ndLibrarySupport.manager(dist_root)
