import os
import sys

import wx

from .laserrender import *
from src.gui.rasterwizard import RasterWizard
from src.gui.terminal import Terminal
from src.kernel import Module
from .egvsave import EgvSave
from .generalsettings import GeneralSettings
from .rastersettings import RasterSettings
from .rotarysettings import RotarySettings
from .silence import Silence
from .traceboundary import TraceBoundary
from .widget import (
    Scene,
)

MILS_IN_MM = 39.3701


def plugin(kernel, lifecycle):
    if lifecycle == "register":
        kernel.register("module/SilenceApp", SilenceApp)
    if lifecycle == "configure":
        kernel_root = kernel.get_context("/")
        kernel_root.open("module/SilenceApp")
    elif lifecycle == "mainloop":
        kernel_root = kernel.get_context("/")
        gui = kernel_root.open("module/SilenceApp")
        kernel_root("window open -p / Silence\n")
        gui.MainLoop()


_ = wx.GetTranslation
supported_languages = (
    ("en", u"English", wx.LANGUAGE_ENGLISH),
    ("it", u"italiano", wx.LANGUAGE_ITALIAN),
    ("fr", u"français", wx.LANGUAGE_FRENCH),
    ("de", u"Deutsch", wx.LANGUAGE_GERMAN),
    ("es", u"español", wx.LANGUAGE_SPANISH),
    ("zh", u"Chinese", wx.LANGUAGE_CHINESE),
)


