## Layout specifications for ndLibraryViewer
## Based on code originally written by Alex Sheu
## Modified by Austin Kao

## Function that creates the TwoDComparisonView layout and sets it
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
    # following copied per code on slicer discourse at:
    # https://discourse.slicer.org/t/slicer-crashes-when-adding-2-custom-layouts-in-startup-script/9071
    ## Add button to layout selector toolbar for this custom layout
    viewToolBar = slicer.util.mainWindow().findChild('QToolBar', 'ViewToolBar')
    layoutMenu = viewToolBar.widgetForAction(viewToolBar.actions()[0]).menu()
    layoutSwitchActionParent = layoutMenu  # use `layoutMenu` to add inside layout list, use `viewToolBar` to add next the standard layout list
    layoutSwitchAction = layoutSwitchActionParent.addAction("2D compare view with Navigator and bonus panel")
    layoutSwitchAction.setIcon(qt.QIcon(':Icons/Go.png'))
    layoutSwitchAction.setToolTip('2D Compare view')
    layoutSwitchAction.connect('triggered()', lambda layoutId = customLayoutId: slicer.app.layoutManager().setLayout(layoutId))


## Function that links Compare1 and Compare2 slice view nodes
def setSliceNodeLinks(value):
    slicer.util.getNode("vtkMRMLSliceCompositeNodeCompare1").SetLinkedControl(value)
    slicer.util.getNode("vtkMRMLSliceCompositeNodeCompare2").SetLinkedControl(value)

## Function that sets label outline (See the outline of label instead of solid color)
def setLabelOutlineAtlas(num):
    slicer.util.getNode("vtkMRMLSliceNodeNav").SetUseLabelOutline(num)
    slicer.util.getNode("vtkMRMLSliceNodeCompare1").SetUseLabelOutline(num)
    slicer.util.getNode("vtkMRMLSliceNodeCompare2").SetUseLabelOutline(num)

