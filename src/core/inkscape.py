import os.path
from sys import platform
from subprocess import run, PIPE


def plugin(kernel, lifecycle):
    if lifecycle == "register":
        @kernel.console_argument('filename', type=str, help="filename of svg to be simplified")
        @kernel.console_command('simplify', help="simplify path", input_type="inkscape", output_type="inkscape")
        def simplify(channel, _, filename, data=None, **kwargs):
            if filename is None:
                channel(_("filename not specified"))

            if not os.path.exists(filename):
                channel(_("file is not found."))
                return
            channel(_("Making plain_svg with Inkscape."))
            c = run([data,
                    '--export-plain-svg=temp.svg',
                    filename
                 ], stdout=PIPE)
            channel(c.stdout)
            return "inkscape", data

        @kernel.console_argument('filename', type=str, help="filename of svg to text-to-path")
        @kernel.console_command('text2path', help="text to path", input_type="inkscape", output_type="inkscape")
        def text2path(channel, _, filename, data=None, **kwargs):
            if filename is None:
                channel(_("filename not specified"))

            if not os.path.exists(filename):
                channel(_("file is not found."))
                return
            channel(_("Making plain_svg with Inkscape."))
            c = run([data,"--export-text-to-path", "--export-filename=temp.svg", filename], stdout=PIPE)
            channel(c.stdout)
            return "inkscape", data

        @kernel.console_option('dpi', "d", type=int, help="dpi to use", default=1000)
        @kernel.console_option('step', "s", type=int, help="step to use")
        @kernel.console_argument('filename', type=str, help="filename of svg to be simplified")
        @kernel.console_command('makepng', help="make png", input_type="inkscape", output_type="inkscape")
        def png(channel, _, filename, dpi=1000, step=None, data=None, **kwargs):
            if step is not None and step > 0:
                dpi = 1000 / step
            if filename is None:
                channel(_("filename not specified"))

            if not os.path.exists(filename):
                channel(_("file is not found."))
                return
            channel(_("Making PNG with Inkscape."))
            c = run([data,
                    '--export-type=png',
                    '--export-filename=temp.png',
                    '--export-dpi=%d' % dpi,
                    filename
                 ], stdout=PIPE)
            channel(c.stdout)
            return "inkscape", data

        @kernel.console_command('version', help="determine inkscape version", input_type="inkscape", output_type="inkscape")
        def version(channel, _, data, **kwargs):
            if not os.path.exists(data):
                channel(_("Inkscape not found."))
                return
            c = run([data, "-V"], stdout=PIPE)
            channel(c.stdout)
            return "inkscape", data

        @kernel.console_command("locate", help="find inkscape", input_type="inkscape", output_type="inkscape")
        def locate(channel, _, data, **kwargs):
            if "win" in platform:
                inkscape = [
                    "C:/Program Files/Inkscape/inkscape.exe",
                    "C:/Program Files (x86)/Inkscape/inkscape.exe",
                    "C:/Program Files/Inkscape/bin/inkscape.exe",
                    "C:/Program Files (x86)/Inkscape/bin/inkscape.exe",
                ]
            elif "linux" in platform:
                inkscape = [
                    "/usr/local/bin/inkscape",
                    "/usr/bin/inkscape",
                ]
            elif "darwin" in platform:
                inkscape = [
                    "/Applications/Inkscape.app/Contents/MacOS/Inkscape"
                    "/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
                ]
            else:
                channel(_("Platform inkscape locations unknown."))
                return
            channel(_("----------"))
            channel(_("Finding Inkscape"))
            match = None
            for ink in inkscape:
                if os.path.exists(ink):
                    match = ink
                    result = _("Success")
                else:
                    result = _("Fail")
                channel("Searching: %s -- Result: %s" % (ink, result))
            channel(_("----------"))
            if match is None:
                return
            root_context = kernel.get_context('/')
            root_context.setting(str, "inkscape_path", "inkscape.exe")
            root_context.inkscape_path = match
            return "inkscape", match

        @kernel.console_command("inkscape", help="perform a special inkscape function", output_type="inkscape")
        def inkscape(channel, _, **kwargs):
            root_context = kernel.get_context('/')
            root_context.setting(str, "inkscape_path", "inkscape.exe")
            return "inkscape", root_context.inkscape_path
