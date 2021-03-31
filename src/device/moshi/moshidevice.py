from ...kernel import STATE_UNKNOWN, Modifier
from .moshicontroller import MoshiController
from .moshiinterpreter import MoshiInterpreter


def plugin(kernel, lifecycle=None):
    if lifecycle == "register":
        kernel.register("device/Moshi", MoshiDevice)


"""
MoshiboardDevice is the backend for Moshiboard devices.

The device is primary composed of three main modules.

* A generic spooler to take in lasercode.
* An interpreter to convert lasercode into moshi-programs.
* A controller to send the data to the hardware using moshi protocols.

"""


class MoshiDevice(Modifier):
    def __init__(self, context, name=None, channel=None, *args, **kwargs):
        Modifier.__init__(self, context, name, channel)
        context.device_name = "Moshi"
        context.device_location = "USB"
        self.state = STATE_UNKNOWN
        self.dx = 0
        self.dy = 0
        self.bed_dim = self.context.get_context("bed")
        self.bed_dim.setting(float, "bed_width", 325.0)
        self.bed_dim.setting(float, "bed_height", 220.0)

    def __repr__(self):
        return "MoshiDevice()"

    @staticmethod
    def sub_register(device):
        device.register("modifier/MoshiInterpreter", MoshiInterpreter)
        device.register("module/MoshiController", MoshiController)

    def attach(self, *a, **kwargs):
        context = self.context
        context.setting(str, "device_name", "Moshi")
        context._quit = False
        context.setting(int, "usb_index", -1)
        context.setting(int, "usb_bus", -1)
        context.setting(int, "usb_address", -1)
        context.setting(int, "usb_serial", -1)
        context.setting(int, "usb_version", -1)
        context.setting(bool, "mock", False)
        context.setting(int, "packet_count", 0)
        context.setting(int, "rejected_count", 0)
        context.setting(bool, "autolock", True)
        context.setting(str, "board", "M2")
        context.setting(bool, "fix_speeds", False)

        self.dx = 0
        self.dy = 0

        context.open_as("module/MoshiController", "pipe")
        context.activate("modifier/MoshiInterpreter", context)
        context.activate("modifier/Spooler")

        context.listen("interpreter;mode", self.on_mode_change)
        context.signal("bed_size", (self.bed_dim.bed_width, self.bed_dim.bed_height))

    def detach(self, *args, **kwargs):
        self.context.unlisten("interpreter;mode", self.on_mode_change)

    def on_mode_change(self, *args):
        self.dx = 0
        self.dy = 0
