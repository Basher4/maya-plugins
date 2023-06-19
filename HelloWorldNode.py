import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds


class HelloWorldNode(omui.MPxLocatorNode):
    TYPE_NAME = "HelloWorld"
    TYPE_ID = om.MTypeId(0x7F7F7)  # This is a dev value.
    DRAW_CLASSIFICATION = "drawdb/geometry/helloworld"
    DRAW_REGISTRANT_ID = "HelloWorldNode"

    def __init__(self):
        super().__init__()

    @classmethod
    def creator(cls):
        return HelloWorldNode()

    @classmethod
    def initialize(cls):
        pass


class HelloWorldDrawOverride(omr.MPxDrawOverride):
    NAME = "HelloWorldDrawOverride"

    def __init__(self, obj):
        super().__init__(obj, None, False)

    def prepareForDraw(self, 
                       bj_path: om.MDagPath,
                       camera_path: om.MDagPath,
                       frame_ctx: omr.MFrameContext,
                       old_data: om.MUserData):
        pass

    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self,
                       obj_path: om.MDagPath,
                       draw_manager: omr.MUIDrawManager,
                       frame_ctx: omr.MFrameContext,
                       data: om.MUserData):
        draw_manager.beginDrawable()
        draw_manager.text2d(om.MPoint(100, 100), "Hello World from my plugin")
        draw_manager.endDrawable()

    @classmethod
    def creator(cls, obj: om.MObject):
        return HelloWorldDrawOverride(obj)


def maya_useNewAPI():
    pass


def initializePlugin(plugin: om.MObject):
    vendor = "Basher4"
    version = "1.0.0"
    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerNode(HelloWorldNode.TYPE_NAME,
                               HelloWorldNode.TYPE_ID,
                               HelloWorldNode.creator,
                               HelloWorldNode.initialize,
                               om.MPxNode.kLocatorNode,
                               HelloWorldNode.DRAW_CLASSIFICATION)
        print("Plugin loaded successfully")
    except Exception as ex:
        om.MGlobal.displayError(
            f"Failed to register node {HelloWorldNode.TYPE_NAME} with error {ex}")

    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(HelloWorldNode.DRAW_CLASSIFICATION,
                                                      HelloWorldNode.DRAW_REGISTRANT_ID,
                                                      HelloWorldDrawOverride.creator)
    except Exception as ex:
        om.MGlobal.displayError(
            f"Failed to register draw override {HelloWorldDrawOverride.NAME} with error {ex}")

def uninitializePlugin(plugin: om.MObject):
    plugin_fn = om.MFnPlugin(plugin)

    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(HelloWorldNode.DRAW_CLASSIFICATION,
                                                        HelloWorldNode.DRAW_REGISTRANT_ID)
    except Exception as ex:
        om.MGlobal.displayError(
            f"Failed to deregister draw override {HelloWorldDrawOverride.NAME} with error {ex}")

    try:
        plugin_fn.deregisterNode(HelloWorldNode.TYPE_ID)
        print("Plugin unloaded successfully")
    except Exception as ex:
        om.MGlobal.displayError(
            f"Failed to deregister node {HelloWorldNode.TYPE_NAME} with error {ex}")


def loadPlugin(plugin_name):
    if not cmds.pluginInfo(plugin_name, q=True, loaded=True):
        cmds.loadPlugin(plugin_name)
    cmds.createNode(HelloWorldNode.TYPE_NAME)


def unloadPlugin(plugin_name):
    if cmds.pluginInfo(plugin_name, q=True, loaded=True):
        # cmds.flushUndo()  # Even when node is deleted it is on the undo stack.
        # Not needed since we create a new scene.
        cmds.unloadPlugin(plugin_name)


if __name__ == "__main__":
    plugin_name = "HelloWorldNode.py"

    cmds.file(new=True, force=True)
    cmds.evalDeferred(f"unloadPlugin('{plugin_name}')")
    cmds.evalDeferred(f"loadPlugin('{plugin_name}')")
