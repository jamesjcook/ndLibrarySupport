
import sys;import os;sys.path.append(r"h:\code");
import ndLibrarySupport;

exec(open(os.path.join(ndLibrarySupport.codePath,"conf.py")).read())
conf_i = conf(r"D:\Libraries\010Rat_Brain")
conf_i.print()

conf_b = conf(r"D:\Libraries\010Rat_Brain\v2020-10-16\21Rat","lib.conf",conf_i)
conf_b.print()
