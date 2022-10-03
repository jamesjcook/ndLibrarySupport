## Angle slider
## Author: Austin Kao
import slicer

class AngleSlider(slicer.qMRMLLinearTransformSlider):
    ## tag is the tag of the slice node where the angle slider will be in
    ## comp1 is the tag of the first slice node to be rotated
    ## comp2 is the tag of the second slice node to be rotated
    ## Rotates between -200 and 200 degrees in the LR directions
    def __init__(self, node_tag, comp1, comp2):
        super(slicer.qMRMLLinearTransformSlider, self).__init__()
        self.node_tag = node_tag
        self.minimum = -200
        self.maximum = 200
        self.decimals = 2
        self.TypeOfTransform = 3
        self.valueChanged.connect(self.rotateNode)
        widget = slicer.modules.reformat.widgetRepresentation()
        rotationSliderBox = widget.findChild("ctkCollapsibleButton")
        rotationSliderBox = rotationSliderBox.findChild("ctkCollapsibleGroupBox", "RotationSlidersGroupBox")
        self.coordinateWidget = rotationSliderBox.findChild("ctkCoordinatesWidget")
        self.nodeSelector = widget.findChild("qMRMLNodeComboBox")
        self.comp1 = "vtkMRMLSliceNode" + comp1
        self.comp2 = "vtkMRMLSliceNode" + comp2
    ## Method that will rotate the node by the amount specified by the slider
    ## Makes use of the coordinate widget in the Reformat module to set rotation
    ## Sets Compare1 and Compare2 nodes to the same coordinates so the same transformation will be observed
    def rotateNode(self, num):
        qtLayout = slicer.app.layoutManager().sliceWidget(self.node_tag).layout()
        qtLayout.addWidget(self)
        self.nodeSelector.setCurrentNodeID(self.comp1)
        y = 1
        rad = num * math.pi/180
        newy = y*math.cos(rad) #-z*math.sin(rad)
        newz = y*math.sin(rad) #+z*math.cos(rad)
        newCoordinates = u"0,{},{}".format(newy,newz)
        self.coordinateWidget.coordinates = newCoordinates
        self.nodeSelector.setCurrentNodeID(self.comp2)
        self.coordinateWidget.coordinates = newCoordinates


