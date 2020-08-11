## Class for a volume selection dropdown menu for the 2D Atlas
## Based on code from Dropdowns.py for FiberCompareView
## Author: Austin Kao

class volumeDropdown(qt.QComboBox):
    ## library is the ndLibrary used to store the locations of the volumes in the dropdown
    ## Make sure library contains the relative path to the volumes
    ## nodeTag is the string tag that identifies the slice view tag the dropdown is in
    def __init__(self, library, nodeTag):
        if not isinstance(nodeTag, str):
            print("Tag is not a string")
            return
        if slicer.app.layoutManager().sliceWidget(nodeTag) is None:
            print("Tag does not exist")
            return
        super(qt.QComboBox, self).__init__()
        self.nodeTag = nodeTag
        qtLayout = slicer.app.layoutManager().sliceWidget(nodeTag).layout()
        qtLayout.addWidget(self)
        self.libDict = dict()
        self.activated.connect(self.changeVolume)
        if library is not None:
            self.setupLibrary(library)
    
    ## Function that will change the volume image being looked at
    ## Because of how the dropdown menu is set up, any entry in volDict should at least have a file path
    ## The corresponding volume may or may not be loaded
    ## If loaded, function will set the loaded volume into the associated slice node
    ## Function will load the requested volume and add it to volDict
    def changeVolume(self, index):
        name = self.itemText(index)
        #print(name)
        #print(self.libDict[name])
        compString = "vtkMRMLSliceCompositeNode"+str(self.nodeTag)
        sliceString = "vtkMRMLSliceNode"+str(self.nodeTag)
        compNode = slicer.app.mrmlScene().GetNodeByID(compString)
        volNode = self.libDict[name].get_volume_node(name)
        if volNode is not None:
            compNode.SetBackgroundVolumeID(volNode.GetID())
        if self.libDict[name].getLabelVolume() is not None:
            compNode.SetReferenceLabelVolumeID(self.libDict[name].getLabelVolume().GetID())
        slicer.app.layoutManager().resetSliceViews()
    
    ## Function that will set up the volumes from a particular ndLibrary for the dropdown menu
    def setupLibrary(self, library):
        if not isinstance(library, ndLibrary):
            print("Not a library")
            return
        self.clear()
        for key in library.getEntireVolumeSet():
            self.addItem(key)
            self.libDict[key] = library