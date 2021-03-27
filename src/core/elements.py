from svgelements import Color, SVGImage, SVGText

from ..kernel import Modifier
from .cutcode import CutCode, LaserSettings


def plugin(kernel, lifecycle=None):
    if lifecycle == "register":
        kernel.register("modifier/ElementCore", ElementCore)
    elif lifecycle == "boot":
        kernel_root = kernel.get_context("/")
        kernel_root.activate("modifier/ElementCore")


class ElementCore(Modifier):
    def __init__(self, context, name=None, channel=None, *args, **kwargs):
        Modifier.__init__(self, context, name, channel)
        self.engrave = CutCode()
        self.engrave_settings = LaserSettings(
            operation="Engrave", color="blue", speed=35.0
        )
        self.cut = CutCode()
        self.cut_settings = LaserSettings(
            operation="Cut", color="red", speed=10.0
        )
        self.raster = CutCode()
        self.raster_settings = LaserSettings(
            operation="Raster", color="black", speed=140.0
        )

    def attach(self, *a, **kwargs):
        context = self.context
        context.elements = self
        context.save = self.save
        context.save_types = self.save_types
        context.load = self.load
        context.load_types = self.load_types

        @self.context.console_argument(
            "op",
            type=str,
            help="operation to execute",
        )
        @self.context.console_command(
            "execute",
            help="execute <operation>",
        )
        def plan(command, channel, _, op=None, args=tuple(), **kwargs):
            if op == "engrave":
                self.context.get_context('/').spooler.job(self.engrave)
            elif op == "cut":
                self.context.get_context('/').spooler.job(self.cut)
            elif op == "raster":
                self.context.get_context('/').spooler.job(self.raster)

        @self.context.console_argument(
            "setting",
            type=str,
            help="setting",
        )
        @self.context.console_argument(
            "value",
            type=str,
            help="setting",
        )
        @self.context.console_command(
            ("cut", "engrave", "raster"),
            help="operation<?> <setting> <value>",
        )
        def plan(command, channel, _, setting, value=None, args=tuple(), **kwargs):

            if command == "engrave":
                s = self.engrave_settings
            elif command == "cut":
                s = self.cut_settings
            elif command == "raster":
                s = self.raster_settings
            else:
                raise ValueError
            v = getattr(s, value)
            if v is None:
                return
            t = type(v)
            setattr(s, value, t(setting))
            channel(_("Set %s setting %s from %s to %s.") % (command, setting, str(v), setting))

    def detach(self, *a, **kwargs):
        context = self.context
        settings = context.derive("settings")
        settings.clear_persistent()

        op_set = settings.derive('engrave')
        for key in dir(self.engrave_settings):
            if key.startswith("_") or key.startswith("implicit"):
                continue
            value = getattr(self.engrave_settings, key)
            if value is None:
                continue
            if isinstance(value, Color):
                value = value.value
            op_set.write_persistent(key, value)

        op_set = settings.derive('cut')
        for key in dir(self.cut_settings):
            if key.startswith("_") or key.startswith("implicit"):
                continue
            value = getattr(self.cut_settings, key)
            if value is None:
                continue
            if isinstance(value, Color):
                value = value.value
            op_set.write_persistent(key, value)

        op_set = settings.derive('raster')
        for key in dir(self.raster_settings):
            if key.startswith("_") or key.startswith("implicit"):
                continue
            value = getattr(self.raster_settings, key)
            if value is None:
                continue
            if isinstance(value, Color):
                value = value.value
            op_set.write_persistent(key, value)

        settings.close_subpaths()

    def boot(self, *a, **kwargs):
        settings = self.context.derive("settings")
        op_set = settings.derive('engrave')
        op_set.load_persistent_object(self.engrave_settings)
        op_set = settings.derive('cut')
        op_set.load_persistent_object(self.cut_settings)
        op_set = settings.derive('raster')
        op_set.load_persistent_object(self.raster_settings)

    def load(self, pathname, **kwargs):
        kernel = self.context._kernel
        for loader_name in kernel.match("load"):
            loader = kernel.registered[loader_name]
            for description, extensions, mimetype in loader.load_types():
                if str(pathname).lower().endswith(extensions):
                    try:
                        results = loader.load(self.context, self, pathname, **kwargs)
                    except FileNotFoundError:
                        return False
                    if not results:
                        continue
                    return True

    def load_types(self, all=True):
        kernel = self.context._kernel
        filetypes = []
        if all:
            filetypes.append("All valid types")
            exts = []
            for loader_name in kernel.match("load"):
                loader = kernel.registered[loader_name]
                for description, extensions, mimetype in loader.load_types():
                    for ext in extensions:
                        exts.append("*.%s" % ext)
            filetypes.append(";".join(exts))
        for loader_name in kernel.match("load"):
            loader = kernel.registered[loader_name]
            for description, extensions, mimetype in loader.load_types():
                exts = []
                for ext in extensions:
                    exts.append("*.%s" % ext)
                filetypes.append("%s (%s)" % (description, extensions[0]))
                filetypes.append(";".join(exts))
        return "|".join(filetypes)

    def save(self, pathname):
        kernel = self.context._kernel
        for save_name in kernel.match("save"):
            saver = kernel.registered[save_name]
            for description, extension, mimetype in saver.save_types():
                if pathname.lower().endswith(extension):
                    saver.save(self.context, pathname, "default")
                    return True
        return False

    def save_types(self):
        kernel = self.context._kernel
        filetypes = []
        for save_name in kernel.match("save"):
            saver = kernel.registered[save_name]
            for description, extension, mimetype in saver.save_types():
                filetypes.append("%s (%s)" % (description, extension))
                filetypes.append("*.%s" % (extension))
        return "|".join(filetypes)
