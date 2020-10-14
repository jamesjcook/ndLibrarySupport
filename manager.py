## ndLibrarySupport manager class
## to create base library, and menu object.
## Also prompts user to get them started.
class manager:
    def __init__(self,rootDir):
        if not os.path.isdir(rootDir):
            print("Please specify a valid path")
            return
        ## Create a tree of ndLibrary object where masterLib is the root
        self.library = ndLibrary(None, rootDir)
        ## Create the menu of data packages to be used in the ndLibraryViewer
        ## DataPackageMenu will instantiate a controller object that will create the other GUI elements
        self.menu = DataPackageMenu(self.library.getRelevantStrainList())
        slicer.util.messageBox("Click Data Packages menu to begin")