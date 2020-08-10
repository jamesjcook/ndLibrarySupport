## Script to test new library file locations
## To run, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\Simplified_Atlas_Test.py")
## Author: Austin Kao

## Load necessary classes and layout
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\TwoDComparisonView.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\ndLibrary.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\VolumeDropdown.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\LabelTextProbe.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\InteractiveLabelSelector.py")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\ExternalLoadButton.py")

## Read lib.conf files to determine volume to load
example_lib = ndLibrary(None, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\RatAvg2019\v2020-07-30")
#example_lib = ndLibrary(None, r"D:\Libraries\Brain\Rattus_norvegicus\Wistar\151124_3_1\v2020-07-30")

## Set up/build necessary UI elements
setLabelOutlineAtlas(1)
dropdown1 = volumeDropdown(example_lib, "Compare1")
dropdown2 = volumeDropdown(example_lib, "Compare2")
dropdown3 = volumeDropdown(example_lib, "Nav")
labelSelector = InteractiveLabelSelector(example_lib, "Nav")
execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\AngleSlider.py")
externalLoad = ExternalLoadButton("Load")