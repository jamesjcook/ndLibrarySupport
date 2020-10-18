## For the functions of the 2D atlas that allow you to click on regions of the brain
## and toggle a label outline over that region
## Author: Austin Kao

class InteractiveLabelSelector:
    ## library specifies the ndLibrary the InteractiveLabelSelector is supposed to manage labels for
    ## nodeTag is the tag of the slice node that the push buttons are supposed to reside in
    ## Use the Colors module in 3D Slicer to toggle the opacity of a specific label
    ## allPushButton is a button that will make all relevant labels visible
    ## nonePushButton is a button that will make all relevant labels invisible
    ## Adds a "Visible" column to the table of colors found in the Colors module
    def __init__(self, library, nodeTag):
        if not isinstance(nodeTag, str):
            print("Tag is not a string")
            return
        if slicer.app.layoutManager().sliceWidget(nodeTag) is None:
            print("Invalid tag")
            return
        widget = slicer.modules.colors.widgetRepresentation()
        frame1 = widget.findChild("QFrame")
        self.comboBox = frame1.findChild("qMRMLColorTableComboBox", "ColorTableComboBox")
        clt_display = widget.findChild("ctkCollapsibleButton", "DisplayCollapsibleButton")
        self.tableView = clt_display.findChild("qMRMLColorTableView")
        self.tableView.activated.connect(self.processTableViewClick)
        self.tableView.model().insertColumn(3)
        self.tableView.model().setHeaderData(3, 1, 'Visible')
        self.allPushButton = qt.QPushButton("Turn on all labels")
        self.nonePushButton = qt.QPushButton("Turn off all labels")
        self.allPushButton.released.connect(self.turnOnLabels)
        self.nonePushButton.released.connect(self.turnOffLabels)
        #insert(through theft from data probe) label line to bottom of window
        statusBar = slicer.util.mainWindow().findChildren('QStatusBar')[0]
        regionLabel = slicer.modules.DataProbeInstance.infoWidget.layerValues["L"]
        #regionLabel.setMinimumHeight(regionLabel.minimumSizeHint.height()*2)
        #mainMenuBar = slicer.util.mainWindow().findChild("QMenuBar", "menubar")
        statusBar.addWidget(regionLabel)
        statusBar.setMinimumHeight(statusBar.height*2.1)
        #mainMenuBar.addWidget(statusBar)
        qtLayout = slicer.app.layoutManager().sliceWidget(nodeTag).layout()
        self.nodeTag = nodeTag
        qtLayout.addWidget(self.allPushButton)
        qtLayout.addWidget(self.nonePushButton)
        sliceNames = slicer.app.layoutManager().sliceViewNames()
        for sliceTag in sliceNames:
            sliceNodeInteractor = slicer.app.layoutManager().sliceWidget(sliceTag).sliceView().interactor()
            sliceNodeInteractor.AddObserver('LeftButtonReleaseEvent', self.processSliceViewClick)
        if library is not None:
            self.setupLibrary(library)
    
    ## Sets the "Hide colors" check box found just above the table of colors
    ## "Hide colors", when checked, hides any unused colors in the table of colors
    def setHideColorsCheckState(self, value):
        widget = slicer.modules.colors.widgetRepresentation()
        clt_display = widget.findChild("ctkCollapsibleButton", "DisplayCollapsibleButton")
        hideColors = clt_display.findChild("QCheckBox")
        hideColors.setCheckState(value)
    
    ## Function to set the current active ndLibrary of an InteractiveLabelSelector
    def setupLibrary(self, library):
        if not isinstance(library, ndLibrary):
            print("Invalid library used")
            return
        self.library = library
        if library.getColorTableNode() is None:
            print("Lookup table not available")
            return
        self.comboBox.currentNodeID = u'' + library.getColorTableNode().GetID()
        self.setHideColorsCheckState(0)
        numRows = self.tableView.colorModel().rowCount()
        for i in range(0, numRows):
            opacityIndex = self.tableView.model().index(i, 2)
            opacity = float(self.tableView.model().data(opacityIndex))
            visibleIndex = self.tableView.model().index(i, 3)
            if opacity == 0:
                self.tableView.model().setData(visibleIndex, 'No')
            else:
                self.tableView.model().setData(visibleIndex, 'Yes')
        self.setHideColorsCheckState(2)

    
    ## Turns off all labels for a LabelMapVolumeNode
    def turnOffLabels(self):
        self.setLabelOpacity(0)
    
    ## Turns on all relevant labels for a LabelMapVolumeNode
    def turnOnLabels(self):
        self.setLabelOpacity(1)
    
    ## Sets the opacity of the labels to a certain value
    ## Skips opacity of region 0: assumed to be Exterior
    def setLabelOpacity(self, value):
        idDict = dict()
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        for node in compNodes:
            idDict[node] = node.GetLabelVolumeID()
            node.SetReferenceLabelVolumeID("None")
        colorTable = self.library.getColorTableNode()
        labelDict = self.library.getLabelDict()
        self.comboBox.currentNodeID = u'' + colorTable.GetID()
        numRows = self.tableView.colorModel().rowCount()
        for i in range(0, numRows):
            #if labelDict.has_key(i) and i != 0:
            if i in labelDict and i != 0:
                colorTable.SetOpacity(i, value)
                index = self.tableView.model().index(i, 3)
                if value == 0:
                    self.tableView.model().setData(index, 'No')
                else:
                    self.tableView.model().setData(index, 'Yes')
        for node in compNodes:
            node.SetReferenceLabelVolumeID(idDict[node])
    
    ## Function that toggles the color of a label for a selected row in the table of colors
    def processTableViewClick(self, index):
        roiNum = index.row()
        self.toggleColor(roiNum)
    
    ## Function that toggles the color of a label for a slice view
    def processSliceViewClick(self, observee, event):
        regionValue = slicer.modules.DataProbeInstance.infoWidget.layerValues["L"].text
        if regionValue == "" or regionValue == u"<b>Out of Frame</b>":
            return
        values = regionValue.split(" ")
        roiNum = values[len(values)-1].replace("(","")
        roiNum = roiNum.replace(")</b>","")
        roiNum = int(roiNum)
        self.toggleColor(roiNum)
    
    ## Function that toggles the opacity of a region in the slice view
    ## Function will change the lookup table in the colors modules in Slicer to the one found in a specific library
    ## In the future, maybe change lookup table to the one being used by the labelmap volume?
    ## Double clicking a particular row will change the opacity value between 0 and 1        
    def toggleColor(self, roiNum):
        if roiNum == 0:
            return
        colorTable = self.library.getColorTableNode()
        if colorTable is None:
            return
        self.comboBox.currentNodeID = u'' + colorTable.GetID()
        rowNum = self.library.getRowNum(roiNum)
        if rowNum is None:
            rowNum = roiNum
            roiNum = self.library.getRegionNum(rowNum)
        opacityIndex = self.tableView.model().index(rowNum, 2)
        visibleIndex = self.tableView.model().index(rowNum, 3)
        #print(self.tableView.model().data(opacityIndex))
        if self.tableView.model().data(opacityIndex) == None:
            print("Opacity data not present")
            return
        opacity = float(self.tableView.model().data(opacityIndex))
        if opacity == 0:
            colorTable.SetOpacity(roiNum, 1)
            self.tableView.model().setData(visibleIndex, 'Yes')
        else:
            colorTable.SetOpacity(roiNum, 0)
            self.tableView.model().setData(visibleIndex, 'No')