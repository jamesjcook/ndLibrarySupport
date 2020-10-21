## Script to simplify distribution packages reducing required features
## see Testing/Simplify *
## relatively clear this doesnt belong as a class, but rather a function of ndLibrary.
## Now that production features of that are in functional state, dont want to open it 
## up and destroy it.
## Prototying "moveFiles": Austin Kao
## Production adaptation: James Cook

import shutil
import re
import os

class simplify:
    def __init__(self, lib, new_location, auto_output=False):
        self.jobs = list()
        if not isinstance(lib,ndLibrary):
            print("Setup master lib")
            self.lib = ndLibrary(None, lib)
        else:
            self.lib = lib
        if auto_output:
            out_lib = self.name_resolve()
            new_location = os.path.join(new_location,out_lib)
        for child in self.lib.children:
            ident = self.name_resolve(child)
            self.jobs.append(["process "+ident,child,os.path.join(new_location,ident)])
            #child_location=
            #simplify(child,
        self.jobs.append(["save "+self.lib.conf.conf_path+" -> "+new_location,self.lib, new_location])
        #self.lib.conf.save(new_location)
        return
    def name_resolve(self,lib=None):
        if lib is None:
            lib = self.lib
        # look at category, childcategory, libname, path variables.
        # n would be our "given name"
        n = os.path.basename(lib.conf_dir)
        vth = ""
        # if we have a redirecting path at this level, that is probably a version
        if "Path" in lib.conf:
            vth = "_"+os.path.basename(lib.conf["Path"])
        # if our lib has a libname, it is probably our preffered nickname.
        if "LibName" in lib.conf:
            n = lib.conf["LibName"]
        #if in lib.conf:
        #if in lib.conf:
        if lib.parent is not None:
            category = lib.parent.conf["ChildCategory"]
        else:
            category = lib.conf["Category"]
        return category+"_"+n+vth
    
    def show_work_log(self):
        for job in self.jobs:
            print(job[0])
    
    def run_jobs(self):
        for job in self.jobs:
            print(job[0])
            if "process" in job[0]:
                #self.process_child_lib(job[1],job[2])
            elif "save" in job[0]:
                self.save_conf(job[1],job[2])
            else:
                print("\tUNKNOWN job op")
    
    def save_conf(self,lib,dest):
        conf=lib.conf
        if "Path" in conf:
            del conf["Path"]
        conf.save(dest)
    
    ### un-converted code from the move files version
    def process_child_lib(self, lib, new_location):
        if not os.path.isdir(new_location):
            os.mkdir(new_location)
        ## Assumes Strain and LibName fields exist for lib.conf file for a lib
        category_txt=""
        if "Strain" in lib.conf:
          category = lib.conf["Strain"]
          category_txt=category+"_"
        lib_name = lib.conf["LibName"]
        vol_set = lib.getEntireVolumeSet()
        ## copy_vol_set replaced by load/harden/save in line loop.
        #self.copy_vol_set(lib,vol_set,new_location,category_txt,lib_name)
        tform_logic = slicer.vtkSlicerTransformLogic()
        # do not compress output
        properties = {'useCompression': 0}
        for vol in vol_set:
            ## Load volume
            print("get volume node "+vol)
            #vol_node=lib.get_volume_node(vol)
            print("\tharden tform")
            #tform_logic.hardenTransform(vol_node)
            vol_dest = os.path.join(new_location,lib_name+"_"+vol+".nhdr"
            print("\tsave "+vol_dest)
            #slicer.util.saveNode(vol_node,vol_dest, properties)
        ref_lib = lib
        label_vol = lib.labelVolume
        label_dir=os.path.join(new_location, "labels")
        if not os.path.isdir(label_dir):
            os.mkdir(label_dir)
        #self.copy_label_vol(ref_lib,label_vol)
        #self.copy_color_table(lib)
        #shutil.copy(os.path.join(lib.file_loc, "lib.conf"), os.path.join(new_location, "lib.conf"))
        lib.conf[lib.recursion_field] = "true"
        self.save_conf(lib,new_location)
        
    def copy_label_vol(self,ref_lib,label_vol):
        if label_vol is not None:
            if isinstance(label_vol, ndLibrary):
                ref_lib = label_vol
            label_volFile = ref_lib.label_vol[0]
            label_volName = label_volFile.split("\\")[-1]
            label_volName = label_volName.split(".")[0]
            labelTransform = ref_lib.originTransform[0]
            labelTransformName = labelTransform.split("\\")[-1]
            #print(label_volFile)
            #print(label_volName)
            #if ref_lib.conf.has_key("FileAbrevPattern"):
            if "FileAbrevPattern" in ref_lib.conf:
                match = re.search(ref_lib.conf["FileAbrevPattern"], label_volName)
                if match and len(match.groups())>1:
                    label_volName = match.group(2)
                elif match:
                    label_volName = match.group(0)
            if not os.path.isdir(label_dir):
                os.mkdir(label_dir)
            newlabel_vol = os.path.join(label_dir, category_txt+lib_name+"_"+label_volName+".nii.gz")
            newLabelTransform = os.path.join(label_dir, labelTransformName)
            #print(newlabel_vol)
            shutil.copy(os.path.join(ref_lib.file_loc, "lib.conf"), os.path.join(label_dir, "lib.conf"))
            shutil.copy(label_volFile, newlabel_vol)
            shutil.copy(labelTransform, newLabelTransform)
    def copy_color_table(self,lib):
        colorTable = lib.colorTable
        if colorTable is not None:
            if isinstance(colorTable, ndLibrary):
                ref_lib = colorTable
            colorTableFile = ref_lib.colorTable[0]
            colorTableName = colorTableFile.split("\\")[-1]
            colorTableName = colorTableName.split(".")[0]
            #print(colorTableFile)
            #print(colorTableName)
            #if ref_lib.conf.has_key("FileAbrevPattern"):
            if "FileAbrevPattern" in ref_lib.conf:
                match = re.search(ref_lib.conf["FileAbrevPattern"], colorTableName)
                if match and len(match.groups())>1:
                    colorTableName = match.group(2)
                elif match:
                    colorTableName = match.group(0)
            newColorTable = os.path.join(label_dir, category_txt+lib_name+"_"+colorTableName+"_lookup.txt")
            #print(newColorTable)
            shutil.copy(colorTableFile, newColorTable)
        #if "originTransform" in lib:
    def copy_origin_transform(lib):
        try:
            originTransform = lib.originTransform[0]
            #print(originTransform)
            #print(os.path.join(new_location, category_txt+lib_name+"_"+originTransform.split("\\")[-1]))
            shutil.copy(originTransform, os.path.join(new_location, originTransform.split("\\")[-1]))
        except:
            print("No OriginTransform")
    def copy_vol_set(lib,vol_set,new_location,category_txt,lib_name):
        for volKey in vol_set:
            #print(os.path.join(new_location, category_txt+lib_name+"_"+volKey+".nii.gz"))
            shutil.copy(vol_set[volKey][0], os.path.join(new_location, category_txt+lib_name+"_"+volKey+".nii.gz"))

#avg = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\23Rat")
#single = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\21Rat")
#moveFiles(avg, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\RatAvg2019\v2020-07-30")
#moveFiles(single, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\151124_3_1\v2020-07-30")
#D:\Libraries\SimplifiedDistributions\RatAtlas2020
