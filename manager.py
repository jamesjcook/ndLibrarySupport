import os
from FiducialClickerMenu import FiducialClickerMenu
from DataPackageMenu import DataPackageMenu
from ndLibrary import ndLibrary
from AtlasController import AtlasController
from viewNavigatorAnd2DCompare import *
from viewNavigatorWithLoadAnd2DCompare import *
from viewNavigatorAndTallAxial import *
from viewTwoOverTwo import *
from viewSetupCode import *
## ndLibrarySupport manager class
## to create base library, and menu object.
## Also prompts user to get them started.
class manager:
    #module_logger = logging.getLogger('spam_application.auxiliary')
    #logger = logging.getLogger('ndLibrarySupport')
    #logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    def __init__(self,rootDir,categoryFilter=r'Species', prompt=True):
        print("prompt is {}".format(prompt))

        if not os.path.isdir(rootDir):
            print("Please specify a valid path")
            print(rootDir)
            return 1
        self.rootDir = rootDir
        self.categoryFilter = categoryFilter
        self.fiducial_menu = FiducialClickerMenu()
        self.menu = None
        self.comparison=False
        self.atlas_menu = None
        # dict of DataPackageMenus, eacho menu has a list of ndLibraries
        self.dict_of_menu_lists = dict()
        # sets up nodes in the scene
        loadNavigatorAnd2DCompare()
        loadNavigatorWithLoadAnd2DCompare()
        loadNavigatorAndTallAxial()
        setNavigatorWithLoadAnd2DCompare()
        setNavigatorAnd2DCompare()
        setNavigatorAndTallAxial()
        setTwoOverTwo()
        setLabelOutlineAtlas(1)
        setSliceNodeLinks(1)

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

        self.setup_library(rootDir)
        if prompt:
            slicer.util.messageBox("Click {} menu to begin".format(self.menu.title))
        #self.menu.setProperty("flashing", 0)
        
        
        
    def setup_library(self, rootDir):
        ## Create a tree of ndLibrary object where masterLib is the root
        self.library = ndLibrary(None, rootDir)
        if "ComparisonMany" in self.library.conf:
            self.comparison=True
            # then we are in new use case
            for child in self.library.children:
                if child.conf["LibName"] == self.library.conf["ComparisonMany"]:
                    libs=child.getLibsByCategory(self.categoryFilter)
                    break
        else:
            libs=self.library.getLibsByCategory(self.categoryFilter)
            static_comparison_lib=None
        
        if "ComparisonOne" in self.library.conf:
            for child in self.library.children:
                if child.conf["LibName"] == self.library.conf["ComparisonOne"]:
                    static_comparison_lib=child
                    break

        ## Create the menu of data packages to be used in the ndLibraryViewer
        ## DataPackageMenu will instantiate a controller object that will create the other GUI elements
        # Old method of filtering let the ndlibrary choose whom went into menu.
        # self.menu = DataPackageMenu(self.library.getRelevantStrainList())
        # new uses configurable category filter internal.
        list_of_views=None
        if self.comparison:
            # then we are in comparison mode. in this mode, we want two AtlasControllers
                # one connected to the "one" ie the atlas
                # one connected to the "many" ie the specimen to compare to the atlas
            # red green are atlas views
            #4 yellow are many comparison view
            list_of_views = ["Slice4", "Yellow"]

            # static_comparison_lib should  get its own AtlasController, but NOT a datapackagemenu
            # and he gets red green views
            # TODO: the atlas controller resets the view every time I change specimen in the DataPackageMenu
                # check if setUpLibrary has already been ran once and then don't run it again
                    # this did not work -- someone else is resetting the view? datapackagemenu?
            assert static_comparison_lib is not None
            static_comparison_list_of_views = ["Red", "Green"]
            self.static_comparison_controller = AtlasController(static_comparison_list_of_views)
            if self.static_comparison_controller.library is None:
                self.static_comparison_controller.setUpLibrary(static_comparison_lib)
        if len(libs) == 0 :
            print("error, no libs matched {}".format(self.categoryFilter))
        if self.menu is None:
            mainWindow = slicer.util.mainWindow()
            menu_bar = mainWindow.findChild("QMenuBar", "menubar")
            self.menu = DataPackageMenu(libs, menu_bar, self.library.conf["LibName"], list_of_views)
        else:
            # this never runs?
            self.menu.populate_menu(libs,self.library.conf["LibName"])
        # this is where we could auto load specified library if desired
        # TODO: 
        self.dict_of_menu_lists[self.menu.title] = libs


    def set_data_package(self, lib_name):
        # find which library to load first
        # then call atlascontroller setup
        for child in self.dict_of_menu_lists[self.menu.title]:
            if child.conf["LibName"] == lib_name:
                self.menu.controller.setUpLibrary(child)
                return child
        return None
