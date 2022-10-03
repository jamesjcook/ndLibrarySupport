## Layout specifications for ndLibraryViewer
## Based on code originally written by Alex Sheu
## Modified by Austin Kao
import slicer
import qt

if "custom_layouts" not in locals():
    custom_layouts=dict()

## Function that creates the NavigatorWithLoadAnd2DCompare layout and sets it
def loadNavigatorWithLoadAnd2DCompare():
    custom_layouts["NavigatorWithLoadAnd2DCompare"]=586
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
    layoutManager.layoutLogic().GetLayoutNode().AddLayoutDescription(custom_layouts["NavigatorWithLoadAnd2DCompare"], customLayout)
    #layoutManager.setLayout(custom_layouts["NavigatorWithLoadAnd2DCompare"])
    # following copied per code on slicer discourse at:
    # https://discourse.slicer.org/t/slicer-crashes-when-adding-2-custom-layouts-in-startup-script/9071
    ## Add button to layout selector toolbar for this custom layout
    viewToolBar = slicer.util.mainWindow().findChild('QToolBar', 'ViewToolBar')
    layoutMenu = viewToolBar.widgetForAction(viewToolBar.actions()[0]).menu()
    layoutSwitchActionParent = layoutMenu  # use `layoutMenu` to add inside layout list, use `viewToolBar` to add next the standard layout list
    layoutSwitchAction = layoutSwitchActionParent.addAction("Navigator and external Load panel over 2D compare views")
    layoutSwitchAction.setIcon(qt.QIcon(':Icons/Go.png'))
    layoutSwitchAction.setToolTip('2D Compare view')
    layoutSwitchAction.connect('triggered()', lambda layoutId = custom_layouts["NavigatorWithLoadAnd2DCompare"]: slicer.app.layoutManager().setLayout(layoutId))

def setNavigatorWithLoadAnd2DCompare():
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout(custom_layouts["NavigatorWithLoadAnd2DCompare"])
