import argparse
import sys

from .kernel import Kernel

try:
    from math import tau
except ImportError:
    from math import pi

    tau = pi * 2


"""
From April Fools Laser Studios: Silence.

Silence is a very convoluted and functional joke. I cloned all the K40 Whisperer GUI and patched it into MeerK40t code.
To get it to work and have a bunch of fancy features. Ripping off the interface word for word requires that this be
licensed the way Whisperer is licensed.

"""

SILENCE_VERSION = "0.0.1"


def pair(value):
    rv = value.split("=")
    if len(rv) != 2:
        raise argparse.ArgumentParser()
    return rv


parser = argparse.ArgumentParser()
parser.add_argument("-V", "--version", action="store_true", help="MeerK40t version")
parser.add_argument("input", nargs="?", type=argparse.FileType("r"), help="input file")
parser.add_argument("-z", "--no_gui", action="store_true", help="run without gui")
parser.add_argument("-b", "--batch", type=argparse.FileType("r"), help="console batch file")
parser.add_argument("-c", "--console", action="store_true", help="start as console")
parser.add_argument(
    "-q", "--quit", action="store_true", help="quit on spooler complete"
)
parser.add_argument("-a", "--auto", action="store_true", help="start running laser")
parser.add_argument(
    "-s",
    "--set",
    action="append",
    nargs="?",
    type=pair,
    metavar="key=value",
    help="set a device variable",
)
parser.add_argument("-P", "--profile", type=int, default=None, help="Specify a settings profile index")


def run():
    argv = sys.argv[1:]
    # argv = "-P 0".split()
    args = parser.parse_args(argv)

    if args.version:
        print("Silence %s" % SILENCE_VERSION)
        return

    if args.profile is not None:
        path = 'profile%d' % args.profile
    else:
        path = ''
    kernel = Kernel("Silence", SILENCE_VERSION, "Silence", path)

    """
    These are frozen bootstraps. They are not dynamically found by entry points they are the configured accepted
    hardcoded addons and plugins permitted by MeerK40t in a compiled bundle.
    """
    try:
        from . import kernelserver

        kernel.add_plugin(kernelserver.plugin)
    except ImportError:
        pass

    try:
        from .kernel_root import basedevice

        kernel.add_plugin(basedevice.plugin)
    except ImportError:
        pass

    try:
        from .core import elements

        kernel.add_plugin(elements.plugin)
    except ImportError:
        pass

    try:
        from .core import bindalias

        kernel.add_plugin(bindalias.plugin)
    except ImportError:
        pass

    try:
        from .core import cutplanner

        kernel.add_plugin(cutplanner.plugin)
    except ImportError:
        pass

    try:
        from .core import webhelp

        kernel.add_plugin(webhelp.plugin)
    except ImportError:
        pass

    try:
        from .kernel_root.lhystudios import lhystudiosdevice

        kernel.add_plugin(lhystudiosdevice.plugin)
    except ImportError:
        pass

    try:
        from .kernel_root.moshi import moshidevice

        kernel.add_plugin(moshidevice.plugin)
    except ImportError:
        pass

    try:
        from .device.ruida import ruidadevice

        kernel.add_plugin(ruidadevice.plugin)
    except ImportError:
        pass

    try:
        from .core import svg_io

        kernel.add_plugin(svg_io.plugin)
    except ImportError:
        pass

    try:
        from .dxf import dxf_io

        kernel.add_plugin(dxf_io.plugin)
    except ImportError:
        # This module cannot be loaded. ezdxf missing.
        pass

    if not args.no_gui:
        # Must permit this plugin in the gui.
        try:
            from .gui import silence

            kernel.add_plugin(silence.plugin)
        except ImportError:
            # This module cannot be loaded. wxPython missing.
            pass

    if not getattr(sys, "frozen", False):
        """
        These are dynamic plugins. They are dynamically found by entry points.
        """
        import pkg_resources

        for entry_point in pkg_resources.iter_entry_points("silence.plugins"):
            try:
                plugin = entry_point.load()
                kernel.add_plugin(plugin)
            except pkg_resources.DistributionNotFound:
                pass

    kernel_root = kernel.get_context("/")
    kernel_root.device_version = SILENCE_VERSION
    kernel_root.device_name = "Silence"

    kernel.bootstrap("register")
    kernel.bootstrap("configure")
    kernel.boot()
    kernel_root.channel("console").watch(print)


    if args.input is not None:
        import os

        kernel_root.load(os.path.realpath(args.input.name))
        elements = kernel_root.elements
        elements.classify(list(elements.elems()))

    if args.set is not None:
        # Set the variables requested here.
        for v in args.set:
            attr = v[0]
            value = v[1]
            if hasattr(kernel_root, attr):
                v = getattr(kernel_root, attr)
                if isinstance(v, bool):
                    setattr(kernel_root, attr, bool(value))
                elif isinstance(v, int):
                    setattr(kernel_root, attr, int(value))
                elif isinstance(v, float):
                    setattr(kernel_root, attr, float(value))
                elif isinstance(v, str):
                    setattr(kernel_root, attr, str(value))

    if args.batch:
        # kernel_root.channel("console").watch(print)
        with args.batch as batch:
            for line in batch:
                kernel_root.console(line.strip() + "\n")
        kernel_root.channel("console").unwatch(print)

    kernel.bootstrap("ready")

    if args.console:
        def thread_text_console():
            kernel_root.channel("console").watch(print)
            while True:
                console_command = input(">")
                if kernel_root._kernel.lifecycle == "shutdown":
                    return
                kernel_root.console(console_command + "\n")
                if console_command in ("quit", "shutdown"):
                    break
            kernel_root.channel("console").unwatch(print)
        if args.no_gui:
            thread_text_console()
        else:
            kernel.threaded(thread_text_console, thread_name="text_console")
    kernel.bootstrap("mainloop")