class SilenceApp(wx.App, Module):
    def __init__(self, context, path):
        wx.App.__init__(self, 0)

        # theme = wx.SystemSettings().GetColour(wx.SYS_COLOUR_WINDOW)[0] < 127
        Module.__init__(self, context, path)
        self.locale = None
        context.setting(int, "draw_mode", 0xFF)
        self.Bind(wx.EVT_CLOSE, self.on_app_close)
        self.Bind(wx.EVT_QUERY_END_SESSION, self.on_app_close)  # MAC DOCK QUIT.
        self.Bind(wx.EVT_END_SESSION, self.on_app_close)
        self.Bind(wx.EVT_END_PROCESS, self.on_app_close)
        # This catches events when the app is asked to activate by some other process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def on_app_close(self, event):
        try:
            if self.context is not None:
                self.context.console("quit\n")
        except AttributeError:
            pass

    def OnInit(self):
        return True

    def BringWindowToFront(self):
        try:  # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass

    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()

    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""
        self.BringWindowToFront()

    def MacNewFile(self):
        try:
            if self.context is not None:
                self.context.console("clear_all\n")
        except AttributeError:
            pass

    def MacPrintFile(self, file_path):
        pass

    def MacOpenFile(self, filename):
        try:
            if self.context is not None:
                self.context.load(os.path.realpath(filename))
        except AttributeError:
            pass

    def MacOpenFiles(self, filenames):
        try:
            if self.context is not None:
                for filename in filenames:
                    self.context.load(os.path.realpath(filename))
        except AttributeError:
            pass

    @staticmethod
    def sub_register(kernel):
        kernel.register("module/Scene", Scene)
        kernel.register("window/Silence", Silence)
        kernel.register("window/GeneralSettings", GeneralSettings)
        kernel.register("window/RasterSettings", RasterSettings)
        kernel.register("window/RotarySettings", RotarySettings)
        kernel.register("window/EgvSave", EgvSave)
        kernel.register("window/TraceBoundary", TraceBoundary)
        kernel.register("window/Terminal", Terminal)
        kernel.register("window/RasterWizard", RasterWizard)

        context = kernel.get_context("/")

        @kernel.console_option(
            "path",
            "p",
            type=context.get_context,
            default=context.active,
            help="Context Path at which to open the window",
        )
        @kernel.console_argument("subcommand", type=str, help="open <window>")
        @kernel.console_argument(
            "window", type=str, help="window to apply subcommand to"
        )
        @kernel.console_command("window", help="Silence window information")
        def window(
            channel, _, subcommand=None, window=None, path=None, args=(), **kwargs
        ):
            """
            Opens a window or provides information. This command is restricted to use with the gui.
            This also allows use of a -p flag that sets the context path for this window to operate at. This should
            often be restricted to where the windows are typically opened since their function and settings usually
            depend on the context used. The default root path is "/". Eg. "window open -p / Settings"
            """
            context = kernel.get_context("/")
            if path is None:
                path = context.active
            if subcommand is None:
                channel(_("----------"))
                channel(_("Loaded Windows in Context %s:") % str(context._path))
                for i, name in enumerate(context.opened):
                    if not name.startswith("window"):
                        continue
                    module = context.opened[name]
                    channel(_("%d: %s as type of %s") % (i + 1, name, type(module)))

                channel(_("----------"))
                channel(_("Loaded Windows in Device %s:") % str(path._path))
                for i, name in enumerate(path.opened):
                    if not name.startswith("window"):
                        continue
                    module = path.opened[name]
                    channel(_("%d: %s as type of %s") % (i + 1, name, type(module)))
                channel(_("----------"))
                return
            if window is None or subcommand == "list":
                channel(_("----------"))
                channel(_("Windows Registered:"))
                for i, name in enumerate(context.match("window")):
                    channel("%d: %s" % (i + 1, name))
                return
            elif subcommand == "open":
                try:
                    parent = context.gui
                except AttributeError:
                    parent = None
                try:
                    path.open("window/%s" % window, parent, *args)
                    channel(_("Window Opened."))
                except (KeyError, ValueError):
                    channel(_("No such window as %s" % window))
                except IndexError:
                    raise SyntaxError
            elif subcommand == "close":
                try:
                    parent = context.gui
                except AttributeError:
                    parent = None
                try:
                    path.close("window/%s" % window, parent, *args)
                    channel(_("Window closed."))
                except (KeyError, ValueError):
                    channel(_("No such window as %s" % window))
                except IndexError:
                    raise SyntaxError
            elif subcommand == "reset":
                if kernel._config is not None:
                    for context in list(kernel.contexts):
                        if context.startswith("window"):
                            del kernel.contexts[context]
                    kernel._config.DeleteGroup("window")
            else:
                raise SyntaxError

        @kernel.console_argument("subcommand", type=str, help="subcommand")
        @kernel.console_argument("view", type=str, help="mode")
        @kernel.console_command(
            "view_setting", help="view_settings <toggle/set/unset> <view>"
        )
        def toggle_draw_mode(subcommand, view, **kwargs):
            """
            Toggle the draw mode.
            """
            if view is None:
                raise SyntaxError
            context = kernel.get_context("/")
            if view == "estimate":
                bits = DRAW_MODE_ESTIMATE
            elif view == "gcode":
                bits = DRAW_MODE_GCODE
            elif view == "cut":
                bits = DRAW_MODE_CUT
            elif view == "engrave":
                bits = DRAW_MODE_ENGRAVE
            elif view == "raster":
                bits = DRAW_MODE_RASTER
            elif view == "grid":
                bits = DRAW_MODE_GRID
            elif view == "guide":
                bits = DRAW_MODE_GUIDES
            elif view == "background":
                bits = DRAW_MODE_BACKGROUND
            elif view == "flip":
                bits = DRAW_MODE_FLIPXY
            elif view == "invert":
                bits = DRAW_MODE_INVERT
            else:
                raise SyntaxError
            if subcommand == "toggle":
                context.draw_mode ^= bits
            elif subcommand == "set":
                context.draw_mode |= bits
            elif subcommand == "unset":
                context.draw_mode |= bits
                context.draw_mode ^= bits
            else:
                raise SyntaxError
            context.signal("draw_mode", context.draw_mode)
            context.signal("refresh_scene")

    def run_later(self, command, *args):
        if wx.IsMainThread():
            command(*args)
        else:
            wx.CallAfter(command, *args)

    def initialize(self, *args, **kwargs):
        context = self.context

        try:  # pyinstaller internal location
            _resource_path = os.path.join(sys._MEIPASS, "locale")
            wx.Locale.AddCatalogLookupPathPrefix(_resource_path)
        except Exception:
            pass

        try:  # Mac py2app resource
            _resource_path = os.path.join(os.environ["RESOURCEPATH"], "locale")
            wx.Locale.AddCatalogLookupPathPrefix(_resource_path)
        except Exception:
            pass

        wx.Locale.AddCatalogLookupPathPrefix(
            "locale"
        )  # Default Locale, prepended. Check this first.

        context._kernel.run_later = self.run_later
        context._kernel.translation = wx.GetTranslation
        context._kernel.set_config(wx.Config(context._kernel.profile))
        context.app = self  # Registers self as kernel.app

        context.setting(int, "language", None)
        language = context.language
        if language is not None and language != 0:
            self.update_language(language)

    def update_language(self, lang):
        """
        Update language to the requested language.
        """
        context = self.context
        try:
            language_code, language_name, language_index = supported_languages[lang]
        except (IndexError, ValueError):
            return
        context.language = lang

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale
        self.locale = wx.Locale(language_index)
        if self.locale.IsOk():
            self.locale.AddCatalog("silence")
        else:
            self.locale = None
        context.signal("language", (lang, language_code, language_name, language_index))
