
import sys
import os

#dist_root = r"D:\Libraries\SimplifiedDistributions"
#lib_path = os.path.join(dist_root,r"RatBrain_v2021-03-02")

# need to mount piper for this to work, also lib.conf files can be lost!
# copy of those is in this directory masquerading as examples
#lib_path=r'\\piper\piperspace\18.gaj.42_packs_BXD89'
lib_path=r'/Volumes/piperspace/18.gaj.42_packs_BXD89'
# run with "dev" code.
sys.path.append(r"/Volumes/workstation_home/software/visualization/slicer");
import ndLibrarySupport;
#TransformedDataPackage
ndman=ndLibrarySupport.manager(lib_path,'TransformedDataPackage')
#D:\CIVM_Apps\Slicer\4.11.20200930\Slicer.exe --python-script H:\code\ndLibrarySupport\Testing\test_simplified_rat.py