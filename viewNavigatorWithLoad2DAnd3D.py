## Layout specifications for ndLibraryViewer
## Based on code originally written by Alex Sheu
## Modified by Austin Kao

if "custom_layouts" not in locals():
    custom_layouts=dict()

## Function that creates the TwoDComparisonView layout and sets it
def loadNavigatorWithLoad2DAnd3D():
    custom_layouts["NavigatorWithLoad2DAnd3D"]=786
    customLayout = ("<layout type=\"vertical\">"
      " <item>"
      "  <layout type=\"horizontal\">"
      "   <item>"
      "    	<view class=\"vtkMRMLSliceNode\" singletontag=\"Navigator\">"
      "      <property name=\"orientation\" action=\"default\">Sagittal</property>"
      "      <property name=\"viewlabel\" action=\"default\">Nav</property>"
      "      <property name=\"viewcolor\" action=\"default\">#6EB04B</property>"
      "     <property name=\"viewgroup\" action=\"default\">1</property>"
      "   	</view>"
      "   </item>"
      "   <item>"
      "    	<view class=\"vtkMRMLSliceNode\" singletontag=\"Load\">"
      "      <property name=\"orientation\" action=\"default\">Axial</property>"
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
      "    	<view class=\"vtkMRMLViewNode\" singletontag=\"1\" verticalStretch=\"0\" "
      "      Background=\"black\" >"
      "      <property name=\"viewlabel\" action=\"default\">Nav</property>"
      "   	</view>"
      "   </item>"
      "  </layout>"
      " </item>"
      "</layout>")
    layoutManager = slicer.app.layoutManager()
    layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(custom_layouts["NavigatorWithLoad2DAnd3D"], customLayout)
    # layoutManager.setLayout(custom_layouts["NavigatorWithLoad2DAnd3D"])
    # following copied per code on slicer discourse at:
    # https://discourse.slicer.org/t/slicer-crashes-when-adding-2-custom-layouts-in-startup-script/9071
    ## Add button to layout selector toolbar for this custom layout
    viewToolBar = slicer.util.mainWindow().findChild('QToolBar', 'ViewToolBar')
    layoutMenu = viewToolBar.widgetForAction(viewToolBar.actions()[0]).menu()
    layoutSwitchActionParent = layoutMenu  # use `layoutMenu` to add inside layout list, use `viewToolBar` to add next the standard layout list
    layoutSwitchAction = layoutSwitchActionParent.addAction("Navigator and external Load panel over 2D + 3D views")
    layoutSwitchAction.setIcon(qt.QIcon(':Icons/Go.png'))
    layoutSwitchAction.setToolTip('2D Compare view')
    layoutSwitchAction.connect('triggered()', lambda layoutId = custom_layouts["NavigatorWithLoad2DAnd3D"]: slicer.app.layoutManager().setLayout(layoutId))
    
def setNavigatorWithLoad2DAnd3D():
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout(custom_layouts["NavigatorWithLoad2DAnd3D"])

