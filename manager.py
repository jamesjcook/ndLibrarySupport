import os
from FiducialClickerMenu import FiducialClickerMenu
from DataPackageMenu import DataPackageMenu
from ndLibrary import ndLibrary
from viewNavigatorAnd2DCompare import *
from viewNavigatorWithLoadAnd2DCompare import *
from viewNavigatorAndTallAxial import *
from viewSetupCode import *
## ndLibrarySupport manager class
## to create base library, and menu object.
## Also prompts user to get them started.
class manager:
    #module_logger = logging.getLogger('spam_application.auxiliary')
    #logger = logging.getLogger('ndLibrarySupport')
    #logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    def __init__(self,rootDir,categoryFilter=r'Species'):

        if not os.path.isdir(rootDir):
            print("Please specify a valid path")
            print(rootDir)
            return 1
        self.rootDir = rootDir
        self.categoryFilter = categoryFilter
        self.fiducial_menu = FiducialClickerMenu()
        self.menu = None
        self.setup_library(rootDir)
        # TODO: setup view code 
        loadNavigatorAnd2DCompare()
        loadNavigatorWithLoadAnd2DCompare()
        loadNavigatorAndTallAxial()
        setNavigatorWithLoadAnd2DCompare()
        setNavigatorAnd2DCompare()
        setNavigatorAndTallAxial()
        setLabelOutlineAtlas(1)
        setSliceNodeLinks(1)
        slicer.util.messageBox("Click "+self.menu.title+" menu to begin")
        #self.menu.setProperty("flashing", 0)
        
    def setup_library(self, rootDir):
        ## Create a tree of ndLibrary object where masterLib is the root
        self.library = ndLibrary(None, rootDir)
        libs=self.library.getLibsByCategory(self.categoryFilter)
        ## Create the menu of data packages to be used in the ndLibraryViewer
        ## DataPackageMenu will instantiate a controller object that will create the other GUI elements
        # Old method of filtering let the ndlibrary choose whom went into menu.
        # self.menu = DataPackageMenu(self.library.getRelevantStrainList())
        # new uses configurable category filter internal.
        if len(libs) == 0 :
            print("error, no libs matched {}".format(self.categoryFilter))
        if (self.menu is None):
            self.menu = DataPackageMenu(libs,self.library.conf["LibName"])
        else:
            self.menu.populate_menu(libs,self.library.conf["LibName"])