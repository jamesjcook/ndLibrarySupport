## Test script to set up Slicer environment for 2D Atlas and load in a specimen
## To run, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\Atlas_Test.py")
## Author: Austin Kao

## Load necessary classes and layout
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\main.py")

## Read lib.conf files to determine volume to load
example_lib = ndLibrary(None, r"D:\CIVM_Apps\Slicer\FiberCompareViewTestData\\090_Heritability")
## Load BTBT/MDT_BTBR example
label = None
if len(example_lib.children) == 1:
    child = example_lib.children[0]
    child.loadVolumes()
    child.loadLabels()
    child.loadTrackTransform()
    libList = list()
    libList.append(child)
    ## Instantiate DataPackageMenu
    menu = DataPackageMenu(libList)
    #label = LabelTextProbe(child)
    #data = slicer.modules.DataProbeInstance.infoWidget
    #data.CrosshairNodeObserverTag = data.CrosshairNode.AddObserver(slicer.vtkMRMLCrosshairNode.CursorPositionModifiedEvent, label.updateText)
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\AngleSlider.py")