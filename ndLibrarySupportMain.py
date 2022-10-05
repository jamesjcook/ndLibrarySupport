#dist_root = r"D:\Libraries\SimplifiedDistributions"
#lib_path = os.path.join(dist_root,r"RatBrain_v2021-03-02")

# need to mount piper for this to work, also lib.conf files can be lost!
# copy of those is in this directory masquerading as examples
#lib_path=r'\\piper\piperspace\18.gaj.42_packs_BXD89'
#lib_path=r'/Volumes/piperspace/18.gaj.42_packs_BXD89'
#lib_path=r'/Users/harry/Data/18.gaj.42_packs_BXD89'
# run with "dev" code.
#sys.path.append(r"/Users/harry/Documents/code");

#TransformedDataPackage

#D:\CIVM_Apps\Slicer\4.11.20200930\Slicer.exe --python-script H:\code\ndLibrarySupport\Testing\test_simplified_rat.py
import sys
import os
from manager import manager
import logging


def lib_start(args,template_conf):
    from optparse import OptionParser
    from shutil import copyfile
    parser = OptionParser()
    # parser.add_option("-f", "--file", dest="filename",
                      # help="write report to FILE", metavar="FILE")
    # parser.add_option("-q", "--quiet",
                      # action="store_false", dest="verbose", default=True,
                      # help="don't print status messages to stdout")
    parser.add_option("-g", "--group", action="store", type="string", dest='group',default='')
    parser.add_option("-l", "--library", "--lib_path", action="store", type="string", dest='lib_path',default='')
    parser.add_option("-t", "--template", action="store", type="string", dest='template',default='')
    parser.add_option("--data_package", action="store", type="string", dest='data_package',default='')

    try:
        (opts, args) = parser.parse_args(args)
    except getopt.GetoptError:
        logger.warning('lib_start.py -g <group> -t <template file>')
        #print 'see https://itk.org/SimpleITKDoxygen/html/namespaceitk_1_1simple.html#ae40bd64640f4014fba1a8a872ab4df98 for the bitdepth info'
        sys.exit(2)
    # if opts.help
        # print 'FILE.py -b <base_image> -e <edge_image> -o <laoprasert_out> [ -w <weighting_factor>]'
        # sys.exit()
    #lib_path=r"L:\ProjectSpace\bxd_RCCF_review"
    # TODO: no hardcoding, definitley not pointing to vidconfmac
    #opts.lib_path=r"/Volumes/vidconfmacspace/18.gaj.42_packs_BXD77"
    #lib_path = os.path.join(lib_path, opts.group)
    if opts.template is not None:
        if os.path.isfile(opts.template):
            template_conf=opts.template
        else:
            logger.warning("Not using template opt because <{}> not file".format(opts.template))

    if not os.path.isfile(os.path.join(opts.lib_path, r'lib.conf')):
        if os.path.isfile(os.path.join(template_conf)):
            copyfile(template_conf, os.path.join(opts.lib_path, r'lib.conf'))
        else:
            logger.warning("Error: no template"+template_conf)
            return None
    ndman=manager(opts.lib_path,categoryFilter='TransformedDataPackage', prompt=opts.data_package == '')
    if opts.data_package != '':
        data_package = ndman.set_data_package(opts.data_package)
        if data_package is None:
            logger.warning("Error finding {} in libraries".format(opts.data_package))
    return ndman




ndman=None
if __name__ == "__main__":
    code_directory = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(code_directory))
    import ndLibrarySupport
    import logging
    logger=logging.getLogger("ndLibrary")
    logger.warning(code_directory)
    #from conf import conf
    # might be able to ask ndLibrarySupport for its code folder
    # Maybe the packed conf could be a hard coded data element of ndlibrary support?
    #logger.warning("Lib support code_dir <{}>".format(ndLibrarySupport.code_directory))
    template_conf = os.path.join(code_directory,"example","samba_packed_study","lib.conf")
    ndman=lib_start(sys.argv[1:],template_conf)
