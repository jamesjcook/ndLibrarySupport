## An object that instantiates different GUI elements and manages the ndLibrary data for each of them
## To run in Slicer, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\ndLibraryViewerInit.py")
## Author: Austin Kao

def initializeNDLibraryViewer(rootDir):
    if not os.path.isdir(rootDir):
        print("Please specify a valid path")
        return
    masterLib = ndLibrary(None, rootDir)
    menu = DataPackageMenu(masterLib.getRelevantStrainList())