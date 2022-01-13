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
        # for our table view, since we only use 0/1 opacity, we'll get clever and use opacity as index into this array.
        self.opacity_text=['No','Yes']
        #insert(through theft from data probe) label line to bottom of window
        statusBar = slicer.util.mainWindow().findChildren('QStatusBar')[0]
        
        self.status_label = qt.QLabel("ActiveLibrary")
        statusBar.addWidget(self.status_label)
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
        self.library=None
        if library is not None:
            self.setupLibrary(library)
        else:
            self.library = library
    
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
        self.status_label.setText(library.conf["LibName"])
        self.comboBox.currentNodeID = u'' + library.getColorTableNode().GetID()
        self.setHideColorsCheckState(0)
        for row_num in range(0, self.tableView.colorModel().rowCount()):
            cname_index = self.tableView.model().index(row_num, 1)
            cname = self.tableView.model().data(cname_index)
            if 'Exterior' in cname or 'Background' in cname:
                continue
            opacity_index = self.tableView.model().index(row_num, 2)
            visible_index = self.tableView.model().index(row_num, 3)
            opacity = float(self.tableView.model().data(opacity_index))
            self.tableView.model().setData(visible_index, self.opacity_text[round(opacity)])
        self.setHideColorsCheckState(2)
    
    ## Turns off all labels for a LabelMapVolumeNode
    def turnOffLabels(self):
        self.setAllLabelOpacity(0)
    
    ## Turns on all relevant labels for a LabelMapVolumeNode
    def turnOnLabels(self):
        self.setAllLabelOpacity(1)
    
    ## Sets the opacity of the labels to a certain value
    ## Skips opacity of region 0: assumed to be Exterior
    def setAllLabelOpacity(self, opacity_value):
        if self.library is None:
            print("Library not ready")
            return
        idDict = dict()
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        # do in background, by taking label volume out of view
        # print("hide labels start")
        for node in compNodes:
            idDict[node] = node.GetLabelVolumeID()
            node.SetReferenceLabelVolumeID("None")
        # print("hide labels end")
        colorTable = self.library.getColorTableNode()
        self.comboBox.currentNodeID = u'' + colorTable.GetID()
        #colorTable.GetColorName(clr_num)
        #colorTable.GetNoName()
        #colorTable.GetNumberOfColors()
        #for row_num in range(0, self.tableView.colorModel().rowCount()):
        # color number is our roi number + any blanks for rois not filled in, blanks are named colorTable.GetNoName()
        for clr_num in range(0, colorTable.GetNumberOfColors()):
            # this is coming in as a none! but why!
            cname = colorTable.GetColorName(clr_num)
            if cname == colorTable.GetNoName() or 'Exterior' in cname or 'Background' in cname:
                continue
            row_num = self.tableView.rowFromColorIndex(clr_num)
            status_print="c:"+str(clr_num)+"r:"+str(row_num)
            current_color=[-1,-1,-1,-1]
            status_get_color=colorTable.GetColor(clr_num,current_color)
            if status_get_color:
                current_opacity=current_color[3]
            else:
                try:
                    opacity_index = self.tableView.model().index(row_num, 2)
                    current_opacity = float(self.tableView.model().data(opacity_index))
                except:
                    print("  skip, no opacity")
                    continue
            if round(current_opacity) == opacity_value:
                # print(status_print+" skip")
                continue
            #cname_index = self.tableView.model().index(row_num, 1)
            #cname = self.tableView.model().data(cname_index)
            visible_index = self.tableView.model().index(row_num, 3)
            colorTable.SetOpacity(clr_num, opacity_value)
            self.tableView.model().setData(visible_index, self.opacity_text[round(current_opacity)])
            # print(status_print+" set")
        # print("show labels")
        for node in compNodes:
            node.SetReferenceLabelVolumeID(idDict[node])
        # print("show labels end")
    
    ## Function that toggles the color of a label for a selected row in the table of colors
    def processTableViewClick(self, index):
        row_num = index.row()
        cname_index = self.tableView.model().index(row_num, 1)
        cname = self.tableView.model().data(cname_index)
        self.toggleColor(self.library.getLabelDict()[cname][0])
    
    ## Function that toggles the color of a label for a slice view
    def processSliceViewClick(self, observee, event):
        regionValue = slicer.modules.DataProbeInstance.infoWidget.layerValues["L"].text
        if regionValue == "" or regionValue == u"<b>Out of Frame</b>":
            return
        #read the TEXT (HAHaha) of the data probe! extracting the number between parenthesis!
        values = regionValue.split(" ")
        roi_num = values[len(values)-1].replace("(","")
        roi_num = roi_num.replace(")</b>","")
        # print("Toggle: "+roi_num)
        roi_num = int(roi_num)
        self.toggleColor(roi_num)
        # print("   IN processSliceViewClick")
        # print(self.library.fiducial_list)
        # print(self.library.conf["LibName"])
        
        if "AnnotationMode" not in self.library.conf:
            return
        ## BAD BAD PLACEMENT -- fix this
        ## save the fiducial list on every click in the scene (this method also triggered when placing a fiducial)
        slicer.util.saveNode(self.library.fiducial_list[1], self.library.fiducial_list[0])
    
    ## Function that toggles the opacity of a region in the slice view
    ## Function will change the lookup table in the colors modules in Slicer to the one found in a specific library
    ## In the future, maybe change lookup table to the one being used by the labelmap volume?
    ## Double clicking a particular row will change the opacity value between 0 and 1        
    def toggleColor(self, roi_num):
        if roi_num == 0:
            return
        colorTable = self.library.getColorTableNode()
        if colorTable is None:
            print("no color table available")
            return
        cname = colorTable.GetColorName(roi_num)
        if cname == colorTable.GetNoName() or 'Exterior' in cname or 'Background' in cname:
            print("skip toggle on "+cname)
            return
        #self.comboBox.currentNodeID = u'' + colorTable.GetID()
        row_num = self.tableView.rowFromColorIndex(roi_num)
        if row_num is None:
            print("problem in finding tableview row_num from roi_num(color number)")
        #opacity_index = self.tableView.model().index(row_num, 2)
        visible_index = self.tableView.model().index(row_num, 3)
        current_color=[-1,-1,-1,-1]
        status_get_color=colorTable.GetColor(roi_num,current_color)
        #if self.tableView.model().data(opacity_index) is not None:
        if status_get_color:
            opacity_value=current_color[3]
        else:
            print("Opacity data not present")
            return
        # get current
        #opacity_value = float(self.tableView.model().data(opacity_index))
        # flippit
        opacity_value=not round(opacity_value);
        colorTable.SetOpacity(roi_num, opacity_value)
        self.tableView.model().setData(visible_index, self.opacity_text[opacity_value])
    
