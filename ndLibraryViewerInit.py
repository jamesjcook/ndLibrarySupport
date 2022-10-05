## An object that instantiates different GUI elements and manages the ndLibrary data for each of them
## Author: Austin Kao
## OBSOLETE Replaced by manager.py

## Function to initialize the ndLibraryViewer
def initializeNDLibraryViewer(rootDir):
    if not os.path.isdir(rootDir):
        self.logger.warning("Please specify a valid path")
        return
    ## Create a tree of ndLibrary object where masterLib is the root
    masterLib = ndLibrary(None, rootDir)
    ## Create the menu of data packages to be used in the ndLibraryViewer
    ## DataPackageMenu will instantiate a controller object that will create the other GUI elements
    menu = DataPackageMenu(masterLib.getRelevantStrainList())