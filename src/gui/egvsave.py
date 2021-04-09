import wx

from src.gui.mwindow import MWindow

MILS_IN_MM = 39.3701


class EgvSave(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(403, 163, *args, **kwds)
        self.context.setting(bool, "egvsave_cut", True)
        self.context.setting(bool, "egvsave_engrave", True)
        self.context.setting(bool, "egvsave_raster", True)
        self.context.setting(bool, "egvsave_gcode", False)
        self.panel_24 = wx.Panel(self, wx.ID_ANY)
        self.check_raster = wx.CheckBox(self.panel_24, wx.ID_ANY, "Raster Engrave")
        self.check_raster.SetValue(self.context.egvsave_raster)
        self.check_engrave = wx.CheckBox(self.panel_24, wx.ID_ANY, "Vector Engrave")
        self.check_engrave.SetValue(self.context.egvsave_engrave)
        self.check_cut = wx.CheckBox(self.panel_24, wx.ID_ANY, "Vector Cut")
        self.check_cut.SetValue(self.context.egvsave_cut)
        self.check_gcode = wx.CheckBox(self.panel_24, wx.ID_ANY, "GCode Operation")
        self.check_gcode.SetValue(self.context.egvsave_gcode)

        self.button_save = wx.Button(self.panel_24, wx.ID_ANY, "Save")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.on_check_egv_raster, self.check_raster)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_egv_engrave, self.check_engrave)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_egv_cut, self.check_cut)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_egv_gcode, self.check_gcode)
        self.Bind(wx.EVT_BUTTON, self.on_button_save, self.button_save)

    def __set_properties(self):
        # begin wxGlade: EgvSave.__set_properties
        self.SetTitle("EGV Save Options")
        self.check_raster.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.check_raster.SetToolTip(
            "Save the Raster Engrave data to an EGV file. The file will contain the data that would be sent to the laser if the Raster Engrave button was pressed."
        )
        self.check_engrave.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.check_engrave.SetToolTip(
            "Save the Vector Engrave data to an EGV file. The file will contain the data that would be sent to the laser if the Vector Engrave button was pressed."
        )
        self.check_cut.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.check_cut.SetToolTip(
            "Save the Vector Cut data to an EGV file. The file will contain the data that would be sent to the laser if the Vector Cut button was pressed."
        )
        self.check_gcode.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.check_gcode.SetToolTip(
            "Save the G-Code Run data to an EGV file. The file will contain the data that would be sent to the laser if the G-Code Run button was pressed."
        )
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: EgvSave.__do_layout
        sizer_55 = wx.BoxSizer(wx.VERTICAL)
        sizer_56 = wx.BoxSizer(wx.VERTICAL)
        sizer_56.Add(self.check_raster, 0, 0, 0)
        sizer_56.Add(self.check_engrave, 0, 0, 0)
        sizer_56.Add(self.check_cut, 0, 0, 0)
        sizer_56.Add(self.check_gcode, 0, 0, 0)
        sizer_56.Add(self.button_save, 0, wx.EXPAND, 0)
        self.panel_24.SetSizer(sizer_56)
        sizer_55.Add(self.panel_24, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_55)
        self.Layout()
        self.Centre()
        # end wxGlade

    def on_check_egv_raster(self, event):  # wxGlade: EgvSave.<event_handler>
        self.context.egvsave_raster = bool(self.check_raster.GetValue())

    def on_check_egv_engrave(self, event):  # wxGlade: EgvSave.<event_handler>
        self.context.egvsave_engrave = bool(self.check_engrave.GetValue())

    def on_check_egv_cut(self, event):  # wxGlade: EgvSave.<event_handler>
        self.context.egvsave_cut = bool(self.check_cut.GetValue())

    def on_check_egv_gcode(self, event):  # wxGlade: EgvSave.<event_handler>
        self.context.egvsave_gcode = bool(self.check_gcode.GetValue())

    def on_button_save(self, event):  # wxGlade: EgvSave.<event_handler>
        self.context.console("egv_save\n")


# end of class EgvSave
