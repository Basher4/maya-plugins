import maya.api.OpenMaya as om
import maya.cmds as cmds


def maya_useNewAPI():
    pass


def initializePlugin(plugin: om.MObject):
    vendor = "Basher4"
    version = "1.0.0"
    om.MFnPlugin(plugin, vendor, version)
    om.MGlobal.displayInfo("Plugin loaded")


def uninitializePlugin(plugin: om.MObject):
    # Nothing was registered in the initialized method so this can be empty.
    om.MGlobal.displayInfo("Plugin unloaded")


if __name__ == "__main__":
    plugin_name = "template.py"
    cmds.evalDeferred(
        f"if cmds.pluginInfo('{plugin_name}', q=True, loaded=True): cmds.unloadPlugin('{plugin_name}')")
    cmds.evalDeferred(
        f"if not cmds.pluginInfo('{plugin_name}', q=True, loaded=True): cmds.loadPlugin('{plugin_name}')")
