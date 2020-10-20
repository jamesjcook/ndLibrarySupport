## An object that instantiates different GUI elements and manages the ndLibrary data for each of them
## Author: Austin Kao

## Could easily be merged with DataPackageMenu... may be better to do so?
## DataPackageMenu is meant to represent the menu itself, and not the underlying processes that set up the atlas
## AtlasController is meant to represent an object that handles the ndLibrary data GUI elements are using
class AtlasController(): ## Rename?
    ## Function that sets up the ndLibrary selected from the DataPackageMenu
    def setUpLibrary(self, library):
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        ## "Clear" the scene
        for node in compNodes:
            node.SetBackgroundVolumeID("None")
            node.SetForegroundVolumeID("None")
            node.SetLabelVolumeID("None")
        ## Update each GUI element accordingly
        self.drop1.setupLibrary(library)
        self.drop2.setupLibrary(library)
        self.dropNav.setupLibrary(library)
        self.labelSelector.setupLibrary(library)
    
    ## Currently only instantiated in DataPackageMenu
    def __init__(self):
        ## Set up the layout and slice view nodes
        setTwoDComparisonView()
        setLabelOutlineAtlas(1)
        setSliceNodeLinks(1)
        ## Set up GUI elements
        self.drop1 = volumeDropdown(None, "Compare1")
        self.drop2 = volumeDropdown(None, "Compare2")
        self.dropNav = volumeDropdown(None, "Nav")
        self.externalLoad = ExternalLoadButton("Load")
        self.labelSelector = InteractiveLabelSelector(None, "Nav")
        self.angleSlider = AngleSlider("Nav", "Compare1", "Compare2")
        ## Modify Slicer's main window
        ## Hide toolbars
        ## Set mouse interaction mode if its available
        ## Hides Python Interactor, module panel
        ## Makes slice intersections visible
        ## May be better to move this code outside the controller?
        mainWindow = slicer.util.mainWindow()
        for toolbar in mainWindow.findChildren("QToolBar"):
            toolbar.setVisible(0)
            if "Mouse" in toolbar.name:
                #print(toolbar.name)
                #action=toolbar.actions()[1]
                for action in toolbar.actions():
                    if "Adjust" in action.name and "Window" in action.name:
                        if not action.isChecked():
                            action.toggle()
                            break
        pythonWidget = mainWindow.findChild("QDockWidget", "PythonConsoleDockWidget")
        pythonWidget.setVisible(0)
        panelWidget = mainWindow.findChild("QDockWidget", "PanelDockWidget")
        panelWidget.setVisible(0)
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        for node in compNodes:
            node.SetSliceIntersectionVisibility(1)