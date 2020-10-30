## An object that instantiates different GUI elements and manages the ndLibrary data for each of them
## Author: Austin Kao

## Could easily be merged with DataPackageMenu... may be better to do so?
## DataPackageMenu is meant to represent the menu itself, and not the underlying processes that set up the atlas
## AtlasController is meant to represent an object that handles the ndLibrary data GUI elements are using
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
    def setUpLibrary(self, library):
        self.library = library
        ## Add additional view setups if appropriate
        tract_path = os.path.join(self.library.Path,"tractography.mrml")
        if os.path.isfile(tract_path):
            if "TractographyDisplay" not in slicer.util.moduleNames():
                self.tractography_prompt()
            else:
                if "NavigatorWith3DAnd2DCompare" not in custom_layouts:
                    loadNavigatorWith3DAnd2D()
                    loadNavigatorWith3DAnd2DCompare()
                    setNavigatorWith3DAnd2DCompare()
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
            if orient_key in library.conf:
                ok=orient_key.replace("Orientation","")
                custom_orient[ok]=library.conf[orient_key]
        sliceNodes = slicer.util.getNodesByClass("vtkMRMLSliceNode")
        for node in sliceNodes:
            for opt in custom_orient:
                if opt in node.GetSingletonTag():
                    node.SetOrientation(custom_orient[opt])
            node.GetSingletonTag()
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
        loadNavigatorAnd2DCompare()
        setNavigatorAnd2DCompare()
        setLabelOutlineAtlas(1)
        setSliceNodeLinks(1)
        self.library = None
        ## Set up GUI elements
        self.drop1 = volumeDropdown(None, "Compare1")
        self.drop2 = volumeDropdown(None, "Compare2")
        self.dropNav = volumeDropdown(None, "Navigator")
        self.externalLoad = ExternalLoadButton("Load")
        self.labelSelector = InteractiveLabelSelector(None, "Navigator")
        self.angleSlider = AngleSlider("Navigator", "Compare1", "Compare2")
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
                self.mouseToolbar = toolbar
                #print(toolbar.name)
                #action=toolbar.actions()[1]
                for action in toolbar.actions():
                    if "Adjust" in action.name and "Window" in action.name:
                        if not action.isChecked():
                            action.toggle()
                            break
        slicer.util.selectModule("Colors")
        self.pythonconsole = mainWindow.findChild("QDockWidget", "PythonConsoleDockWidget")
        self.pythonconsole.setVisible(0)
        self.modulepanel = mainWindow.findChild("QDockWidget", "PanelDockWidget")
        self.modulepanel.setVisible(0)
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        for node in compNodes:
            node.SetSliceIntersectionVisibility(1)