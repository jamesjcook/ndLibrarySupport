## Layout specifications for ndLibraryViewer
## Based on code originally written by Alex Sheu
## Modified by Austin Kao

if "custom_layouts" not in locals():
    custom_layouts=dict()

## Function that creates the NavigatorAnd2DCompare layout and sets it
def loadNavigatorAndTallAxial():
    custom_layouts["NavigatorAndTallAxial"]=986
    customLayout = ("<layout type=\"horizontal\">"
      " <item>"
      "  <layout type=\"vertical\">"
      "   <item>"
      "    	<view class=\"vtkMRMLSliceNode\" singletontag=\"Navigator\">"
      "      <property name=\"orientation\" action=\"default\">Sagittal</property>"
      "      <property name=\"viewlabel\" action=\"default\">Nav</property>"
      "      <property name=\"viewcolor\" action=\"default\">#6EB04B</property>"
      "     <property name=\"viewgroup\" action=\"default\">1</property>"
      "   	</view>"
      "   </item>"
      "   <item>"
      "    <view class=\"vtkMRMLSliceNode\" singletontag=\"Compare1\">"
      "     <property name=\"orientation\" action=\"default\">Coronal</property>"
      "     <property name=\"viewlabel\" action=\"default\">C1</property>"
      "     <property name=\"viewcolor\" action=\"default\">#EDD54C</property>"
      "     <property name=\"viewgroup\" action=\"default\">1</property>"
      "    </view>"
      "   </item>"
      "  </layout>"
      " </item>"
      " <item>"
      "  <view class=\"vtkMRMLSliceNode\" singletontag=\"Axial\">"
      "   <property name=\"orientation\" action=\"default\">Axial</property>"
      "   <property name=\"viewlabel\" action=\"default\">A</property>"
      "   <property name=\"viewcolor\" action=\"default\">#6EB04B</property>"
      "   <property name=\"viewgroup\" action=\"default\">1</property>"
      "  </view>"
      " </item>"
      "</layout>")
    layoutManager = slicer.app.layoutManager()
    layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(custom_layouts["NavigatorAndTallAxial"], customLayout)
    #layoutManager.setLayout(custom_layouts["NavigatorAnd2DCompare"])
    # following copied per code on slicer discourse at:
    # https://discourse.slicer.org/t/slicer-crashes-when-adding-2-custom-layouts-in-startup-script/9071
    ## Add button to layout selector toolbar for this custom layout
    viewToolBar = slicer.util.mainWindow().findChild('QToolBar', 'ViewToolBar')
    layoutMenu = viewToolBar.widgetForAction(viewToolBar.actions()[0]).menu()
    layoutSwitchActionParent = layoutMenu  # use `layoutMenu` to add inside layout list, use `viewToolBar` to add next the standard layout list
    layoutSwitchAction = layoutSwitchActionParent.addAction("Navigator and coronal panel beside Axial view")
    layoutSwitchAction.setIcon(qt.QIcon(':Icons/Go.png'))
    layoutSwitchAction.setToolTip('2D Compare view')
    layoutSwitchAction.connect('triggered()', lambda layoutId = custom_layouts["NavigatorAndTallAxial"]: slicer.app.layoutManager().setLayout(layoutId))

def setNavigatorAndTallAxial():
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout(custom_layouts["NavigatorAndTallAxial"])
