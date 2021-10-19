## generate new config files using the conf.py save function
## save them in the correct location

import os
import re
import pathlib

from ndLibrarySupport import conf
from ndLibrarySupport import ndLibrary

def print_dict(d):
    for x in d:
        print(x,d[x])
    print('\n')


# path to the directory where we save the config files
# data_conf is the config file for data 
# likewise for labels_conf
def generate_config_one_experiment(path, data_conf, labels_conf):
    # if a config file already exists, delete it
    if(os.path.isfile(os.path.join(path,'lib.conf'))):
        os.remove(os.path.join(path,'lib.conf'))
    if(os.path.isfile(os.path.join(path,'labels/lib.conf'))):
        os.remove(os.path.join(path,'labels/lib.conf'))

    try:
        update_origin_transform(path, data_conf, labels_conf)
    except:
        pass
    
    
    data_conf.save(path)
    labels_conf.save(os.path.join(path,'labels'))


# data_conf and labels_conf are conf object that we want to manipulate
# both will store the same transform path
# but in labels_conf we need to prefix with ../../ because paths are RELATIVE 
# path is to the experiment folder (ie N58600)
def update_origin_transform(path, data_conf, labels_conf):
    final_path = ''

    # extract the current folder name 
    experiment_name = os.path.basename(os.path.normpath(path))

    rigid_transform_regex = re.compile('_\d_' + experiment_name + '_to_.*_rigid\.mat')

    # TODO: in MDT_BxD89 (the average folder) the transform name removes the MDT_ prefix
    # this works to isolate BxD89, however BxD89_to_symmetric45um does not have a RIGID transform file (only affine and warp)
    if(re.match('MDT_(.*)', experiment_name)):
        m = re.search('MDT_(.*)', experiment_name)
        experiment_name = m.group(1)
        # does not find the affine transform. why?
        rigid_transform_regex = re.compile('_\d_' + experiment_name + '_to_.*_affine\.mat')
    print('experiment = ' + experiment_name)
    transform_folder_regex = re.compile(experiment_name + '_to_.*')

    transform_path = os.path.join(path, 'transforms')
    for i in os.listdir(transform_path):
        if(transform_folder_regex.match(i)):
            print(i)
            transform_path = os.path.join(transform_path,i)
            for j in os.listdir(transform_path):
                if(rigid_transform_regex.match(j)):
                    final_path = os.path.join('transforms/',i,j)
                    break 
            break 
    print('TRANSFORM PATH = ' + final_path)
    data_conf['OriginTransform'] = final_path
    labels_conf['OriginTransform'] = os.path.join('../../',final_path)


# a recursive definition of the previous function
# generalize to hunt for the correct transform.mat file even if it is hidden deep within nested folders or a weird location
def update_origin_transform_recursive():
    pass


# paths to our 'template' conf files that we will copy into the appropriate locations
#data_conf_template_path = r'/Users/harry/Documents/code/ndLibrarySupport/example/samba_packed_study/Specimen1/lib.conf'
#labels_conf_template_path = r'/Users/harry/Documents/code/ndLibrarySupport/example/samba_packed_study/Specimen1/labels/lib.conf'
data_conf_template_path = r'L:\ProjectSpace\bxd_RCCF_review\code\ndLibrarySupport\example\samba_packed_study\Specimen1\lib.conf'
labels_conf_template_path = r'L:\ProjectSpace\bxd_RCCF_review\code\ndLibrarySupport\example\samba_packed_study\Specimen1\labels\lib.conf'


# loads the template config files as a conf object (an extended dict)
#data_conf,labels_conf = load_template(data_conf_template_path, labels_conf_template_path)
#labels_conf.print()



# the base directory where all data from different trials are stored
#path = r'/Users/harry/Data/18.gaj.42_packs_BXD89'
#print(path)
#print(os.listdir(path))

# loop through all experiments in the 18.gaj.42_packs_BXD89
#directory = r'/Users/harry/Data/18.gaj.42_packs_BXD89'

#experiments = os.listdir(directory)

#use data_package instead of experiment
# following line removes everything from the experiments list that is not a folder
# and completes the full path by reintroducing the prefix
#experiments = [ os.path.join(directory,x) for x in experiments if os.path.isdir(os.path.join(directory,x)) ]

# for each experiment, pass that directory along for the function to build the config files
#for path in experiments:
#    generate_config_one_experiment(path, data_conf, labels_conf)


#directory = r'L:\ProjectSpace\bxd_RCCF_review\archive_dump\connectomeN58665dsi_studioRCCF'
#generate_config_one_experiment(directory, data_conf, labels_conf)


library_path = r'L:\ProjectSpace\bxd_RCCF_review';
archive_dump = r'L:\ProjectSpace\bxd_RCCF_review\archive_dump';
script = r'L:\workstation\code\shared\pipeline_utilities\prototype\prototype_generate_diffusion_nhdr.pl';
groups = ['BXD101','BXD24','BXD29','BXD34','BXD43','BXD44','BXD45','BXD48a','BXD51','BXD60','BXD62','BXD65b','BXD77','BXD89']

#path = r"L:\ProjectSpace\bxd_RCCF_review\BXD60\190625-7_1"
#ndLibrary(None, path, data_conf_template_path)
template = data_conf_template_path
for g in groups:
    group_path = os.path.join(library_path, g)
    for p in os.listdir(group_path):
        # to check which is newer-currently saved lib.conf or the template
        # only update if the template is newer
        # must delete old file to update it
#        conf_path = os.path.join(group_path,p,'lib.conf')
#        if os.path.isfile(conf_path) and pathlib.Path(conf_path).stat().st_mtime < pathlib.Path(template).stat().st_mtime:
#            os.remove(conf_path)
#        path = os.path.join(group_path, p)
        print("\n   recoloring: " + path)
        ndLibrary(None, path, template)
        # find labels in ndLibrary 
        # find anterior commisure 
        # find color images (gqi color file) -- or any other color file 
        # if we have both of these, then measure color channels 
        # if brightest channel is green, then we want to swap red and green channels
            # maybe find smaerter way to demermine color 
        # check for longest dimension in picture
            # usually 2x1x1 
            # longst should be green 
            # whatever you swap it with "must" be red
        
        