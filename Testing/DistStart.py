
import sys
import os

TestPath = os.path.dirname(os.path.abspath(__file__))
dist_root = os.path.dirname(os.path.dirname(os.path.dirname(TestPath)))

sys.path.append(dist_root)
import ndLibrarySupport
ndman=ndLibrarySupport.manager(dist_root)
