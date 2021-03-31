import wx

from src.gui.mwindow import MWindow

MILS_IN_MM = 39.3701


class RotarySettings(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(391, 155, *args, **kwds)
        self.panel_23 = wx.Panel(self, wx.ID_ANY)
        self.check_rotary_enable = wx.CheckBox(self.panel_23, wx.ID_ANY, "")
        self.text_rotary_scale_y = wx.TextCtrl(self.panel_23, wx.ID_ANY, "1.000")
        self.text_rotary_speed_rapid = wx.TextCtrl(self.panel_23, wx.ID_ANY, "0.0")

        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_rotary_enable, self.check_rotary_enable
        )
        self.Bind(wx.EVT_TEXT, self.on_text_rotary_scale_y, self.text_rotary_scale_y)
        self.Bind(wx.EVT_TEXT, self.on_text_rotary_speed, self.text_rotary_speed_rapid)
        # end wxGlade
        self.context.setting(bool, "rotary_enable", False)
        self.context.setting(float, "rotary_scale_y", 1.0)
        self.context.setting(float, "rotary_speed", 0.0)
        self.check_rotary_enable.SetValue(self.context.rotary_enable)
        self.text_rotary_scale_y.SetValue(str(self.context.rotary_scale_y))
        self.text_rotary_speed_rapid.SetValue(str(self.context.rotary_speed))
        self.toggle_disabled()
        self.context.listen("rotary_enable", self.on_rotary_enable)

    def toggle_disabled(self):
        self.text_rotary_scale_y.Enable(self.check_rotary_enable.Value)
        self.text_rotary_speed_rapid.Enable(self.check_rotary_enable.Value)

    def on_rotary_enable(self, *args, **kwargs):
        self.check_rotary_enable.SetValue(self.context.rotary_enable)
        self.toggle_disabled()

    def window_close(self):
        self.context.unlisten("rotary_enable", self.on_rotary_enable)

    def __set_properties(self):
        # begin wxGlade: RotarySettings.__set_properties
        self.SetTitle("Rotary Settings")
        self.check_rotary_enable.SetToolTip(
            "This option causes the program to use the settings in the rotary settings window intended to be used with a rotary devices attached to the y-axis connector on the controller board."
        )
        self.text_rotary_scale_y.SetToolTip(
            "This is the scale factor applied to the y-axis inputs to adjust the output for use on a rotary device.\nSince you will need to plug the rotary axis into the Y-axis motor driver. You will likely need to change the scale factor so that the Y-Axis moves the correct amount when rotating the rotary axis. The needed scale factor can be determined by engraving a vertical line 1 inch long then measuring the length of the engraved line. You divide the input length by the actual engraved length around the circular object to get the scale factor.\n\n(input length)/(engraved length) = Needed Scale Factor\nMake sure the scale factor is set to 1.0 before performing the test described above."
        )
        self.text_rotary_speed_rapid.SetToolTip(
            "This option can set the rapid speed when the rotary settings are enabled. It is common for the high default rapid speeds to cause items on a rotary device to jump off of the rollers. With this option the rapid speeds can be reduced to prevent this."
        )
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RotarySettings.__do_layout
        sizer_50 = wx.BoxSizer(wx.VERTICAL)
        sizer_51 = wx.BoxSizer(wx.VERTICAL)
        sizer_54 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_53 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_52 = wx.BoxSizer(wx.HORIZONTAL)
        label_39 = wx.StaticText(self.panel_23, wx.ID_ANY, "Use Rotary Settings")
        label_39.SetMinSize((200, 16))
        sizer_52.Add(label_39, 0, 0, 0)
        sizer_52.Add(self.check_rotary_enable, 0, 0, 0)
        sizer_51.Add(sizer_52, 1, wx.EXPAND, 0)
        label_40 = wx.StaticText(
            self.panel_23, wx.ID_ANY, "Rotary Scale Factor (Y axis)"
        )
        label_40.SetMinSize((200, 16))
        sizer_53.Add(label_40, 0, 0, 0)
        sizer_53.Add(self.text_rotary_scale_y, 0, 0, 0)
        sizer_51.Add(sizer_53, 1, wx.EXPAND, 0)
        label_41 = wx.StaticText(self.panel_23, wx.ID_ANY, "Rapid Speed (default=0)")
        label_41.SetMinSize((200, 16))
        sizer_54.Add(label_41, 0, 0, 0)
        sizer_54.Add(self.text_rotary_speed_rapid, 0, 0, 0)
        sizer_51.Add(sizer_54, 1, wx.EXPAND, 0)
        self.panel_23.SetSizer(sizer_51)
        sizer_50.Add(self.panel_23, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_50)
        self.Layout()
        # end wxGlade

    def on_check_rotary_enable(self, event):  # wxGlade: RotarySettings.<event_handler>
        self.context.rotary_enable = self.check_rotary_enable.Value
        self.context.signal("rotary_enable", self.context.rotary_enable)
        self.toggle_disabled()

    def on_text_rotary_scale_y(self, event):  # wxGlade: RotarySettings.<event_handler>
        try:
            self.context.rotary_scale_y = float(self.text_rotary_scale_y.Value)
        except ValueError:
            pass

    def on_text_rotary_speed(self, event):  # wxGlade: RotarySettings.<event_handler>
        try:
            self.context.rotary_speed = float(self.text_rotary_speed_rapid.Value)
        except ValueError:
            pass

# end of class RotarySettings
