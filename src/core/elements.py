from ..device.lasercommandconstants import COMMAND_MOVE
from ..svgelements import Color, SVGImage, Path, Polygon, Move, Close, Line, QuadraticBezier, CubicBezier, Arc

from ..kernel import Modifier
from .cutcode import CutCode, LaserSettings, LineCut, QuadCut, CubicCut, RasterCut


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
            operation="Engrave", color="blue", speed=20.0, passes_custom=True, passes=1,
        )
        self.cut = CutCode()
        self.cut_settings = LaserSettings(
            operation="Cut", color="red", speed=10.0, passes_custom=True, passes=1,
        )
        self.raster = CutCode()
        self.raster_settings = LaserSettings(
            operation="Raster", color="black", speed=100.0, passes_custom=True, passes=1,
        )
        self.gcode = CutCode()
        self.gcode_settings = LaserSettings(
            operation="GCode", color="black", speed=140.0, passes_custom=True, passes=1,
        )

    def engrave_cutcode(self, objects):
        c = self.engrave
        settings = self.engrave_settings
        self._vector_cutcode(c, settings, objects)

    def cut_cutcode(self, objects):
        c = self.cut
        settings = self.cut_settings
        self._vector_cutcode(c, settings, objects)

    def gcode_cutcode(self, objects):
        c = self.gcode
        settings = self.gcode_settings
        self._vector_cutcode(c, settings, objects)

    def image_cutcode(self, objects):
        c = self.raster
        settings = self.raster_settings
        for object_image in objects:
            settings = LaserSettings(settings)
            try:
                settings.raster_step = int(object_image.values["raster_step"])
            except KeyError:
                settings.raster_step = 1
            direction = settings.raster_direction
            settings.crosshatch = False
            if direction == 4:
                cross_settings = LaserSettings(settings)
                cross_settings.crosshatch = True
                c.append(RasterCut(object_image, settings))
                c.append(RasterCut(object_image, cross_settings))
            else:
                c.append(RasterCut(object_image, settings))
        return c

    def raster_cutcode(self, objects):
        c = self.raster
        settings = self.raster_settings
        direction = settings.raster_direction
        settings.crosshatch = False
        if direction == 4:
            cross_settings = LaserSettings(settings)
            cross_settings.crosshatch = True
            for object_image in objects:
                if not isinstance(object_image, SVGImage):
                    continue
                c.append(RasterCut(object_image, settings))
                c.append(RasterCut(object_image, cross_settings))
        else:
            for object_image in objects:
                if not isinstance(object_image, SVGImage):
                    continue
                c.append(RasterCut(object_image, settings))
        return c

    def _vector_cutcode(self, cutcode: CutCode, settings: LaserSettings, objects: list):
        for object_path in objects:
            if isinstance(object_path, SVGImage):
                box = object_path.bbox()
                plot = Path(
                        Polygon(
                            (box[0], box[1]),
                            (box[0], box[3]),
                            (box[2], box[3]),
                            (box[2], box[1]),
                            )
                        )
            else:
                # Is a shape or path.
                if not isinstance(object_path, Path):
                    plot = abs(Path(object_path))
                else:
                    plot = abs(object_path)
            for seg in plot:
                if isinstance(seg, Move):
                    pass  # Move operations are ignored.
                elif isinstance(seg, Close):
                    cutcode.append(LineCut(seg.start, seg.end, settings=settings))
                elif isinstance(seg, Line):
                    cutcode.append(LineCut(seg.start, seg.end, settings=settings))
                elif isinstance(seg, QuadraticBezier):
                    cutcode.append(
                        QuadCut(seg.start, seg.control, seg.end, settings=settings)
                    )
                elif isinstance(seg, CubicBezier):
                    cutcode.append(
                        CubicCut(
                            seg.start,
                            seg.control1,
                            seg.control2,
                            seg.end,
                            settings=settings,
                        )
                    )
                elif isinstance(seg, Arc):
                    for s in seg.as_cubic_curves():
                        cutcode.append(
                            CubicCut(
                                s.start,
                                s.control1,
                                s.control2,
                                s.end,
                                settings=settings,
                            )
                        )
        return cutcode

    def attach(self, *a, **kwargs):
        context = self.context
        context.elements = self
        context.save = self.save
        context.save_types = self.save_types
        context.load = self.load
        context.load_types = self.load_types
        context.engrave = self.engrave
        context.cut = self.cut
        context.raster = self.raster
        context.engrave_settings = self.engrave_settings
        context.cut_settings = self.cut_settings
        context.raster_settings = self.raster_settings

        @self.context.console_command(
            "cut",
            help="starts an op chain",
            output_type="op"
        )
        def op_init(command, **kwargs):
            return "op", ("cut", self.cut, self.cut_settings)

        @self.context.console_command(
            "engrave",
            help="starts an op chain",
            output_type="op"
        )
        def op_init(command, **kwargs):
            return "op", ("engrave", self.engrave, self.engrave_settings)

        @self.context.console_command(
            "raster",
            help="starts an op chain",
            input_type=(None, 'image'),
            output_type="op"
        )
        def op_init(command, data_type, data, **kwargs):
            if data_type == 'image':
                self.raster_cutcode(data)
            return "op", ("raster", self.raster, self.raster_settings)

        @self.context.console_argument(
            "setting",
            type=str,
            help="setting",
        )
        @self.context.console_argument(
            "value",
            type=str,
            help="value",
        )
        @self.context.console_command(
            "set",
            help="set <setting> <value>",
            output_type="op",
            input_type="op"
        )
        def op_set(channel, _, data=None, setting=None, value=None, **kwargs):
            name, cutcode, op_set = data
            if setting is None:
                channel(_("%s Settings:" % name))
                for setv in dir(op_set):
                    if setv.startswith('_') or setv.startswith('implicit'):
                        continue
                    v = getattr(op_set, setv)
                    if not isinstance(v, (int, float, str, complex, Color)):
                        continue
                    channel("%s=%s" % (setv, str(v)))
                return
            try:
                v = getattr(op_set, setting)
            except AttributeError:
                return
            if v is None:
                return
            t = type(v)
            setattr(op_set, setting, t(value))
            channel(_("%s: '%s' from %s to %s.") % (name, setting, str(v), value))
            self.context.signal("op_setting_update", name)
            return "op", data

        @self.context.console_command(
            "execute",
            help="<op> execute",
            input_type="op",
            output_type="op",
        )
        def op_execute(channel, _, data=None, **kwargs):
            if data is None:
                channel(_("Nothing to Execute"))
                return
            name, cutcode, op_set = data
            if not len(cutcode):
                self.context.signal("statusbar", _("No %s data to send") % name, 2)
                return

            for i in range(op_set.implicit_passes):
                cutcode.set_offset(context.offset_x, context.offset_y)
                self.context.get_context('/').spooler.job(cutcode)
            self.context.get_context('/').spooler.job(self.context.registered["plan/origin"])
            return "op", data

        @self.context.console_command(
            "list",
            help="<op> list",
            input_type="op",
            output_type="op",
        )
        def op_list(channel, _, data=None, **kwargs):
            if data is None:
                channel(_("Nothing to list"))
                return
            name, cutcode, op_set = data
            channel(_("%s Objects:" % name))
            for code in cutcode:
                channel(str(code))
            return "op", data

        @self.context.console_command(
            "clear",
            help="<op> clear",
            input_type="op",
            output_type="op",
        )
        def op_clear(channel, _, data=None, **kwargs):
            name, cutcode, op_set = data
            cutcode.clear()
            return "op", data

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
