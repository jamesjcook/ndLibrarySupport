## Script to simplify distribution packages reducing required features
## see Testing/Simplify *
## Prototying "moveFiles": Austin Kao
## Production adaptation: James Cook

import shutil
import re
import os


class simplify:
    def __init__(self, lib, new_location):
        if not isinstance(lib,ndLibraray):
            print("Setup master lib")
            self.lib = ndLibrary(lib)
            self.lib.loadEntire()
        else:
            self.lib = lib
            
        return
        ### un-converted code from the move files version
    def processSubLib(self, lib, new_location):
        ## Assumes Strain and LibName fields exist for lib.conf file for a lib
        volSet = lib.getEntireVolumeSet()
        labelVolume = lib.labelVolume
        ref_lib = lib
        category_txt=""
        if "Strain" in lib.fields:
          category = lib.fields["Strain"]
          category_txt=category+"_"
        libname = lib.fields["LibName"]
        if not os.path.isdir(new_location):
            os.mkdir(new_location)
        shutil.copy(os.path.join(lib.file_loc, "lib.conf"), os.path.join(new_location, "lib.conf"))
        labelDir=os.path.join(new_location, "labels")
        if labelVolume is not None:
            if isinstance(labelVolume, ndLibrary):
                ref_lib = labelVolume
            labelVolumeFile = ref_lib.labelVolume[0]
            labelVolumeName = labelVolumeFile.split("\\")[-1]
            labelVolumeName = labelVolumeName.split(".")[0]
            labelTransform = ref_lib.originTransform[0]
            labelTransformName = labelTransform.split("\\")[-1]
            #print(labelVolumeFile)
            #print(labelVolumeName)
            #if ref_lib.fields.has_key("FileAbrevPattern"):
            if "FileAbrevPattern" in ref_lib.fields:
                match = re.search(ref_lib.fields["FileAbrevPattern"], labelVolumeName)
                if match and len(match.groups())>1:
                    labelVolumeName = match.group(2)
                elif match:
                    labelVolumeName = match.group(0)
            if not os.path.isdir(labelDir):
                os.mkdir(labelDir)
            newLabelVolume = os.path.join(labelDir, category_txt+libname+"_"+labelVolumeName+".nii.gz")
            newLabelTransform = os.path.join(labelDir, labelTransformName)
            #print(newLabelVolume)
            shutil.copy(os.path.join(ref_lib.file_loc, "lib.conf"), os.path.join(labelDir, "lib.conf"))
            shutil.copy(labelVolumeFile, newLabelVolume)
            shutil.copy(labelTransform, newLabelTransform)
        colorTable = lib.colorTable
        if colorTable is not None:
            if isinstance(colorTable, ndLibrary):
                ref_lib = colorTable
            colorTableFile = ref_lib.colorTable[0]
            colorTableName = colorTableFile.split("\\")[-1]
            colorTableName = colorTableName.split(".")[0]
            #print(colorTableFile)
            #print(colorTableName)
            #if ref_lib.fields.has_key("FileAbrevPattern"):
            if "FileAbrevPattern" in ref_lib.fields:
                match = re.search(ref_lib.fields["FileAbrevPattern"], colorTableName)
                if match and len(match.groups())>1:
                    colorTableName = match.group(2)
                elif match:
                    colorTableName = match.group(0)
            newColorTable = os.path.join(labelDir, category_txt+libname+"_"+colorTableName+"_lookup.txt")
            #print(newColorTable)
            shutil.copy(colorTableFile, newColorTable)
        #if "originTransform" in lib:
        try:
            originTransform = lib.originTransform[0]
            #print(originTransform)
            #print(os.path.join(new_location, category_txt+libname+"_"+originTransform.split("\\")[-1]))
            shutil.copy(originTransform, os.path.join(new_location, originTransform.split("\\")[-1]))
        except:
            print("No OriginTransform")
        for volKey in volSet:
            #print(os.path.join(new_location, category_txt+libname+"_"+volKey+".nii.gz"))
            shutil.copy(volSet[volKey][0], os.path.join(new_location, category_txt+libname+"_"+volKey+".nii.gz"))

#avg = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\23Rat")
#single = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\21Rat")
#moveFiles(avg, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\RatAvg2019\v2020-07-30")
#moveFiles(single, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\151124_3_1\v2020-07-30")
#D:\Libraries\SimplifiedDistributions\RatAtlas2020
