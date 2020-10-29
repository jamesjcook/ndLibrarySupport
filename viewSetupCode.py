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
    nodes = slicer.util.getNodesByClass("vtkMRMLSliceCompositeNode")
    node_link=dict()
    for node in nodes:
        node_link[node.GetID()] = node.GetLinkedControl()
        node.SetLinkedControl(0)
    #SliceFOVMatch2DViewSpacingMatchVolumes 
    #SliceResolutionMatchVolumes
    node=slicer.util.getNode("vtkMRMLSliceNodeNavigator")
    node.SetSliceResolutionMode (node.SliceFOVMatch2DViewSpacingMatchVolumes)
    node.SetSliceVisible(True)
    node=slicer.util.getNode("vtkMRMLSliceNodeCompare1")
    node.SetSliceResolutionMode (node.SliceFOVMatch2DViewSpacingMatchVolumes)
    node.SetSliceVisible(True)
    for node in nodes:
        if node.GetID() in node_link:
            node.SetLinkedControl(node_link[node.GetID()])
    #layoutManager = slicer.app.layoutManager()
    #for sliceViewName in layoutManager.sliceViewNames():
    #  controller = layoutManager.sliceWidget(sliceViewName).sliceController()
    #  controller.setSliceVisible(True)
    
