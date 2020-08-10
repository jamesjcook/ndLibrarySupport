## Class for the external loading of a desired volume file
## Author: Austin Kao

## Tinkering: connect to slicer.app.coreIOManager().newFileLoaded signal
## File is already loaded though...
'''
def test(properties):
    print("Properties are")
    print(properties)
    properties['show'] = False
    print(properties)

def test1():
    print("hi")

def test2(string):
    print(string)
'''

class ExternalLoadButton(qt.QPushButton):
    def __init__(self, nodeTag):
        self.button = qt.QPushButton("Load External Volume")
        self.button.released.connect(self.loadExternalVolume)
        self.nodeTag = nodeTag
        slicer.app.layoutManager().sliceWidget(nodeTag).layout().addWidget(self.button)
    
    ## Function to load an external volume that the user chooses
    ## Currently lets user load in nodes like normal, then sets the scene so that loaded volume appears only
    ## in the external load node (whereever the button is located)
    def loadExternalVolume(self):
        compNodes = slicer.app.mrmlScene().GetNodesByClass("vtkMRMLSliceCompositeNode")
        volumes = dict()
        externalLoadID = "vtkMRMLSliceCompositeNode"+str(self.nodeTag)
        for node in compNodes:
            if node.GetID() != externalLoadID:
                volumes[node] = (node.GetBackgroundVolumeID(), node.GetForegroundVolumeID(), node.GetLabelVolumeID())
        result = slicer.app.coreIOManager().openAddDataDialog()
        if result == False:
            return
        externalLoadNode = slicer.app.mrmlScene().GetNodeByID(externalLoadID)
        externalLoadNode.SetReferenceLabelVolumeID("None")
        for node in compNodes:
            if node.GetID() != externalLoadID:
                node.SetBackgroundVolumeID(volumes[node][0])
                node.SetForegroundVolumeID(volumes[node][1])
                node.SetReferenceLabelVolumeID(volumes[node][2])