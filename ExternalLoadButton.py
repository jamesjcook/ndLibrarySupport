## Class for the external loading of a desired volume file not present in the atlas files
## Author: Austin Kao

## Tinkering: connect to slicer.app.coreIOManager().newFileLoaded signal
## File is already loaded when signal is emitted though...
'''
def test(properties):
    print("Properties are")
    print(properties)
    properties['show'] = False
    print(properties)
'''

class ExternalLoadButton(qt.QPushButton):
    ## nodeTag is the tag of the node the button is placed in
    def __init__(self, nodeTag):
        super(qt.QPushButton, self).__init__()
        self.text = "Load External Volume"
        self.released.connect(self.loadExternalVolume)
        self.nodeTag = nodeTag
        slicer.app.layoutManager().sliceWidget(nodeTag).layout().addWidget(self)
    
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
        ## openAddDataDialog() method does not return until user chooses to load something or not
        ## Create new method to open a file dialog that behaves as expected?
        result = slicer.app.coreIOManager().openAddDataDialog()
        if result == False:
            # result may be false even if we loaded. Will have to read docs on why.
            # For now alternative is to check if bg id changed.
            #print("AddDataDialog returned False")
            #return
            pass
            # This whole function works by abusing the default of "reset slice to new data" on load.
        # When we load data, all viewers are pointed at new data, after that we restore view.
        externalLoadNode = slicer.app.mrmlScene().GetNodeByID(externalLoadID)
        externalLoadNode.SetReferenceLabelVolumeID("None")
        for node in compNodes:
            if node.GetID() != externalLoadID:
                if node.GetBackgroundVolumeID() == volumes[node][0]:
                    # if we didnt change background id(eg we didnt load), skip this reset.
                    continue
                node.SetBackgroundVolumeID(volumes[node][0])
                node.SetForegroundVolumeID(volumes[node][1])
                node.SetReferenceLabelVolumeID(volumes[node][2])
                sliceWidget = slicer.app.layoutManager().sliceWidget(node.GetSingletonTag())
                if sliceWidget is not None:
                    sliceWidget.fitSliceToBackground()