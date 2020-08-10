## Class for a dropdown menu that lists all the data packages available for an atlas
## To run in Slicer, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\DataPackageMenu.py")
## Author: Austin Kao

#class DataPackageMenu(qt.QMenu):
class DataPackageMenu(qt.QMenu):
    '''
    ## Function to update GUI elements with a selected ndLibrary
    ## GUI elements should be able to use volumes for the added library
    def loadLibrary(self, index):
        name = self.itemText(index)
        #print("Hey this is working")
        #print(name)
        lib = self.packageDict[name]
        self.controller.setUpLibrary(lib)
    '''
    def __init__(self, ndLibraries):
        if not isinstance(ndLibraries, list):
            print("Not a list")
            return
        #super(qt.QComboBox, self).__init__()
        super(qt.QMenu, self).__init__()
        print("Trying to create menu")
        mainWindow = slicer.app.activeWindow()
        mainMenuBar = mainWindow.findChild("QMenuBar", "menubar")
        mainMenuBar.addMenu(self)
        self.title = "Data Packages"
        for toolbar in mainWindow.findChildren("QToolBar"):
            toolbar.setVisible(0)
        #menuLabel = qt.QLabel("Data packages:")
        #newToolBar = qt.QToolBar()
        #mainWindow.addToolBar(newToolBar)
        #newToolBar.addWidget(menuLabel)
        #newToolBar.addWidget(self)
        self.controller = AtlasController(ndLibraries)
        #self.packageDict = dict()
        for lib in ndLibraries:
            if not isinstance(lib, ndLibrary):
                continue
            name = lib.file_loc
            #if lib.fields.has_key("Strain") and lib.fields.has_key("LibName"):
            if "Strain" in lib.fields and "LibName" in lib.fields:
                name = lib.fields["Strain"] + " " + lib.fields["LibName"]
            elif "LibName" in lib.fields:
                name = lib.fields["LibName"]
            #self.packageDict[name] = lib
            #self.addItem(name)
            menuItem = qt.QAction(name, self)
            self.addAction(menuItem)
            def loadRelevantLibrary():
                self.controller.setUpLibrary(lib)
            menuItem.triggered.connect(loadRelevantLibrary)
        #self.activated.connect(self.loadLibrary)