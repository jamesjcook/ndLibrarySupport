
# this code assumes you've already loaded the main code.
# py2
#    execfile(codePath+"/Testing/SimplifyBrainstemAtlas.py")
#@ py3
#    exec(open(codePath+"/Testing/SimplifyBrainstemAtlas.py").read())
#codePath
# load the transfer function
if not '2.7' in sys.version:
  exec(open(ndLibrarySupport.codePath+"/Testing/Move_Atlas_Script.py").read())
else:
  execfile(ndLibrarySupport.codePath+"/Testing/Move_Atlas_Script.py")

rootDir = r"D:\Libraries\040Human_Brainstem"
distRoot=r"D:\Libraries\SimplifiedDistributions\HumanBrainstem2020"

brainstem = ndLibrary(None, rootDir)
moveFiles(brainstem,distRoot +  r"\130827-2-0_v2020-10-13")
