import wx

from src.gui.mwindow import MWindow

MILS_IN_MM = 39.3701


class TraceBoundary(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(503, 195, *args, **kwds)
        self.context.setting(int, "trace_power", 100)
        self.context.setting(float, "trace_gap", 0.0)
        self.context.setting(float, "trace_speed", 50)
        self.context.setting(bool, "trace_laser_on", False)

        self.panel_25 = wx.Panel(self, wx.ID_ANY)
        self.checkbox_trace_laser = wx.CheckBox(self.panel_25, wx.ID_ANY, "")
        self.checkbox_trace_laser.SetValue(bool(self.context.trace_laser_on))
        self.text_trace_power = wx.TextCtrl(
            self.panel_25, wx.ID_ANY, str(self.context.trace_power)
        )
        self.text_trace_gap = wx.TextCtrl(
            self.panel_25, wx.ID_ANY, str(self.context.trace_gap)
        )
        self.text_trace_speed = wx.TextCtrl(
            self.panel_25, wx.ID_ANY, str(self.context.trace_speed)
        )
        self.button_trace = wx.Button(self.panel_25, wx.ID_ANY, "Trace")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.on_check_trace_laser, self.checkbox_trace_laser)
        self.Bind(wx.EVT_TEXT, self.on_text_trace_power, self.text_trace_power)
        self.Bind(wx.EVT_TEXT, self.on_text_trace_gap, self.text_trace_gap)
        self.Bind(wx.EVT_TEXT, self.on_text_trace_speed, self.text_trace_speed)
        self.Bind(wx.EVT_BUTTON, self.on_button_trace, self.button_trace)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: TraceBoundary.__set_properties
        self.SetTitle("Trace Boundary")
        self.text_trace_speed.SetForegroundColour(wx.Colour(0, 255, 0))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: TraceBoundary.__do_layout
        sizer_57 = wx.BoxSizer(wx.VERTICAL)
        sizer_58 = wx.BoxSizer(wx.VERTICAL)
        sizer_62 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_61 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_60 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_59 = wx.BoxSizer(wx.HORIZONTAL)
        label_42 = wx.StaticText(self.panel_25, wx.ID_ANY, "Laser 'On' During Trace")
        label_42.SetMinSize((150, 16))
        sizer_59.Add(label_42, 0, 0, 0)
        sizer_59.Add(self.checkbox_trace_laser, 0, 0, 0)
        sizer_58.Add(sizer_59, 1, wx.EXPAND, 0)
        label_43 = wx.StaticText(self.panel_25, wx.ID_ANY, "Power (PPI) Trace")
        label_43.SetMinSize((150, 16))
        sizer_60.Add(label_43, 0, 0, 0)
        sizer_60.Add(self.text_trace_power, 0, 0, 0)
        label_46 = wx.StaticText(self.panel_25, wx.ID_ANY, "ppi")
        sizer_60.Add(label_46, 0, 0, 0)
        sizer_58.Add(sizer_60, 1, wx.EXPAND, 0)
        label_44 = wx.StaticText(self.panel_25, wx.ID_ANY, "Outline Gap")
        label_44.SetMinSize((150, 16))
        label_44.SetToolTip("Gap between design and trace.")
        sizer_61.Add(label_44, 0, 0, 0)
        sizer_61.Add(self.text_trace_gap, 0, 0, 0)
        label_47 = wx.StaticText(self.panel_25, wx.ID_ANY, "mm")
        sizer_61.Add(label_47, 0, 0, 0)
        sizer_58.Add(sizer_61, 1, wx.EXPAND, 0)
        label_45 = wx.StaticText(self.panel_25, wx.ID_ANY, "Speed for Trace")
        label_45.SetMinSize((150, 16))
        sizer_62.Add(label_45, 0, 0, 0)
        sizer_62.Add(self.text_trace_speed, 0, 0, 0)
        label_48 = wx.StaticText(self.panel_25, wx.ID_ANY, "mm/s")
        sizer_62.Add(label_48, 0, 0, 0)
        sizer_58.Add(sizer_62, 1, wx.EXPAND, 0)
        sizer_58.Add(self.button_trace, 0, wx.EXPAND, 0)
        self.panel_25.SetSizer(sizer_58)
        sizer_57.Add(self.panel_25, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_57)
        self.Layout()
        # end wxGlade

    def on_check_trace_laser(self, event):  # wxGlade: TraceBoundary.<event_handler>
        self.context.trace_laser_on = bool(self.checkbox_trace_laser.GetValue())

    def on_text_trace_power(self, event):  # wxGlade: TraceBoundary.<event_handler>
        try:
            self.context.trace_power = int(self.text_trace_power.GetValue())
        except ValueError:
            pass

    def on_text_trace_gap(self, event):  # wxGlade: TraceBoundary.<event_handler>
        try:
            self.context.trace_gap = float(self.text_trace_gap.GetValue())
        except ValueError:
            pass

    def on_text_trace_speed(self, event):  # wxGlade: TraceBoundary.<event_handler>
        try:
            self.context.trace_speed = float(self.text_trace_speed.GetValue())
        except ValueError:
            pass

    def on_button_trace(self, event):  # wxGlade: TraceBoundary.<event_handler>
        self.context.console("trace execute\n")


# end of class TraceBoundary
