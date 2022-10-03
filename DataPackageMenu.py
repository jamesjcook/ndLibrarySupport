## Class for a dropdown menu that lists all the data packages available for an atlas
## Author: Austin Kao
import qt
import slicer

from AtlasController import AtlasController
from ndLibrary import ndLibrary

class DataPackageMenu(qt.QMenu):
    ## ndLibraries is the list of ndLibraries to be displayed in the data package menu
    ## Places menu in the top menu bar (With File, Edit, etc.)
    libDict = dict()
    firstInteraction = True
    flashTimer = qt.QTimer()
    def __init__(self, list_of_libraries, pack_name=None):
        if not isinstance(list_of_libraries, list):
            print("Not a list")
            return
        super(qt.QMenu, self).__init__()
        mainWindow = slicer.app.activeWindow()
        mainMenuBar = mainWindow.findChild("QMenuBar", "menubar")
        mainMenuBar.addMenu(self)
        # attempte to add qpushbutton direct fails.
        #button = qt.QPushButton
        #button.setMenu(self);
        #mainMenuBar.addMenu(button)
        #self.initStyleSheet = self.styleSheet
        if pack_name is not None:
            self.title=pack_name+" Packages"
        else:
            self.title = "Data Packages"
        ## Instantiate the controller of the ndLibraryViewer
        # TODO: two cobntrollers? based off of a setting in lib.conf, sensitivity to a child library called Atlas 
        # if i have an atlas child node, then make a second controller
        self.controller = AtlasController()
        self.populate_menu(list_of_libraries,pack_name)
        #self.setProperty("flashing", 0)
        self.flashTimer.timeout.connect(self.flashToggle)
        # Triggered didnt work to stop the timer, clicked, and entered don't exist, hovered seems to work
        # Trouble is: it floats in top left corner instead of on menu as expected.
        #self.triggered.connect(self.flashStop)
        #self.clicked.connect(self.flashStop)
        #self.entered.connect(self.flashStop)
        #self.aboutToShow.connect(self.flashStop)
        #self.hovered.connect(self.flashStop)
        #self.flashTimer.start(1500)
        #self.flashTimer.singleShot(500,self.flashStart)
    def populate_menu(self, list_of_libraries, pack_name=None):
        ## Create the items in the menu and attach functions to each one
        if pack_name is not None:
            self.title=pack_name+" Packages"
        else:
            self.title="Data Packages"
        for lib in list_of_libraries:
            if not isinstance(lib, ndLibrary):
                continue
            name = lib.file_loc
            if "Strain" in lib.conf and "LibName" in lib.conf:
                name = lib.conf["Strain"] + " " + lib.conf["LibName"]
            elif "LibName" in lib.conf:
                name = lib.conf["LibName"]
            menuItem = qt.QAction(name, self)
            self.addAction(menuItem)
            ## Define a function for the menu item to execute when selected
            ## MUST must be a lambda for this to work
            ## storing our lambda's for later so we can manually trigger them.
            self.libDict[name] = lambda instancedLoader, lib=lib: self.controller.setUpLibrary(lib)
            menuItem.triggered.connect(self.libDict[name])
            #menuItem.triggered.connect(self.flashStop())
            #menuItem.triggered.connect(self.setUpLib)
        
    def flashStart(self):
        self.flashTimer.start(1500)
    def flashToggle(self):
        if self.property("flashing") == 0:
            self.setProperty("flashing", 1)
            #self.setStyleSheet("QMenu::item {background-color: lightblue; }")
            self.hide();
        elif self.property("flashing") == 1:
            self.setProperty("flashing", 0)
            #self.setStyleSheet(self.initStyleSheet)
            #style()->unpolish(this);
            #style()->polish(this);
            self.show()
    def flashStop(self):
        if self.firstInteraction == True:
            print("flash stop")
            self.firstInteraction = False
            self.flashTimer.stop()
        #self.flashTimer.timeout.disconnect(self.flashToggle)
        #self.triggered.disconnect(self.flashStop)
