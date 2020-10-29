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
        if not os.path.isdir(new_location):
            self.jobs.append(["mkdir "+os.path.basename(new_location),new_location])
        for child in self.lib.children:
            ident = self.name_resolve(child)
            self.jobs.append(["process "+ident,child,os.path.join(new_location,ident)])
            #child_location=
            #simplify(child,
        self.lib.conf[self.lib.filter_field]=".*"
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
    
    def run(self,test_mode=False):
        for job in self.jobs:
            print(job[0])
            if "mkdir" in job[0]:
                os.mkdir(job[1])
            elif "process" in job[0]:
                self.process_child_lib(job[1],job[2],test_mode)
            elif "save" in job[0]:
                self.save_conf(job[1],job[2])
            else:
                print("\tUNKNOWN job op")
    
    def save_conf(self,lib,dest):
        #conf=lib.conf.copy()
        conf=ndLibrarySupport.conf("blank")
        for e in lib.conf:
            conf[e]=lib.conf[e]
        conf.comments.clear()
        key = "Path"
        if key in conf:
            conf["#"+key]= conf[key]
            del conf[key]
        if key in conf:
            conf["#"+key]= conf[key]
            del conf[key]
        key = "CustomPython"
        if key in conf:
            conf["#"+key]= conf[key]
            del conf[key]
        conf.save(dest)
    
    ### un-converted code from the move files version
    def process_child_lib(self, lib, new_location, test_mode=False):
        if not os.path.isdir(new_location):
            os.mkdir(new_location)
        ## Assumes Strain and LibName fields exist for lib.conf file for a lib
        category_txt=""
        category = lib.conf["Category"]
        if category in lib.conf:
            category_text = lib.conf[category] + "_"
        else:
            category_text = category + "_"
        lib_name = lib.conf["LibName"]
        vol_set = lib.getEntireVolumeSet()
        ## copy_vol_set replaced by load/harden/save in line loop.
        #self.copy_vol_set(lib,vol_set,new_location,category_txt,lib_name)
        tform_logic = slicer.vtkSlicerTransformLogic()
        # do not compress output
        properties = {'useCompression': 0}
        for vol in vol_set:
            ## custom color table support
            ctblKey="ColorTable_"+vol
            if ctblKey in vol_set[vol].conf:
                ctbl=os.path.join(vol_set[vol].Path,vol_set[vol].conf[ctblKey])
                print("custom color table:"+vol_set[vol].conf[ctblKey]+" for "+vol)
                if ctblKey not in lib.conf:
                    lib.conf[ctblKey] = os.path.basename(ctbl)
                    ctbl_dest = shutil.copy(ctbl, os.path.join(new_location, lib.conf[ctblKey]))
            else:
                ctbl = None
            #if ctbl is not None:
            #    volNode.GetDisplayNode().SetAndObserveColorNodeID(ctbl.GetID())
            #vol_dest = os.path.join(new_location,category_text+lib_name+"_"+vol+".nhdr")
            vol_dest = os.path.join(new_location,lib_name+"_"+vol+".nhdr")
            if os.path.isfile(vol_dest):
                print("previously completed "+vol)
                continue
            print("load/find volume node "+vol)
            vol_node=lib.get_volume_node(vol)
            print("\tharden tform")
            tform_logic.hardenTransform(vol_node)
            print("\tsave "+vol_dest)
            slicer.util.saveNode(vol_node,vol_dest, properties)
            # in tesitng just do 1
            if test_mode:
                break;
        label_dir=os.path.join(new_location, "labels")
        self.copy_label_vol(lib,label_dir)
        self.copy_color_table(lib,label_dir)
        self.save_label_conf(lib,label_dir)
        ## tractography needs to be last, becuase it has to save the scene, and removes all the other nodes. 
        self.copy_tractography(lib,new_location)
        ##
        ## UPDATE filter, pattern, match fields
        ##
        lib.conf[lib.recursion_field] = "true"
        lib.conf[lib.filter_field] = lib_name+".*|labels"
        sep="|"
        lib.conf[lib.pattern_field] = "(.*?)("+sep.join(vol_set)+"|labels)(.*)"
        lib.conf[lib.match_field] = r"\2"
        self.save_conf(lib,new_location)
    
    def copy_label_vol(self,lib,new_location):
        if not os.path.isdir(new_location):
            os.mkdir(new_location)
        lib_name = lib.conf["LibName"]
        vol = "labels"
        vol_dest = os.path.join(new_location,lib_name+"_"+vol+".nhdr")
        if os.path.isfile(vol_dest):
            print("previously completed "+vol)
            return
        vol_node = lib.getLabelVolume()
        label_vol = lib.labelVolume
        tform_logic = slicer.vtkSlicerTransformLogic()
        # label compression is delicious
        properties = {'useCompression': 1}
        if label_vol is not None :
            if isinstance(label_vol, ndLibrary):
                lib = label_vol
            print("load/find volume node "+vol)
            #vol_node=lib.loadLabels(vol)
            print("\tharden tform")
            tform_logic.hardenTransform(vol_node)
            print("\tsave "+vol_dest)
            slicer.util.saveNode(vol_node,vol_dest, properties)
    
    def copy_tractography(self,lib,new_location):
        # look for tractography, and load(or return)
        if not lib.load_tractography():
            return
        else:
            if "TractographyDisplay" not in slicer.moduleNames.TractographyDisplay:
                slicer.util.warningDisplay("CANNOT simplify tractography missing required extensions","ERROR ndLibraraySupport Simplify")
                return
            # set our output dir/scene path
            tract_dir=os.path.join(new_location, "tractography")
            if not os.path.isdir(tract_dir):
                os.mkdir(tract_dir)
            tform_logic = slicer.vtkSlicerTransformLogic()
            lib_name = lib.conf["LibName"]
            properties = {}
            # Get the tracks from scene
            tracks=slicer.util.getNodesByClass("vtkMRMLFiberBundleNode")
            for node in tracks:
                trk=node.GetName()
                #dest = os.path.join(tract_dir,lib_name+"_"+trk+".vtk")
                dest = os.path.join(tract_dir,trk+".vtk")
                if os.path.isfile(dest):
                    print("previously completed "+trk)
                    continue
                print("\tharden tform")
                tform_logic.hardenTransform(node)
                print("\tsave "+dest)
                slicer.util.saveNode(node,dest, properties)
            # set blankish view 
            #node_list=slicer.mrmlScene.GetNodes()
            #node_list.GetNumberOfItems()
            # foreach node, 
            # if not trk remove 
            node_classes=('vtkMRMLVolumeNode',
                          'vtkMRMLLinearTransformNode',
                          #'vtkMRMLColorTableNode',
                          'vtkMRMLViewNode',
                          'vtkMRMLSliceNode',
                          'vtkMRMLCameraNode',
                          'vtkMRMLLayoutNode')
            for node_class in node_classes:
                self.remove_nodes_by_class(node_class)
                pass
            slicer.util.saveScene(tract_dir+".mrml")
            # conf updates
            lib.conf[lib.recursion_field] = "false"
            lib.conf[lib.filter_field] = ".*[.]vtk"
            sep="|"
            lib.conf[lib.pattern_field] = "(.*)"
            lib.conf[lib.match_field] = r"\1"
            if "CustomPython" in lib.conf:
                del lib.conf["CustomPython"]
            # conf save
            self.save_conf(lib,tract_dir)
            # remove all tracks?
            for node in tracks:
                slicer.mrmlScene.RemoveNode(node)
                pass
    
    def copy_color_table(self,lib,new_location):
        lib_name = lib.conf["LibName"]
        fname = "labels_lookup"
        ctbl_dest = os.path.join(new_location,lib_name+"_"+fname+".txt")
        if os.path.isfile(ctbl_dest):
            return
        colorTable = lib.colorTable
        if colorTable is not None:
            if isinstance(colorTable, ndLibrary):
                lib = colorTable
            colorTableFile = lib.colorTable[0]
            shutil.copy(colorTableFile, ctbl_dest)
    
    def save_label_conf(self,lib,new_location):
        lib_name = lib.conf["LibName"]
        while isinstance(lib.labelVolume, ndLibrary):
            lib = lib.labelVolume
            
        lib.conf[lib.filter_field] = lib_name+".*|labels"
        sep="|"
        lib.conf[lib.pattern_field] = "(.*?)(labels)(.*)"
        lib.conf[lib.match_field] = r"\2"
        self.save_conf(lib,new_location)
    
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
    
    def remove_nodes_by_class(self,node_class):
        # foreach node, 
        # if not trk remove 
        node_list=slicer.util.getNodesByClass(node_class)
        for node in node_list:
            slicer.mrmlScene.RemoveNode(node)

#avg = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\23Rat")
#single = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\21Rat")
#moveFiles(avg, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\RatAvg2019\v2020-07-30")
#moveFiles(single, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\151124_3_1\v2020-07-30")
#D:\Libraries\SimplifiedDistributions\RatAtlas2020
