## Script to move Atlas files to another location
## To run in Slicer, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\Move_Atlas_Script.py")
## Author: Austin Kao

execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\ndLibrary.py")
import shutil
import re
import os

## Assumes Strain and LibName fields exist for lib.conf file for a lib
def moveFiles(lib, new_location):
    # os.mkdir(os.path.join(new_location, "labels")) //Uncomment this line if you need to make labels directory
    volSet = lib.getEntireVolumeSet()
    labelVolume = lib.labelVolume
    ref_lib = lib
    strain = lib.fields["Strain"]
    libname = lib.fields["LibName"]
    shutil.copy(os.path.join(lib.file_loc, "lib.conf"), os.path.join(new_location, "lib.conf"))
    if labelVolume is not None:
        if isinstance(labelVolume, ndLibrary):
            ref_lib = labelVolume
        labelVolumeFile = ref_lib.labelVolume[0]
        labelVolumeName = labelVolumeFile.split("\\")[-1]
        labelVolumeName = labelVolumeName.split(".")[0]
        labelTransform = ref_lib.trackTransform[0]
        labelTransformName = labelTransform.split("\\")[-1]
        #print(labelVolumeFile)
        #print(labelVolumeName)
        if ref_lib.fields.has_key("FileAbrevPattern"):
            match = re.search(ref_lib.fields["FileAbrevPattern"], labelVolumeName)
            if match and len(match.groups())>1:
                labelVolumeName = match.group(2)
            elif match:
                labelVolumeName = match.group(0)
        newLabelVolume = os.path.join(new_location, "labels", strain+"_"+libname+"_"+labelVolumeName+".nii.gz")
        newLabelTransform = os.path.join(new_location, "labels", labelTransformName)
        #print(newLabelVolume)
        shutil.copy(os.path.join(ref_lib.file_loc, "lib.conf"), os.path.join(new_location, "labels", "lib.conf"))
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
        if ref_lib.fields.has_key("FileAbrevPattern"):
            match = re.search(ref_lib.fields["FileAbrevPattern"], colorTableName)
            if match and len(match.groups())>1:
                colorTableName = match.group(2)
            elif match:
                colorTableName = match.group(0)
        newColorTable = os.path.join(new_location, "labels", strain+"_"+libname+"_"+colorTableName+"_lookup.txt")
        #print(newColorTable)
        shutil.copy(colorTableFile, newColorTable)
    trackTransform = lib.trackTransform[0]
    #print(trackTransform)
    #print(os.path.join(new_location, strain+"_"+libname+"_"+trackTransform.split("\\")[-1]))
    shutil.copy(trackTransform, os.path.join(new_location, trackTransform.split("\\")[-1]))
    for volKey in volSet:
        #print(os.path.join(new_location, strain+"_"+libname+"_"+volKey+".nii.gz"))
        shutil.copy(volSet[volKey][0], os.path.join(new_location, strain+"_"+libname+"_"+volKey+".nii.gz"))

avg = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\23Rat")
single = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\21Rat")
moveFiles(avg, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\RatAvg2019\v2020-07-30")
moveFiles(single, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\151124_3_1\v2020-07-30")