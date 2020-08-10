## An object that instantiates different GUI elements and manages the ndLibrary data for each of them
## To run in Slicer, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\AtlasController.py")
## Author: Austin Kao

## Could easily be merged with DataPackageMenu... may be better to do so?
## DataPackageMenu is meant to represent the menu itself, and not the underlying processes that set up the atlas
## AtlasController is meant to represent an object that handles the ndLibrary data GUI elements are using
class AtlasController():
    ## Function that sets up the ndLibrary selected from the DataPackageMenu
    def setUpLibrary(self, library):
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        for node in compNodes:
            node.SetBackgroundVolumeID("None")
            node.SetForegroundVolumeID("None")
            node.SetLabelVolumeID("None")
        self.drop1.setupLibrary(library)
        self.drop2.setupLibrary(library)
        self.dropNav.setupLibrary(library)
        self.labelSelector.setupLibrary(library)
    def __init__(self, ndLibraries):
        if not isinstance(ndLibraries, list):
            print("Not a list")
            return
        setTwoDComparisonView()
        setLabelOutlineAtlas(1)
        setSliceNodeLinks(1)
        self.libraries = ndLibraries
        self.drop1 = volumeDropdown(None, "Compare1")
        self.drop2 = volumeDropdown(None, "Compare2")
        self.dropNav = volumeDropdown(None, "Nav")
        self.externalLoad = ExternalLoadButton("Load")
        self.labelSelector = InteractiveLabelSelector(None, "Nav")
        self.angleSlider = AngleSlider("Nav", "Compare1", "Compare2")
        window = slicer.util.mainWindow()
        pythonWidget = window.findChild("QDockWidget", "PythonConsoleDockWidget")
        pythonWidget.setVisible(0)
        panelWidget = window.findChild("QDockWidget", "PanelDockWidget")
        panelWidget.setVisible(0)
        compNodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
        for node in compNodes:
            node.SetSliceIntersectionVisibility(1)