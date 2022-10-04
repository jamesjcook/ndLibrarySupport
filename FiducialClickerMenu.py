import slicer
import qt
import re 
import copy

## BAD BEHAVIOR -- children should not place themselves
## this class auto called on startup (just like Data Package menu)

## FiducialClickerMenu is a subclass of qt.QMenu
class FiducialClickerMenu(qt.QMenu):
    def __init__(self): 
        super(qt.QMenu, self).__init__()
        mainWindow = slicer.util.mainWindow()
        mainMenuBar = mainWindow.findChild("QMenuBar", "menubar")
        #mainMenuBar.addMenu(self)
        #self.title = r'Fiducial Clicker'
        
        
        ## find the mouse toolbar 
        a=slicer.util.mainWindow().findChildren("QToolBar")
        mouse_menu = None
        for x in a:
            if re.match(r'.*Mouse.*ToolBar.*', x.name):
                mouse_menu = x#.actions()
                
                
        ## action is a child of mouse_menu with text="Mouse Interaction"
        #action=mouse_menu.findChildren("QObject")[2]
        action=None
        for x in mouse_menu.findChildren("QObject"):
            try:
                if x.text == r"Mouse Interaction":
                    x.text = "Mouse Contrast Fiducial"
                    action = x
                    break
            except:
                pass
        if action:
            mainMenuBar.addAction(action)