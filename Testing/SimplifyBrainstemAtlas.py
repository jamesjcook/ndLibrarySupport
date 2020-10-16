
# this code assumes you've already loaded the main code.
#codePath
# load the transfer function
if (sys.version_info > (3, 0)):
  exec(open(ndLibrarySupport.codePath+"/Testing/Move_Atlas_Script.py").read())
else:
  execfile(ndLibrarySupport.codePath+"/Testing/Move_Atlas_Script.py")

rootDir = r"D:\Libraries\040Human_Brainstem"
distRoot=r"D:\Libraries\SimplifiedDistributions\HumanBrainstem2020"

brainstem = ndLibrary(None, rootDir)
moveFiles(brainstem,distRoot +  r"\130827-2-0_v2020-10-13")
