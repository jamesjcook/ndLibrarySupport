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
        self.addItem(r"<To begin, select Data Package from menu of main application>")
        self.libDict = dict()
        self.activated.connect(self.changeVolume)
        if library is not None:
            self.setupLibrary(library)
            self.library = library
        #self.loadSignal = qt.QTimer()
        #self.loadSignal.timeout.connect(self.busySpinner)
        #self.loadSigA = r"|/-\\"
        #self.loadSigI = 0
        self.statusMessage = ""
        self.viewSet = False
    
    ## Function that will change the volume image being looked at
    ## Because of how the dropdown menu is set up, any entry in volDict should at least have a file path
    ## The corresponding volume may or may not be loaded
    ## If loaded, function will set the loaded volume into the associated slice node
    ## Function will load the requested volume and add it to volDict
    def changeVolume(self, index):
        name = self.itemText(index)
        #print(name)
        #print(self.libDict[name])
        if name not in self.libDict:
            return
        compString = "vtkMRMLSliceCompositeNode"+str(self.nodeTag)
        #sliceString = "vtkMRMLSliceNode"+str(self.nodeTag)
        compNode = slicer.app.mrmlScene().GetNodeByID(compString)
        self.statusMessage = "loading "+name+" ..."
        slicer.util.showStatusMessage(self.statusMessage)
        self.setItemText(index,self.statusMessage)
        slicer.util.mainWindow().update()
        #self.loadSignal.start(250)
        
        #if type(self.volDict) is tuple:
        #    volNode = self.volDict[key][1]
        #else:
        #    print("Bizarro code path")
        #    volNode = self.volDict[key][1]
        
        if type(self.libDict[name]) is tuple:
            print("error on "+name+" select, coder is off their rocker and passed tuple instead of ndLibrary")
            return
        volNode = self.libDict[name].get_volume_node(name)
        if volNode is not None:
            compNode.SetBackgroundVolumeID(volNode.GetID())
            self.statusMessage = ""
            self.setItemText(index,name)
        else:
            self.statusMessage=name+ " Error loading"
            self.setItemText(index,self.statusMessage)
        slicer.util.showStatusMessage(self.statusMessage)
        if self.libDict[name].getLabelVolume() is not None:
            compNode.SetReferenceLabelVolumeID(self.libDict[name].getLabelVolume().GetID())
        elif self.library.getLabelVolume() is not None:
            compNode.SetReferenceLabelVolumeID(self.library.getLabelVolume().GetID())
        #killtimer?
        #self.loadSignal.stop()
        if not self.viewSet:
            #slicer.app.layoutManager().resetSliceViews()
            sliceWidget = slicer.app.layoutManager().sliceWidget(self.nodeTag)
            sliceWidget.fitSliceToBackground()
            # Avoid starting at midline display for Navigator because of label transformation effects
            nW=slicer.app.layoutManager().sliceWidget("Navigator")
            val=nW.sliceController().sliceOffsetSlider().value
            #if "Navigator" in self.nodeTag:
            if abs(val) < 0.250:
                nW.sliceController().setSliceOffsetValue(0.250)
            self.viewSet = True
    # interface is DISABLED while loading so this is not possible
    # Maybe slicer.util.mainWindow().update() will force re-draw?
    #def busySpinner(self):
    #    self.loadSigI += 1
    #    self.loadSigI = self.loadSigI % len(self.loadSigA)
    #    slicer.util.showStatusMessage(self.statusMessage + " " +self.loadSigA[self.loadSigI])
    ## Function that will set up the volumes from a particular ndLibrary for the dropdown menu
    def setupLibrary(self, library):
        if not isinstance(library, ndLibrary):
            print("Not a library")
            return
        self.clear()
        self.library = library
        self.addItem(r"<Click here to select data volume>")
        volset = library.getEntireVolumeSet().copy()
        if library.vol_ordering in library.conf:
            sorting = library.conf[library.vol_ordering].split(',')
            #print("use sorting")
        else:
            sorting = None
        if sorting is not None:
            for key in sorting:
                if key in volset:
                    #print("insert "+key)
                    self.addItem(key)
                    if isinstance(volset[key], ndLibrary):
                        #print("key using sublib")
                        self.libDict[key] = volset[key]
                    else:
                        self.libDict[key] = library
                    del volset[key]
        for key in volset:
            self.addItem(key)
            self.libDict[key] = library