## Test script to set up Slicer environment for 2D Atlas and load in a specimen
## To run, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\Average_Rat_Test.py")
## Author: Austin Kao

## Load necessary classes and layout
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\TwoDComparisonView.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\ndLibrary.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\VolumeDropdown.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\LabelTextProbe.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\InteractiveLabelSelector.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\ExternalLoadButton.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\DataPackageMenu.py")
## Set up/build necessary UI elements
setTwoDComparisonView()
setLabelOutlineAtlas(1)
## Read lib.conf files to determine volume to load
example_lib = ndLibrary(None, r"D:\Libraries\010Rat_Brain\v2020-06-25\23Rat")
#example_lib.loadEntire()
#print(example_lib.file_loc)
#example_lib.loadVolumes()
#example_lib.loadLabels()
#example_lib.loadTrackTransform()
dropdown1 = volumeDropdown(example_lib, "Compare1")
dropdown2 = volumeDropdown(example_lib, "Compare2")
dropdown3 = volumeDropdown(example_lib, "Nav")
labelSelector = InteractiveLabelSelector(example_lib, "Nav")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\AngleSlider.py")
externalLoad = ExternalLoadButton("Load")
angleSlider = AngleSlider("Nav", "Compare1", "Compare2")