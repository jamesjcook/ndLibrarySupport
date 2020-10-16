## Class for a dropdown menu that lists all the data packages available for an atlas
## Author: Austin Kao

class DataPackageMenu(qt.QMenu):
    ## ndLibraries is the list of ndLibraries to be displayed in the data package menu
    ## Places menu in the top menu bar (With File, Edit, etc.)
    libDict = dict()
    def __init__(self, ndLibraries):
        if not isinstance(ndLibraries, list):
            print("Not a list")
            return
        super(qt.QMenu, self).__init__()
        mainWindow = slicer.app.activeWindow()
        mainMenuBar = mainWindow.findChild("QMenuBar", "menubar")
        mainMenuBar.addMenu(self)
        self.title = "Data Packages"
        ## Instantiate the controller of the ndLibraryViewer
        self.controller = AtlasController()
        ## Create the items in the menu and attach functions to each one
        for lib in ndLibraries:
            if not isinstance(lib, ndLibrary):
                continue
            name = lib.file_loc
            if "Strain" in lib.fields and "LibName" in lib.fields:
                name = lib.fields["Strain"] + " " + lib.fields["LibName"]
            elif "LibName" in lib.fields:
                name = lib.fields["LibName"]
            menuItem = qt.QAction(name, self)
            self.addAction(menuItem)
            ## Define a function for the menu item to execute when selected
            ## MUST must be a lambda for this to work
            ## storing our lambda's for later so we can manually trigger them.
            self.libDict[name] = lambda instancedLoader, lib=lib: self.controller.setUpLibrary(lib)
            menuItem.triggered.connect(self.libDict[name])
            #menuItem.triggered.connect(self.setUpLib)
