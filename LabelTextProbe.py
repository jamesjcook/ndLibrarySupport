## Sets up the label text probe
## To run in Slicer, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\LabelTextProbe.py")
## Author: Austin Kao

class LabelTextProbe:
    def __init__(self, library):
        if not isinstance(library, ndLibrary) or not library.fields.has_key("Path"):
            print("Invalid library used")
            return
        #library.loadLabels()
        self.library = library
    
    def updateText(self, observee, event):
        regionValue = slicer.modules.DataProbeInstance.infoWidget.layerValues["L"].text
        if regionValue == "" or regionValue == u"<b>Out of Frame</b>":
            return
        nums = regionValue.split(" ")
        #print(nums[len(nums)-1])
        roiNum = nums[len(nums)-1].replace("(","")
        roiNum = roiNum.replace(")</b>","")
        roiNum = int(roiNum)
        roiLabel = self.library.getRegionLabel(roiNum)
        currentText = slicer.modules.DataProbeInstance.infoWidget.viewInfo.text
        slicer.modules.DataProbeInstance.infoWidget.viewInfo.text = currentText + " Region: " + roiLabel