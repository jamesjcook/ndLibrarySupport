
# this code assumes you've already loaded the main code.
#codePath
# load the transfer function
if (sys.version_info > (3, 0)):
  exec(open(ndLibrarySupport.codePath+"/Testing/Move_Atlas_Script.py").read())
else:
  execfile(ndLibrarySupport.codePath+"/Testing/Move_Atlas_Script.py")

#rootDir=r""
distRoot=r"D:\Libraries\SimplifiedDistributions\RatAtlas2020"
avg = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\23Rat")
single = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\21Rat")
#moveFiles(avg, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\RatAvg2019\v2020-07-30")
#moveFiles(single, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\151124_3_1\v2020-07-30")

#D:\Libraries\SimplifiedDistributions\RatAtlas2020
moveFiles(avg, distRoot + r"\RatAvg2019_v2020-10-13")
moveFiles(single,distRoot +  r"\151124_3_1_v2020-10-13")
