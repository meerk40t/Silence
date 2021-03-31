import wx

from src.gui.mwindow import MWindow

MILS_IN_MM = 39.3701


class RasterSettings(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(729, 370, *args, **kwds)
        self.panel_22 = wx.Panel(self, wx.ID_ANY)
        self.text_scanline_step = wx.TextCtrl(self.panel_22, wx.ID_ANY, "0.002")
        self.check_bottom_up = wx.CheckBox(self.panel_22, wx.ID_ANY, "")
        self.check_halftone = wx.CheckBox(self.panel_22, wx.ID_ANY, "")
        self.choice_halftone_resolution = wx.Choice(
            self.panel_22,
            wx.ID_ANY,
            choices=["1000", "500", "333", "250", "200", "163", "143", "125"],
        )
        self.slider_raster_black = wx.Slider(
            self.panel_22,
            wx.ID_ANY,
            0,
            1,
            50,
            style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS,
        )
        self.slider_raster_white = wx.Slider(
            self.panel_22,
            wx.ID_ANY,
            0,
            0,
            1,
            style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS,
        )
        self.slider_raster_transition = wx.Slider(
            self.panel_22,
            wx.ID_ANY,
            0,
            0,
            10,
            style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS,
        )
        self.panel_raster_curve = wx.Panel(self, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.on_text_scanline_step, self.text_scanline_step)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_bottom2top, self.check_bottom_up)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_halftone, self.check_halftone)
        self.Bind(
            wx.EVT_CHOICE,
            self.on_choice_halftone_resolution,
            self.choice_halftone_resolution,
        )
        self.Bind(wx.EVT_COMMAND_SCROLL, self.on_slider_black, self.slider_raster_black)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.on_slider_white, self.slider_raster_white)
        self.Bind(
            wx.EVT_COMMAND_SCROLL,
            self.on_slider_transition,
            self.slider_raster_transition,
        )
        # end wxGlade
        self.context.setting(int, "raster_step", 2)
        self.context.setting(bool, "raster_bottom", False)
        self.context.setting(bool, "halftone", True)
        self.context.setting(int, "halftone_resolution", 2)
        self.context.setting(float, "halftone_black", 2.5)
        self.context.setting(float, "halftone_white", 0.50)
        self.context.setting(float, "halftone_transition", 3.5)
        self.text_scanline_step.SetValue(str(self.context.raster_step / 1000.0))
        self.check_bottom_up.SetValue(self.context.raster_bottom)
        self.check_halftone.SetValue(self.context.halftone)
        self.slider_raster_black.SetValue(self.context.halftone_black)
        self.slider_raster_white.SetValue(self.context.halftone_white)
        self.slider_raster_transition.SetValue(self.context.halftone_transition)
        self.context.listen("halftone", self.on_halftone)
        self.toggle_disabled()

    def on_halftone(self, *args, **kwargs):
        self.check_halftone.SetValue(self.context.halftone)
        self.toggle_disabled()

    def toggle_disabled(self):
        self.choice_halftone_resolution.Enable(self.context.halftone)
        self.slider_raster_black.Enable(self.context.halftone)
        self.slider_raster_white.Enable(self.context.halftone)
        self.slider_raster_transition.Enable(self.context.halftone)

    def window_close(self):
        self.context.unlisten("halftone", self.on_halftone)

    def __set_properties(self):
        # begin wxGlade: RasterSettings.__set_properties
        self.SetTitle("Raster Settings")
        self.check_halftone.SetValue(1)
        self.choice_halftone_resolution.SetSelection(0)
        self.panel_raster_curve.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RasterSettings.__do_layout
        sizer_41 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_42 = wx.BoxSizer(wx.VERTICAL)
        sizer_49 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_48 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_47 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_46 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_45 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_44 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_43 = wx.BoxSizer(wx.HORIZONTAL)
        label_30 = wx.StaticText(self.panel_22, wx.ID_ANY, "Scanline Step")
        label_30.SetMinSize((150, 16))
        sizer_43.Add(label_30, 0, 0, 0)
        sizer_43.Add(self.text_scanline_step, 0, 0, 0)
        label_37 = wx.StaticText(self.panel_22, wx.ID_ANY, "in")
        sizer_43.Add(label_37, 0, 0, 0)
        sizer_42.Add(sizer_43, 1, wx.EXPAND, 0)
        label_31 = wx.StaticText(self.panel_22, wx.ID_ANY, "Engrave Bottom Up")
        label_31.SetMinSize((150, 16))
        sizer_44.Add(label_31, 0, 0, 0)
        sizer_44.Add(self.check_bottom_up, 0, 0, 0)
        sizer_42.Add(sizer_44, 1, wx.EXPAND, 0)
        label_32 = wx.StaticText(self.panel_22, wx.ID_ANY, "Halftone (Dither)")
        label_32.SetMinSize((150, 16))
        sizer_45.Add(label_32, 0, 0, 0)
        sizer_45.Add(self.check_halftone, 0, 0, 0)
        sizer_42.Add(sizer_45, 1, wx.EXPAND, 0)
        label_33 = wx.StaticText(self.panel_22, wx.ID_ANY, "Halftone Resolution")
        label_33.SetMinSize((150, 16))
        sizer_46.Add(label_33, 0, 0, 0)
        sizer_46.Add(self.choice_halftone_resolution, 0, 0, 0)
        label_38 = wx.StaticText(self.panel_22, wx.ID_ANY, "dpi")
        sizer_46.Add(label_38, 0, 0, 0)
        sizer_42.Add(sizer_46, 1, wx.EXPAND, 0)
        label_34 = wx.StaticText(self.panel_22, wx.ID_ANY, "Slope, Black (2.5)")
        label_34.SetMinSize((150, 16))
        sizer_47.Add(label_34, 0, 0, 0)
        sizer_47.Add(self.slider_raster_black, 1, wx.EXPAND, 0)
        sizer_42.Add(sizer_47, 1, wx.EXPAND, 0)
        label_35 = wx.StaticText(self.panel_22, wx.ID_ANY, "Slope, White (0.50)")
        label_35.SetMinSize((150, 16))
        sizer_48.Add(label_35, 0, 0, 0)
        sizer_48.Add(self.slider_raster_white, 1, wx.EXPAND, 0)
        sizer_42.Add(sizer_48, 1, wx.EXPAND, 0)
        label_36 = wx.StaticText(self.panel_22, wx.ID_ANY, "Transition (2.5)")
        label_36.SetMinSize((150, 16))
        sizer_49.Add(label_36, 0, 0, 0)
        sizer_49.Add(self.slider_raster_transition, 1, wx.EXPAND, 0)
        sizer_42.Add(sizer_49, 1, wx.EXPAND, 0)
        self.panel_22.SetSizer(sizer_42)
        sizer_41.Add(self.panel_22, 1, wx.EXPAND, 0)
        sizer_41.Add(self.panel_raster_curve, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_41)
        self.Layout()
        # end wxGlade

    def on_text_scanline_step(self, event):  # wxGlade: RasterSettings.<event_handler>
        try:
            self.context.raster_step = int(
                float(self.text_scanline_step.GetValue()) * 1000
            )
        except ValueError:
            pass

    def on_check_bottom2top(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.raster_bottom = self.check_bottom_up.Value

    def on_check_halftone(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.halftone = self.check_halftone.Value
        self.context.signal("halftone", self.context.halftone)
        self.toggle_disabled()

    def on_choice_halftone_resolution(
            self, event
    ):  # wxGlade: RasterSettings.<event_handler>
        self.context.halftone_resolution = (
            self.choice_halftone_resolution.GetSelection()
        )

    def on_slider_black(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.halftone_black = self.slider_raster_black.Value

    def on_slider_white(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.halftone_black = self.slider_raster_white.Value

    def on_slider_transition(self, event):  # wxGlade: RasterSettings.<event_handler>
        self.context.halftone_black = self.slider_raster_transition.Value

# end of class RasterSettings
