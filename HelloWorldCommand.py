import maya.api.OpenMaya as om
import maya.cmds as cmds


class HelloWorldCmd(om.MPxCommand):
    COMMAND_NAME = "HelloWorld"

    def __init__(self):
        super().__init__()

    def doIt(self, args):
        print("Hello World!")

    @classmethod
    def creator(cls):
        return HelloWorldCmd()


def maya_useNewAPI():
    pass


def initializePlugin(plugin: om.MObject):
    vendor = "Basher4"
    version = "1.0.0"
    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(
            HelloWorldCmd.COMMAND_NAME, HelloWorldCmd.creator)
        print("Plugin loaded successfully")
    except Exception as ex:
        om.MGlobal.displayError(
            f"Failed to register command {HelloWorldCmd.COMMAND_NAME} with error {ex}")


def uninitializePlugin(plugin: om.MObject):
    plugin_fn = om.MFnPlugin(plugin)

    try:
        plugin_fn.deregisterCommand(HelloWorldCmd.COMMAND_NAME)
        print("Plugin unloaded successfully")
    except Exception as ex:
        om.MGlobal.displayError(
            f"Failed to deregister command {HelloWorldCmd.COMMAND_NAME} with error {ex}")


if __name__ == "__main__":
    plugin_name = f"HelloWorldCommand.py"

    cmds.evalDeferred(
        f"if cmds.pluginInfo('{plugin_name}', q=True, loaded=True): cmds.unloadPlugin('{plugin_name}')")
    cmds.evalDeferred(
        f"if not cmds.pluginInfo('{plugin_name}', q=True, loaded=True): cmds.loadPlugin('{plugin_name}')")
