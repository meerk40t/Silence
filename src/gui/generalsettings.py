import wx

from src.gui.mwindow import MWindow

MILS_IN_MM = 39.3701


class GeneralSettings(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(570, 597, *args, **kwds)
        self.panel_5 = wx.Panel(self, wx.ID_ANY)
        self.radio_units_inch = wx.RadioButton(self.panel_5, wx.ID_ANY, "inch")
        self.radio_units_mm = wx.RadioButton(self.panel_5, wx.ID_ANY, "mm")
        self.panel_8 = wx.Panel(self, wx.ID_ANY)
        self.check_init_home = wx.CheckBox(self.panel_8, wx.ID_ANY, "")
        self.panel_10 = wx.Panel(self, wx.ID_ANY)
        self.check_finish_unlock_rail = wx.CheckBox(
            self.panel_10, wx.ID_ANY, "Unlock Rail"
        )
        self.check_finish_beep = wx.CheckBox(self.panel_10, wx.ID_ANY, "Beep")
        self.panel_13 = wx.Panel(self.panel_10, wx.ID_ANY)
        self.check_finish_popup_report = wx.CheckBox(
            self.panel_10, wx.ID_ANY, "Popup Report"
        )
        self.check_finish_run_batch = wx.CheckBox(
            self.panel_10, wx.ID_ANY, "Run Batch File:"
        )
        self.text_batch_file = wx.TextCtrl(self.panel_10, wx.ID_ANY, "")
        self.panel_11 = wx.Panel(self, wx.ID_ANY)
        self.check_preprocess_crc = wx.CheckBox(self.panel_11, wx.ID_ANY, "")
        self.panel_12 = wx.Panel(self, wx.ID_ANY)
        self.text_inkscape_path = wx.TextCtrl(self.panel_12, wx.ID_ANY, "")
        self.button_find_inkscape = wx.Button(self.panel_12, wx.ID_ANY, "Find Inkscape")
        self.text_inkscape_timeout = wx.TextCtrl(self.panel_12, wx.ID_ANY, "3")
        self.panel_14 = wx.Panel(self, wx.ID_ANY)
        self.check_home_upper_right = wx.CheckBox(self.panel_14, wx.ID_ANY, "")
        self.panel_15 = wx.Panel(self, wx.ID_ANY)
        self.choice_board_name = wx.Choice(
            self.panel_15,
            wx.ID_ANY,
            choices=[
                "LASER-M2",
                "LASER-M1",
                "LASER-M",
                "LASER-B2",
                "LASER-B1",
                "LASER-B",
                "LASER-A",
                "Moshiboard",
            ],
        )
        self.panel_16 = wx.Panel(self, wx.ID_ANY)
        self.text_laser_width = wx.TextCtrl(self.panel_16, wx.ID_ANY, "325")
        self.panel_17 = wx.Panel(self, wx.ID_ANY)
        self.text_laser_height = wx.TextCtrl(self.panel_17, wx.ID_ANY, "220")
        self.panel_18 = wx.Panel(self, wx.ID_ANY)
        self.text_x_factor = wx.TextCtrl(self.panel_18, wx.ID_ANY, "1.000")
        self.panel_19 = wx.Panel(self, wx.ID_ANY)
        self.text_y_factor = wx.TextCtrl(self.panel_19, wx.ID_ANY, "1.000")
        self.panel_20 = wx.Panel(self, wx.ID_ANY)
        self.button_save = wx.Button(self.panel_20, wx.ID_ANY, "Save")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_unit_change, self.radio_units_inch)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_unit_change, self.radio_units_mm)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_init_home, self.check_init_home)
        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_finish_unlock, self.check_finish_unlock_rail
        )
        self.Bind(wx.EVT_CHECKBOX, self.on_check_finish_beep, self.check_finish_beep)
        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_finish_popup, self.check_finish_popup_report
        )
        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_finish_batch, self.check_finish_run_batch
        )
        self.Bind(wx.EVT_TEXT, self.on_text_batchfile, self.text_batch_file)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_preprocess, self.check_preprocess_crc)
        self.Bind(wx.EVT_TEXT, self.on_text_inkscape_path, self.text_inkscape_path)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_find_inkscape, self.button_find_inkscape
        )
        self.Bind(
            wx.EVT_TEXT, self.on_text_inkscape_timeout, self.text_inkscape_timeout
        )
        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_home_upper_right, self.check_home_upper_right
        )
        self.Bind(wx.EVT_CHOICE, self.on_choice_board, self.choice_board_name)
        self.Bind(wx.EVT_TEXT, self.on_text_bed_width, self.text_laser_width)
        self.Bind(wx.EVT_TEXT, self.on_text_bed_height, self.text_laser_height)
        self.Bind(wx.EVT_TEXT, self.on_text_x_factor, self.text_x_factor)
        self.Bind(wx.EVT_TEXT, self.on_text_y_factor, self.text_y_factor)
        self.Bind(wx.EVT_BUTTON, self.on_button_save, self.button_save)
        # end wxGlade
        self.context.setting(int, "units", 0)
        self.context.setting(bool, "init_home", True)
        self.context.setting(bool, "finish_unlock", False)
        self.context.setting(bool, "finish_beep", False)
        self.context.setting(bool, "finish_batch", False)
        self.context.setting(bool, "finish_popup", False)
        self.context.setting(str, "finish_batch_file", None)
        self.context.setting(bool, "crc_preprocess", False)
        self.context.setting(str, "inkscape_path", None)
        self.context.setting(float, "inkscape_timeout", 3.0)
        self.context.setting(bool, "home_right", False)
        self.context.setting(str, "board", "M2")
        self.bed_dim = self.context.get_context('bed')
        self.bed_dim.setting(float, "bed_width", 325.0)
        self.bed_dim.setting(float, "bed_height", 220.0)
        self.context.setting(float, "bed_width", 325.0)
        self.context.setting(float, "bed_height", 220.0)
        self.context.setting(float, "x_factor", 1.0)
        self.context.setting(float, "y_factor", 1.0)
        if self.context.units == 0:
            self.radio_units_mm.SetValue(True)
            self.radio_units_inch.SetValue(False)
        else:
            self.radio_units_mm.SetValue(False)
            self.radio_units_inch.SetValue(True)
        self.check_init_home.SetValue(self.context.init_home)
        self.check_finish_unlock_rail.SetValue(self.context.finish_unlock)
        self.check_finish_beep.SetValue(self.context.finish_beep)
        self.check_finish_run_batch.SetValue(self.context.finish_batch)
        self.check_finish_popup_report.SetValue(self.context.finish_popup)
        if self.context.finish_batch_file is not None:
            self.text_batch_file.SetValue(self.context.finish_batch_file)
        self.check_preprocess_crc.SetValue(self.context.crc_preprocess)
        if self.context.inkscape_path is not None:
            self.text_inkscape_path.SetValue(self.context.inkscape_path)
        self.text_inkscape_timeout.SetValue(str(self.context.inkscape_timeout))
        self.check_home_upper_right.SetValue(self.context.home_right)
        self.choice_board_name.SetStringSelection(self.context.board)
        self.text_laser_width.SetValue(str(self.bed_dim.bed_width))
        self.text_laser_height.SetValue(str(self.bed_dim.bed_height))
        self.text_x_factor.SetValue(str(self.context.x_factor))
        self.text_y_factor.SetValue(str(self.context.y_factor))

    def __set_properties(self):
        # begin wxGlade: GeneralSettings.__set_properties
        self.SetTitle("General Settings")
        self.radio_units_inch.SetToolTip("Set the working units.")
        self.radio_units_mm.SetToolTip("Set the working units.")
        self.check_init_home.SetToolTip(
            "This option determines if the laser will move to the home position when the laser is initialized. If Home Upon Initialize is turned off the laser will remain in the current location when it is initialized and the rail will be unlocked. The only indication that the laser properly initialized will be that a message in the status bar will say the rail successfully unlocked."
        )
        self.check_init_home.SetValue(1)
        self.check_preprocess_crc.SetToolTip(
            "For each packet of data sent to the laser a Cyclic Redundancy Check (CRC) code is sent to ensure the data is received correctly by the controller board. By default the CRC data is calculated before sending data to the laser. If you un-select this option you may save time by having the CRC data calculate on the fly. There is a chance the laser might pause (especially at the beginning of the job.) but the cutting and engraving should not be affected by the pauses."
        )
        self.check_preprocess_crc.SetValue(1)
        self.text_inkscape_path.SetToolTip(
            'The path to the Inkscape executable file "inkscape.exe".\n\nUnless your computer has a special Inkscape installation you should leave this entry blank. We will search the typical install locations for Windows and Linux.\n\nThese are the locations that will be searched:\nC:\\Program Files\\Inkscape\\inkscape.exe\nC:\\Program Files (x86)\\Inkscape\\inkscape.exe\n/usr/bin/inkscape\n/usr/local/bin/inkscape\n\nIf your Inkscape executable is not in one of these locations you will need to enter the full path to the executable file. Entering the path to a link to the file will not work in Windows (i.e. don\'t try to link your desktop icon.)\n\nIn Linux you can find the location of the executable by typing "which Inkscape" in a terminal window.\nIn Windows you can right click on your desktop icon and select properties. Then navigate to the executable.\n\nWhen you know the location of the executable you can use the Find Inkscape button to navigate to the executable and the path text will be entered in the entry field.'
        )
        self.text_inkscape_timeout.SetMinSize((50, 23))
        self.check_home_upper_right.SetToolTip(
            "Some lasers home in the upper right corner rather than the more common upper left corner. If your laser homes in the upper right corner you will want to select this option otherwise all of your engravings will come out mirrored and the jog buttons will be reversed."
        )
        self.choice_board_name.SetToolTip(
            'This option selects the version of the Lihuiyu controller board that you have installed in your laser. You can look at your board and find the writing that says "6C6879-LASER-xx" where xx is the version of you board and select the option from the drop down menu that matches most your board version. If you have a HT Master5, HT Master6, HT-XEON5 or HT-XEON-DRV I think you should choose LASER-M2. If you choose the wrong board the speeds will not be correct.\n\nList of the supported boards:\n- 6C6879-LASER-M2 (M2 Nano)\n- 6C6879-LASER-B1\n- 6C6879-LASER-M1\n- 6C6879-LASER-M\n- 6C6879-LASER-B\n- 6C6879-LASER-B2\n- 6C6879-LASER-A\n- Moshiboards.\n- HT Master5 (use LASER-M2 setting)\n- HT Master6 (use LASER-M2 setting)\n- HT-XEON5 (use LASER-M2 setting)\n- HT-XEON-DRV (use LASER-M2 setting)'
        )
        self.choice_board_name.SetSelection(0)
        self.text_laser_width.SetToolTip(
            "The value sets the usable laser width or size in the X-axis for your laser. This sets the size of the area displayed in the main window."
        )
        self.text_laser_height.SetToolTip(
            "The value sets the usable laser width or size in the Y-axis for your laser. This sets the size of the area displayed in the main window."
        )
        self.text_x_factor.SetToolTip(
            "The scale factor scales the output of your laser by the value entered. You might need to use the scale factor if you replace the pulley and belt on your X-axis. For example if you replace the belt and find that when you make a line that is 5 inches long in Inkscape but the output is 4.5 inches you would need to change the scale factor to 4.5/5.0 = 0.9."
        )
        self.text_y_factor.SetToolTip(
            "The scale factor scales the output of your laser by the value entered. You might need to use the scale factor if you replace the pulley and belt on your Y-axis. For example if you replace the belt and find that when you make a line that is 5 inches long in Inkscape but the output is 4.5 inches you would need to change the scale factor to 5.0/4.5 = 1.111.\n\nYou can also use the Y-Scale factor to accommodate the use of a rotary axis. Since you will need to plug the rotary axis into the Y-axis motor driver. You will also likely need to change the scale factor so that the Y-Axis moves the correct amount when rotating the rotary axis. Similar to the example above the rotary axis adjustment can be determined by engraving a vertical line 1 inch long then measuring the line. You divide the input length by the actual engraved length around the circular object to get the scale factor.\n\n(input length)/(engraved length) = Needed Scale Factor\nMake sure the scale factor is set to 1.0 before performing the test described above."
        )
        self.button_save.SetToolTip(
            "The Save button will save all of the current settings to a configuration file. "
        )
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GeneralSettings.__do_layout
        sizer_24 = wx.BoxSizer(wx.VERTICAL)
        sizer_25 = wx.BoxSizer(wx.VERTICAL)
        sizer_40 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_39 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_38 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_36 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_35 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_34 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_33 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_30 = wx.StaticBoxSizer(
            wx.StaticBox(self.panel_12, wx.ID_ANY, "Inkscape Options"), wx.VERTICAL
        )
        sizer_32 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_31 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_29 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_28 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(2, 3, 0, 0)
        sizer_27 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_26 = wx.BoxSizer(wx.HORIZONTAL)
        label_11 = wx.StaticText(self.panel_5, wx.ID_ANY, "Units")
        label_11.SetMinSize((150, 16))
        sizer_26.Add(label_11, 0, 0, 0)
        sizer_26.Add(self.radio_units_inch, 0, 0, 0)
        sizer_26.Add(self.radio_units_mm, 0, 0, 0)
        self.panel_5.SetSizer(sizer_26)
        sizer_25.Add(self.panel_5, 1, wx.EXPAND, 0)
        label_15 = wx.StaticText(self.panel_8, wx.ID_ANY, "Home Upon Initialize")
        label_15.SetMinSize((150, 16))
        sizer_27.Add(label_15, 0, 0, 0)
        sizer_27.Add(self.check_init_home, 0, 0, 0)
        self.panel_8.SetSizer(sizer_27)
        sizer_25.Add(self.panel_8, 1, wx.EXPAND, 0)
        label_16 = wx.StaticText(self.panel_10, wx.ID_ANY, "After Job Finishes:")
        label_16.SetMinSize((150, 16))
        sizer_28.Add(label_16, 0, 0, 0)
        grid_sizer_1.Add(self.check_finish_unlock_rail, 0, 0, 0)
        grid_sizer_1.Add(self.check_finish_beep, 0, 0, 0)
        grid_sizer_1.Add(self.panel_13, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.check_finish_popup_report, 0, 0, 0)
        grid_sizer_1.Add(self.check_finish_run_batch, 0, 0, 0)
        grid_sizer_1.Add(self.text_batch_file, 0, 0, 0)
        sizer_28.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.panel_10.SetSizer(sizer_28)
        sizer_25.Add(self.panel_10, 1, wx.EXPAND, 0)
        label_17 = wx.StaticText(self.panel_11, wx.ID_ANY, "Preprocess CRC Data")
        label_17.SetMinSize((150, 16))
        sizer_29.Add(label_17, 0, 0, 0)
        sizer_29.Add(self.check_preprocess_crc, 0, 0, 0)
        self.panel_11.SetSizer(sizer_29)
        sizer_25.Add(self.panel_11, 1, wx.EXPAND, 0)
        static_line_6 = wx.StaticLine(self, wx.ID_ANY)
        sizer_25.Add(static_line_6, 0, wx.EXPAND, 0)
        label_18 = wx.StaticText(self.panel_12, wx.ID_ANY, "Inkscape Executable")
        label_18.SetMinSize((150, 16))
        sizer_31.Add(label_18, 0, 0, 0)
        sizer_31.Add(self.text_inkscape_path, 0, 0, 0)
        sizer_31.Add(self.button_find_inkscape, 0, 0, 0)
        sizer_30.Add(sizer_31, 1, wx.EXPAND, 0)
        label_19 = wx.StaticText(self.panel_12, wx.ID_ANY, "Inkscape Timeout")
        label_19.SetMinSize((150, 16))
        sizer_32.Add(label_19, 0, 0, 0)
        sizer_32.Add(self.text_inkscape_timeout, 0, 0, 0)
        label_20 = wx.StaticText(self.panel_12, wx.ID_ANY, "minutes")
        sizer_32.Add(label_20, 0, 0, 0)
        sizer_30.Add(sizer_32, 1, wx.EXPAND, 0)
        self.panel_12.SetSizer(sizer_30)
        sizer_25.Add(self.panel_12, 1, wx.EXPAND, 0)
        static_line_9 = wx.StaticLine(self, wx.ID_ANY)
        sizer_25.Add(static_line_9, 0, wx.EXPAND, 0)
        label_21 = wx.StaticText(self.panel_14, wx.ID_ANY, "Home in Upper Right")
        label_21.SetMinSize((150, 16))
        sizer_33.Add(label_21, 0, 0, 0)
        sizer_33.Add(self.check_home_upper_right, 0, 0, 0)
        self.panel_14.SetSizer(sizer_33)
        sizer_25.Add(self.panel_14, 1, wx.EXPAND, 0)
        label_22 = wx.StaticText(self.panel_15, wx.ID_ANY, "Board Name")
        label_22.SetMinSize((150, 16))
        sizer_34.Add(label_22, 0, 0, 0)
        sizer_34.Add(self.choice_board_name, 0, 0, 0)
        self.panel_15.SetSizer(sizer_34)
        sizer_25.Add(self.panel_15, 1, wx.EXPAND, 0)
        label_23 = wx.StaticText(self.panel_16, wx.ID_ANY, "Laser Area Width")
        label_23.SetMinSize((150, 16))
        sizer_35.Add(label_23, 0, 0, 0)
        sizer_35.Add(self.text_laser_width, 0, 0, 0)
        label_24 = wx.StaticText(self.panel_16, wx.ID_ANY, "mm")
        sizer_35.Add(label_24, 0, 0, 0)
        self.panel_16.SetSizer(sizer_35)
        sizer_25.Add(self.panel_16, 1, wx.EXPAND, 0)
        label_25 = wx.StaticText(self.panel_17, wx.ID_ANY, "Laser Area Height")
        label_25.SetMinSize((150, 16))
        sizer_36.Add(label_25, 0, 0, 0)
        sizer_36.Add(self.text_laser_height, 0, 0, 0)
        label_26 = wx.StaticText(self.panel_17, wx.ID_ANY, "mm")
        sizer_36.Add(label_26, 0, 0, 0)
        self.panel_17.SetSizer(sizer_36)
        sizer_25.Add(self.panel_17, 1, wx.EXPAND, 0)
        label_27 = wx.StaticText(self.panel_18, wx.ID_ANY, "X Scale Factor")
        label_27.SetMinSize((150, 16))
        sizer_38.Add(label_27, 0, 0, 0)
        sizer_38.Add(self.text_x_factor, 0, 0, 0)
        self.panel_18.SetSizer(sizer_38)
        sizer_25.Add(self.panel_18, 1, wx.EXPAND, 0)
        label_28 = wx.StaticText(self.panel_19, wx.ID_ANY, "Y Scale Factor")
        label_28.SetMinSize((150, 16))
        sizer_39.Add(label_28, 0, 0, 0)
        sizer_39.Add(self.text_y_factor, 0, 0, 0)
        self.panel_19.SetSizer(sizer_39)
        sizer_25.Add(self.panel_19, 1, wx.EXPAND, 0)
        label_29 = wx.StaticText(self.panel_20, wx.ID_ANY, "Configuration File")
        label_29.SetMinSize((150, 16))
        sizer_40.Add(label_29, 0, 0, 0)
        sizer_40.Add(self.button_save, 0, 0, 0)
        self.panel_20.SetSizer(sizer_40)
        sizer_25.Add(self.panel_20, 1, wx.EXPAND, 0)
        sizer_24.Add(sizer_25, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_24)
        self.Layout()
        # end wxGlade

    def on_radio_unit_change(self, event):  # wxGlade: GeneralSettings.<event_handler>
        if self.radio_units_mm:
            self.context.units = 0
        if self.radio_units_inch:
            self.context.units = 1

    def on_check_init_home(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.init_home = self.check_init_home.Value

    def on_check_finish_unlock(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.finish_unlock = self.check_finish_unlock_rail.Value

    def on_check_finish_beep(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.finish_beep = self.check_finish_beep.Value

    def on_check_finish_popup(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.finish_popup = self.check_finish_popup_report.Value

    def on_check_finish_batch(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.finish_batch = self.check_finish_run_batch.Value

    def on_text_batchfile(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.finish_batch_file = self.text_batch_file.Value

    def on_check_preprocess(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.crc_preprocess = self.check_preprocess_crc.Value

    def on_text_inkscape_path(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.inkscape_path = self.text_inkscape_path.Value

    def on_button_find_inkscape(
            self, event
    ):  # wxGlade: GeneralSettings.<event_handler>
        self.context.console("inkscape locate\n")
        self.text_inkscape_path.SetValue(self.context.inkscape_path)

    def on_text_inkscape_timeout(
            self, event
    ):  # wxGlade: GeneralSettings.<event_handler>
        self.context.inkscape_timeout = float(self.text_inkscape_timeout.Value)

    def on_check_home_upper_right(
            self, event
    ):  # wxGlade: GeneralSettings.<event_handler>
        self.context.home_right = self.check_home_upper_right.Value

    def on_choice_board(self, event):  # wxGlade: GeneralSettings.<event_handler>
        self.context.board = self.choice_board_name.GetStringSelection()

    def on_text_bed_width(self, event):  # wxGlade: GeneralSettings.<event_handler>
        try:
            self.bed_dim.bed_width = float(self.text_laser_width.Value)
            self.context.signal(
                "bed_size", (self.bed_dim.bed_width, self.bed_dim.bed_height)
            )
        except ValueError:
            pass

    def on_text_bed_height(self, event):  # wxGlade: GeneralSettings.<event_handler>
        try:
            self.bed_dim.bed_height = float(self.text_laser_height.Value)
            self.context.signal(
                "bed_size", (self.bed_dim.bed_width, self.bed_dim.bed_height)
            )
        except ValueError:
            pass

    def on_text_x_factor(self, event):  # wxGlade: GeneralSettings.<event_handler>
        try:
            self.context.x_factor = float(self.text_x_factor.Value)
        except ValueError:
            pass

    def on_text_y_factor(self, event):  # wxGlade: GeneralSettings.<event_handler>
        try:
            self.context.y_factor = float(self.text_y_factor.Value)
        except ValueError:
            pass

    def on_button_save(self, event):  # wxGlade: GeneralSettings.<event_handler>
        pass

# end of class GeneralSettings
