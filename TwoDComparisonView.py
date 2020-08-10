## Layout specifications for 2D Atlas
## Based on code originally written by Alex Sheu
## To run, type: execfile("D:\CIVM_Apps\Slicer\FiberCompareView\\2D_Atlas\\TwoDComparisonView.py")
## Modified by Austin Kao

def setTwoDComparisonView():
    customLayout = ("<layout type=\"vertical\">"
      " <item>"
      "  <layout type=\"horizontal\">"
      "   <item>"
      "    	<view class=\"vtkMRMLSliceNode\" singletontag=\"Nav\">"
      "      <property name=\"orientation\" action=\"default\">Sagittal</property>"
      "      <property name=\"viewlabel\" action=\"default\">Nav</property>"
      "      <property name=\"viewcolor\" action=\"default\">#6EB04B</property>"
      "     <property name=\"viewgroup\" action=\"default\">1</property>"
      "   	</view>"
      "   </item>"
      "   <item>"
      "    	<view class=\"vtkMRMLSliceNode\" singletontag=\"Load\">"
      "      <property name=\"orientation\" action=\"default\">Coronal</property>"
      "      <property name=\"viewlabel\" action=\"default\">Load</property>"
      "      <property name=\"viewcolor\" action=\"default\">#909090</property>"
      "   	</view>"
      "   </item>"
      "  </layout>"
      " </item>"
      " <item>"
      "  <layout type=\"horizontal\">"
      "   <item>"
      "    <view class=\"vtkMRMLSliceNode\" singletontag=\"Compare1\">"
      "     <property name=\"orientation\" action=\"default\">Coronal</property>"
      "     <property name=\"viewlabel\" action=\"default\">C1</property>"
      "     <property name=\"viewcolor\" action=\"default\">#EDD54C</property>"
      "     <property name=\"viewgroup\" action=\"default\">1</property>"
      "    </view>"
      "   </item>"
      "   <item>"
      "    <view class=\"vtkMRMLSliceNode\" singletontag=\"Compare2\">"
      "     <property name=\"orientation\" action=\"default\">Coronal</property>"
      "     <property name=\"viewlabel\" action=\"default\">C2</property>"
      "     <property name=\"viewcolor\" action=\"default\">#f6e9a2</property>"
      "     <property name=\"viewgroup\" action=\"default\">1</property>"
      "    </view>"
      "   </item>"
      "  </layout>"
      " </item>"
      "</layout>")
    customLayoutId=586
    layoutManager = slicer.app.layoutManager()
    layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(customLayoutId, customLayout)
    layoutManager.setLayout(586)

def setSliceNodeLinks(value):
    slicer.util.getNode("vtkMRMLSliceCompositeNodeCompare1").SetLinkedControl(value)
    slicer.util.getNode("vtkMRMLSliceCompositeNodeCompare2").SetLinkedControl(value)

def setLabelOutlineAtlas(num):
    slicer.util.getNode("vtkMRMLSliceNodeNav").SetUseLabelOutline(num)
    slicer.util.getNode("vtkMRMLSliceNodeCompare1").SetUseLabelOutline(num)
    slicer.util.getNode("vtkMRMLSliceNodeCompare2").SetUseLabelOutline(num)