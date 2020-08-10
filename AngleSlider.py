## Angle slider
## To run, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\AngleSlider.py")
## Author: Austin Kao

## Method that will rotate the node by the amount specified by the slider
## Makes use of the LR slider in the Reformat module to set rotation
## Copies coordinates so that Compare1 and Compare2 nodes will share the same rotation transformation
## TODO: fix bug where suspected rounding error will not calibrate position correctly

class AngleSlider(slicer.qMRMLLinearTransformSlider):
    def __init__(self, tag, comp1, comp2):
        super(slicer.qMRMLLinearTransformSlider, self).__init__()
        qtLayout = slicer.app.layoutManager().sliceWidget(tag).layout()
        qtLayout.addWidget(self)
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
        
    def rotateNode(self, num):
        self.nodeSelector.setCurrentNodeID(self.comp1)
        y = 1
        rad = num * math.pi/180
        newy = y*math.cos(rad) #-z*math.sin(rad)
        newz = y*math.sin(rad) #+z*math.cos(rad)
        newCoordinates = u"0,{},{}".format(newy,newz)
        self.coordinateWidget.coordinates = newCoordinates
        self.nodeSelector.setCurrentNodeID(self.comp2)
        self.coordinateWidget.coordinates = newCoordinates


