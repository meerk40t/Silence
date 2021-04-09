import wx

from src.gui.mwindow import MWindow

MILS_IN_MM = 39.3701


class RasterSettings(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(324, 155, *args, **kwds)
        self.text_scanline_step = wx.TextCtrl(self, wx.ID_ANY, "0.002")
        self.check_invert = wx.CheckBox(
            self, wx.ID_ANY, "Invert Raster Color", style=wx.ALIGN_RIGHT
        )
        self.check_bottom_up = wx.CheckBox(
            self, wx.ID_ANY, "Engrave Bottom Up", style=wx.ALIGN_RIGHT
        )
        self.check_wizard = wx.CheckBox(
            self, wx.ID_ANY, "Apply RasterWizard", style=wx.ALIGN_RIGHT
        )
        choices = [
            script_name for script_name in self.context.match("raster_script", True)
        ]
        self.combo_wizard = wx.ComboBox(
            self, wx.ID_ANY, choices=choices, style=wx.CB_DROPDOWN
        )

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.on_text_scanline_step, self.text_scanline_step)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_invert, self.check_invert)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_bottom2top, self.check_bottom_up)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_wizard, self.check_wizard)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_wizard, self.combo_wizard)
        # end wxGlade
        self.context.setting(bool, "wizard", True)
        self.context.setting(str, "wizard_script", "Gravy")
        self.context.setting(bool, "invert", False)
        step = self.context.elements.raster_settings.raster_step
        self.text_scanline_step.SetValue(str(step / 1000.0))
        self.check_bottom_up.SetValue(
            self.context.elements.raster_settings.raster_direction
        )
        self.check_wizard.SetValue(self.context.wizard)
        self.combo_wizard.SetValue(self.context.wizard_script)

        self.context.listen("invert", self.on_invert)
        self.context.listen("wizard", self.on_wizard)

    def window_close(self):
        self.context.unlisten("wizard", self.on_wizard)
        self.context.unlisten("invert", self.on_invert)

    def __set_properties(self):
        # begin wxGlade: RasterSettings.__set_properties
        self.SetTitle("Raster Settings")
        self.check_wizard.SetValue(1)
        self.combo_wizard.SetMinSize((200, 23))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RasterSettings.__do_layout
        rastersetting_sizer = wx.BoxSizer(wx.VERTICAL)
        scanline_sizer = wx.WrapSizer(wx.VERTICAL)
        label_30 = wx.StaticText(self, wx.ID_ANY, "Scanline Step")
        label_30.SetMinSize((150, 16))
        scanline_sizer.Add(label_30, 0, 0, 0)
        scanline_sizer.Add(self.text_scanline_step, 0, 0, 0)
        label_37 = wx.StaticText(self, wx.ID_ANY, "in")
        scanline_sizer.Add(label_37, 0, 0, 0)
        rastersetting_sizer.Add(scanline_sizer, 0, wx.EXPAND, 0)
        rastersetting_sizer.Add(self.check_invert, 0, 0, 0)
        rastersetting_sizer.Add(self.check_bottom_up, 0, 0, 0)
        rastersetting_sizer.Add(self.check_wizard, 0, 0, 0)
        rastersetting_sizer.Add(self.combo_wizard, 0, 0, 0)
        self.SetSizer(rastersetting_sizer)
        self.Layout()
        # end wxGlade

    def on_wizard(self, *args, **kwargs):
        self.check_wizard.SetValue(self.context.wizard)

    def on_invert(self, *args, **kwargs):
        self.check_invert.SetValue(self.context.invert)

    def on_text_scanline_step(self, event):  # wxGlade: RasterSettings.<event_handler>
        try:

            self.context.elements.raster_settings.raster_step = int(
                float(self.text_scanline_step.GetValue()) * 1000
            )
        except ValueError:
            pass

    def on_check_bottom2top(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.elements.raster_settings.raster_direction = (
            1 if self.check_bottom_up.GetValue() else 0
        )

    def on_check_invert(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.invert = bool(self.check_invert.GetValue())
        self.context.signal("invert", self.context.invert)

    def on_check_wizard(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.wizard = bool(self.check_wizard.GetValue())
        self.context.signal("wizard", self.context.wizard)

    def on_combo_wizard(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.wizard_script = self.combo_wizard.GetValue()


# end of class RasterSettings
