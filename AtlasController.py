## An object that instantiates different GUI elements and manages the ndLibrary data for each of them
## Author: Austin Kao

## Could easily be merged with DataPackageMenu... may be better to do so?
## DataPackageMenu is meant to represent the menu itself, and not the underlying processes that set up the atlas
## AtlasController is meant to represent an object that handles the ndLibrary data GUI elements are using

import slicer
import os

from VolumeDropdown import VolumeDropdown
from ExternalLoadButton import ExternalLoadButton
from InteractiveLabelSelector import InteractiveLabelSelector
from AngleSlider import AngleSlider

class AtlasController(): ## Rename?
    def tractography_prompt(self):
        slicer.util.warningDisplay(
        # 68 chars first line which seems reasonable for message box.
            "Tractography data may be available, however it cannot be used until\n"
            +"the tractography extensions are installed.\n\n"
            +"Please open the ExtensionManger (from the view menu) and install\n"
            +"SlicerDMRI and UKFTractography (not available for all nightly builds)\n\n"
            +"If the extension manager should fail to display any content, try\n"
            +"https://www.slicer.org/wiki/Documentation/Nightly/SlicerApplication/ExtensionsManager#Installing_an_extension_without_network_connection",
            "Tractography Available and inactive" )
    ## Function that sets up the ndLibrary selected from the DataPackageMenu
    def setUpLibrary(self, list_of_libraries):
        # TODO: check that list_of_libraries is a list of libs
        if isinstance(list_of_libraries, list):
            self.library = list_of_libraries[0]
        else:
            self.library = list_of_libraries
        ## Add additional view setups if appropriate
        tract_path = os.path.join(self.library.Path,"tractography.mrml")


        # somewhere in here is the problem
        if os.path.isfile(tract_path):
            if "TractographyDisplay" not in slicer.util.moduleNames():
                self.tractography_prompt()
            else:
                if "NavigatorWith3DAnd2DCompare" not in custom_layouts:
                    loadNavigatorWithLoad2DAnd3D()
                    loadNavigatorWith3DAnd2DCompare()
                    loadNavigatorAndTallAxial()
                    setNavigatorWith3DAnd2DCompare()
                    setNavigatorAndTallAxial()
                    showSlicesInNavigator()
                    setNavigatorAnd2DCompare()
                v=self.modulepanel.visible
                slicer.util.moduleSelector().selectModule("TractographyDisplay")
                slicer.util.moduleSelector().selectModule("Models")
                self.modulepanel.setVisible(v)
                
        ## set viewer orientation
        custom_orient=dict()
        orient_keys=["CompareOrientation","NavigatorOrientation"]
        for orient_key in orient_keys:
            if orient_key in self.library.conf:
                ok=orient_key.replace("Orientation","")
                custom_orient[ok]=self.library.conf[orient_key]
        
        for view in self.view_names:
            orient_key = "{}Orientation".format(view)
            if orient_key in self.library.conf:
                ok=orient_key.replace("Orientation","")
                custom_orient[ok]=self.library.conf[orient_key]
        sliceNodes = slicer.util.getNodesByClass("vtkMRMLSliceNode")
        for node in sliceNodes:
            for opt in custom_orient:
                if opt in node.GetSingletonTag():
                    node.SetOrientation(custom_orient[opt])
            node.GetSingletonTag()
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        self.clear_views()
        ## "Clear" the scene
        """for node in compNodes:
            node.SetBackgroundVolumeID("None")
            node.SetForegroundVolumeID("None")
            node.SetLabelVolumeID("None")"""





        ## Update each GUI element accordingly
        # TODO: this is where ndlibraries for each slice view are set
        # drop 123 are bad names
        # this function should take in a list of drop menus to populate
        # this one is told to do things, does not make decisinos
        for dropdown in self.list_of_VolumeDropdowns:
            dropdown.setupLibrary(self.library)
        """self.drop1.setupLibrary(self.library)
        self.drop2.setupLibrary(self.library)
        self.drop3.setupLibrary(self.library)
        self.dropNav.setupLibrary(self.library)
        self.labelSelector.setupLibrary(self.library)"""
        
        if "AnnotationMode" not in self.library.conf:
            return
        ## ADD ON FROM HARRISON
        ## load up the desired F.mrk.json file to show and save fiducials
        # TODO: grab chickever library relates to the specimen, not atlas
        from shutil import copyfile
        print(self.library)
        #F_template = r"L:\ProjectSpace\bxd_RCCF_review\archive_dump\fiducial_template.mrk.json"
        F_template = r"C:\Users\hmm56\Documents\F.fcsv"
        tmp = self.library.conf["LibName"] + r".fcsv" 
        #tmp = library.conf["LibName"] +r".mrk.json"
        F_this_lib = os.path.join(self.library.file_loc, tmp)

        
        # if the scene has already loaded any fiducial lists, then remove them from the scene 
        # this deletes them. be sure they are saved beforehand
        markup_nodes = slicer.mrmlScene.GetNodesByClass('vtkMRMLMarkupsNode')
        for node in markup_nodes:
            slicer.mrmlScene.RemoveNode(node)
        
        # if file does not exist, then copy the template to appropriate place
        if not os.path.isfile(F_this_lib):
            copyfile(F_template, F_this_lib)
        self.library.fiducial_list[0] = F_this_lib
        
        # check if scene has already loaded a fiducial list before loading another
        #if not library.fiducial_list[1]:
        #    library.fiducial_list[1] = slicer.util.loadMarkupsFiducialList(F_this_lib, returnNode=True)
        #else:
        #    slicer.util.loadMarkupsFiducialList(library.fiducial_list[0])
        self.library.fiducial_list[1] = slicer.util.loadMarkupsFiducialList(F_this_lib, returnNode=True)
        self.library.fiducial_list[1].SetMarkupLabelFormat("%d")
        originTransform = self.library.getOriginTransform()
        if originTransform is not None:
            self.library.fiducial_list[1].SetAndObserveTransformNodeID(originTransform.GetID())
        
        ## SAVING is currently handled in InteractiveLabelSelector.processSliceViewClick
        
        ## 

    ## Currently only instantiated in DataPackageMenu
    # now also instantiates a 2nd instance in manager.py to control the atlas view (for comparison)
    def __init__(self, view_names=None):
        self.setup_lib_counter = 0
        ## Set up the layout and slice view nodes
        """loadNavigatorAnd2DCompare()
        loadNavigatorWithLoadAnd2DCompare()
        loadNavigatorAndTallAxial()
        setNavigatorWithLoadAnd2DCompare()
        setNavigatorAnd2DCompare()
        setNavigatorAndTallAxial()
        setLabelOutlineAtlas(1)
        setSliceNodeLinks(1)"""
        self.library = None
        self.view_names = view_names
        ## Set up GUI elements
        # TODO: currently, each slice view has its own volumeDropdown
            # each volumeDropdown can have its own ndLibrary (the None argument here)
            # when we instantiate the volumeDropdowns, we just need to attach the appropriate ndLibrary (specimen on left, atlas on right)
        # extend atlascontroller to contain a list of drop downs
        # self.drop_menus is a list of these
        # get passed a list of dtrings for who to setup, based upon the VolumeDropdown id name (like Compare1 or Axial)
            # names are set by viewNavigatorWith...
            # view_names are the list to update thism with
            # a list of who this controller is going to control
        self.list_of_VolumeDropdowns = []
        for view in view_names:
            self.list_of_VolumeDropdowns.append(VolumeDropdown(None, view))

        """self.drop1 = VolumeDropdown(None, "Compare1")
        self.drop2 = VolumeDropdown(None, "Compare2")
        self.drop3 = VolumeDropdown(None, "Axial")
        self.dropNav = VolumeDropdown(None, "Navigator")"""
        
        # not sure what to do with these
        #self.externalLoad = ExternalLoadButton("Load")
        #self.labelSelector = InteractiveLabelSelector(None, "Navigator")
        #self.angleSlider = AngleSlider("Navigator", "Compare1", "Compare2")
    def clear_views(self):
        for view in self.list_of_VolumeDropdowns:
            view.clear_view()
        
        
