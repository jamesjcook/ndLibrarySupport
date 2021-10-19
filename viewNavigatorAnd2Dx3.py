## Layout specifications for ndLibraryViewer
## Based on code originally written by Alex Sheu
## Modified by Austin Kao

## To load a new transform, update code in AtlasController.py
if "custom_layouts" not in locals():
    custom_layouts=dict()

## Function that creates the NavigatorAnd2Dx3 layout and sets it
def loadNavigatorAnd2Dx3():
    custom_layouts["NavigatorAnd2Dx3"]=687
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
      "    <view class=\"vtkMRMLSliceNode\" singletontag=\"Compare3\">"
      "     <property name=\"orientation\" action=\"default\">Coronal</property>"
      "     <property name=\"viewlabel\" action=\"default\">C3</property>"
      "     <property name=\"viewcolor\" action=\"default\">#EDD54C</property>"
      "     <property name=\"viewgroup\" action=\"default\">1</property>"
      "    </view>"
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
    layoutManager = slicer.app.layoutManager()
    layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(custom_layouts["NavigatorAnd2Dx3"], customLayout)
    #layoutManager.setLayout(custom_layouts["NavigatorAnd2Dx3"])
    # following copied per code on slicer discourse at:
    # https://discourse.slicer.org/t/slicer-crashes-when-adding-2-custom-layouts-in-startup-script/9071
    ## Add button to layout selector toolbar for this custom layout
    viewToolBar = slicer.util.mainWindow().findChild('QToolBar', 'ViewToolBar')
    layoutMenu = viewToolBar.widgetForAction(viewToolBar.actions()[0]).menu()
    layoutSwitchActionParent = layoutMenu  # use `layoutMenu` to add inside layout list, use `viewToolBar` to add next the standard layout list
    layoutSwitchAction = layoutSwitchActionParent.addAction("Navigator with 3x 2D compare views")
    layoutSwitchAction.setIcon(qt.QIcon(':Icons/Go.png'))
    layoutSwitchAction.setToolTip('2D Compare view x3')
    layoutSwitchAction.connect('triggered()', lambda layoutId = custom_layouts["NavigatorAnd2Dx3"]: slicer.app.layoutManager().setLayout(layoutId))

def setNavigatorAnd2Dx3():
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout(custom_layouts["NavigatorAnd2Dx3"])
