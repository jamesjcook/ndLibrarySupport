## Simple view control functions 
## We dont know how we want to create a class for view protocol handling,
## So we're throwing loose helper functions in here for now.



## Function that links Compare1 and Compare2 slice view nodes
def setSliceNodeLinks(value):
    slicer.util.getNode("vtkMRMLSliceCompositeNodeCompare1").SetLinkedControl(value)
    slicer.util.getNode("vtkMRMLSliceCompositeNodeCompare2").SetLinkedControl(value)

## Function that sets label outline (See the outline of label instead of solid color)
def setLabelOutlineAtlas(num):
    slicer.util.getNode("vtkMRMLSliceNodeNavigator").SetUseLabelOutline(num)
    slicer.util.getNode("vtkMRMLSliceNodeCompare1").SetUseLabelOutline(num)
    slicer.util.getNode("vtkMRMLSliceNodeCompare2").SetUseLabelOutline(num)

def showSlicesInNavigator():
    # Save current link status, and unlink
    nodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
    node_link=dict()
    for node in nodes:
        node_link[node.GetID()] = node.GetLinkedControl()
        node.SetLinkedControl(0)
    # Set resolution mode
    nodes = slicer.util.getNodesByClass("vtkMRMLSliceNode")
    for node in nodes:
        #node.SetSliceResolutionMode(node.SliceFOVMatch2DViewSpacingMatchVolumes)
        node.SetSliceResolutionMode(node.SliceResolutionMatchVolumes)
        node.SetSliceVisible(False)
    node=slicer.util.getNode("vtkMRMLSliceNodeNavigator")
    node.SetSliceVisible(True)
    node=slicer.util.getNode("vtkMRMLSliceNodeCompare1")
    node.SetSliceVisible(True)
    nodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
    for node in nodes:
        if node.GetID() in node_link:
            node.SetLinkedControl(node_link[node.GetID()])
    #layoutManager = slicer.app.layoutManager()
    #for sliceViewName in layoutManager.sliceViewNames():
    #  controller = layoutManager.sliceWidget(sliceViewName).sliceController()
    #  controller.setSliceVisible(True)
    
