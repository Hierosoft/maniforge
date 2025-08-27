import wx
import wx.glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from maniforge.slicerpreset import SlicerPreset
from maniforge.slicerpresets import SlicerPresets
from maniforge.pressureadvance import PressureAdvance
import sys

class GCodeCanvas(wx.glcanvas.GLCanvas):
    def __init__(self, parent):
        attribs = [wx.glcanvas.WX_GL_RGBA, wx.glcanvas.WX_GL_DOUBLEBUFFER, wx.glcanvas.WX_GL_DEPTH_SIZE, 16]
        super().__init__(parent, attribList=attribs)
        self.context = wx.glcanvas.GLContext(self)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.points = []
        self.colors = []

    def set_gcode(self, gcode):
        self.points = []
        self.colors = []
        current_pos = [0.0, 0.0, 0.0]
        last_pos = [0.0, 0.0, 0.0]
        for line in gcode.split('\n'):
            line = line.strip()
            if line.startswith('G1'):
                parts = line.split()
                x = y = z = None
                for part in parts[1:]:
                    if part.startswith('X'):
                        x = float(part[1:])
                    elif part.startswith('Y'):
                        y = float(part[1:])
                    elif part.startswith('Z'):
                        z = float(part[1:])
                    elif part.startswith('E'):
                        e = float(part[1:])
                        if e > 0:
                            self.points.append(last_pos[:])
                            self.points.append([x if x is not None else last_pos[0],
                                               y if y is not None else last_pos[1],
                                               z if z is not None else last_pos[2]])
                            self.colors.append([1.0, 0.0, 0.0, 1.0])
                            self.colors.append([1.0, 0.0, 0.0, 1.0])
                if x is not None:
                    current_pos[0] = x
                if y is not None:
                    current_pos[1] = y
                if z is not None:
                    current_pos[2] = z
                last_pos = current_pos[:]
        self.Refresh()

    def init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.GetClientSize()[0] / self.GetClientSize()[1], 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, -50, 50, 0, 0, 0, 0, 0, 1)

    def on_paint(self, event):
        self.SetCurrent(self.context)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.init_gl()
        glBegin(GL_LINES)
        for i, point in enumerate(self.points):
            glColor4fv(self.colors[i])
            glVertex3f(point[0], point[1], point[2])
        glEnd()
        self.SwapBuffers()

    def on_resize(self, event):
        self.SetCurrent(self.context)
        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)
        self.Refresh()

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Pressure Advance Calibration Tool", size=(1200, 800))
        self.settings = SlicerPreset()
        self.presets = SlicerPresets()
        self.generator = PressureAdvance(self.settings)
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left side: Settings
        self.settings_sizer = wx.BoxSizer(wx.VERTICAL)
        self.create_settings_controls()
        self.sizer.Add(self.settings_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Right side: Preview and G-code
        self.preview_sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas = GCodeCanvas(self.panel)
        self.preview_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        self.gcode_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.preview_sizer.Add(self.gcode_text, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.preview_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(self.sizer)
        self.validate_and_update()
        self.Centre()

    def create_settings_controls(self):
        # Presets
        self.presets_combo = wx.ComboBox(self.panel, choices=self.presets.get_presets())
        self.presets_combo.Bind(wx.EVT_COMBOBOX, self.on_preset_select)
        self.settings_sizer.Add(wx.StaticText(self.panel, label="Presets"), 0, wx.ALL, 5)
        self.settings_sizer.Add(self.presets_combo, 0, wx.EXPAND | wx.ALL, 5)

        # Filename
        self.filename_ctrl = wx.TextCtrl(self.panel)
        self.auto_filename_ctrl = wx.CheckBox(self.panel, label="Auto Filename")
        self.auto_filename_ctrl.SetValue(self.settings.auto_filename)
        self.filename_ctrl.Bind(wx.EVT_TEXT, self.on_field_change)
        self.auto_filename_ctrl.Bind(wx.EVT_CHECKBOX, self.on_auto_filename)
        self.settings_sizer.Add(wx.StaticText(self.panel, label="File Name"), 0, wx.ALL, 5)
        self.settings_sizer.Add(self.filename_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        self.settings_sizer.Add(self.auto_filename_ctrl, 0, wx.ALL, 5)

        # Settings fields
        fields = [
            ("Firmware", "firmware", ["klipper", "marlin1_1_9", "marlin1_1_8", "rrf3"], wx.Choice),
            ("Bed Shape", "bed_shape", ["Rect", "Round"], wx.Choice),
            ("Nozzle Diameter (mm)", "nozzle_diameter", float),
            ("Bed Size X (mm)", "bed_x", float),
            ("Bed Size Y (mm)", "bed_y", float),
            ("Extrusion Multiplier", "ext_mult", float),
            ("Travel Speed (mm/s)", "speed_travel", float),
            ("Extruder Name", "extruder_name", str),
            ("Tool Index", "tool_index", int),
            ("Origin Bed Center", "origin_center", bool, wx.CheckBox),
            ("Retract Distance (mm)", "retract_dist", float),
            ("Z Hop", "zhop_enable", bool, wx.CheckBox),
            ("Retract Speed (mm/s)", "speed_retract", float),
            ("Z Hop Height (mm)", "zhop_height", float),
            ("Unretract Speed (mm/s)", "speed_unretract", float),
            ("Use Firmware Retraction", "fw_retract", bool, wx.CheckBox),
            ("First Layer Height (mm)", "height_firstlayer", float),
            ("Anchor Option", "anchor_option", ["anchor_frame", "anchor_layer", "no_anchor"], wx.Choice),
            ("First Layer Print Speed (mm/s)", "speed_firstlayer", float),
            ("Anchor Line Width (%)", "anchor_layer_line_ratio", float),
            ("First Layer Fan Speed (%)", "fan_speed_firstlayer", float),
            ("Anchor Frame Perimeters", "anchor_perimeters", int),
            ("Line Width (%)", "line_ratio", float),
            ("Layer Count", "num_layers", int),
            ("Print Speed (mm/s)", "speed_perimeter", float),
            ("Layer Height (mm)", "height_layer", float),
            ("Acceleration (mm/s^2)", "acceleration", float),
            ("Acceleration Enable", "acceleration_enable", bool, wx.CheckBox),
            ("Fan Speed (%)", "fan_speed", float),
            ("Wall Count", "wall_count", int),
            ("Corner Angle (°)", "corner_angle", float),
            ("Side Length (mm)", "wall_side_length", float),
            ("Printing Direction (°)", "print_dir", ["0", "45", "90", "135", "180", "225", "270", "315"], wx.Choice),
            ("Spacing (mm)", "pattern_spacing", float),
            ("PA Start Value", "pa_start", float),
            ("PA End Value", "pa_end", float),
            ("PA Increment", "pa_step", float),
            ("Increment Smooth Time Instead", "pa_smooth", bool, wx.CheckBox),
            ("Number Tab", "use_lineno", bool, wx.CheckBox),
            ("No Leading Zeroes", "lineno_no_leading_zero", bool, wx.CheckBox),
            ("Show on LCD", "echo", bool, wx.CheckBox),
            ("Bed Temp (°C)", "bed_temp", float),
            ("Don't Add G28", "start_gcode_no_homing", bool, wx.CheckBox),
            ("Hotend Temp (°C)", "hotend_temp", float),
            ("Don't Add Heating G-Codes", "start_gcode_no_heating", bool, wx.CheckBox),
            ("Start G-code", "start_gcode", str, wx.TextCtrl, wx.TE_MULTILINE),
            ("End G-code", "end_gcode", str, wx.TextCtrl, wx.TE_MULTILINE),
        ]

        for label, attr, type_or_choices, *control_args in fields:
            control_type = control_args[0] if control_args else wx.TextCtrl
            style = control_args[1] if len(control_args) > 1 else 0
            self.create_setting_field(label, attr, type_or_choices, control_type, style)

        # Save button
        self.save_button = wx.Button(self.panel, label="Save G-code")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        self.settings_sizer.Add(self.save_button, 0, wx.ALL, 5)

    def create_setting_field(self, label, attr, type_or_choices, control_type=wx.TextCtrl, style=0):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self.panel, label=label), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        if control_type == wx.CheckBox:
            ctrl = wx.CheckBox(self.panel)
            ctrl.SetValue(getattr(self.settings, attr))
            ctrl.Bind(wx.EVT_CHECKBOX, lambda evt: self.on_field_change(evt, attr, bool))
        elif control_type == wx.Choice:
            ctrl = wx.Choice(self.panel, choices=type_or_choices)
            ctrl.SetStringSelection(str(getattr(self.settings, attr)))
            ctrl.Bind(wx.EVT_CHOICE, lambda evt: self.on_field_change(evt, attr, str))
        else:
            if attr in ['start_gcode', 'end_gcode']:
                style = wx.TE_MULTILINE
            ctrl = wx.TextCtrl(self.panel, value=str(getattr(self.settings, attr)), style=style)
            ctrl.Bind(wx.EVT_TEXT, lambda evt: self.on_field_change(evt, attr, type_or_choices))
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)
        self.settings_sizer.Add(sizer, 0, wx.EXPAND | wx.ALL, 5)
        setattr(self, f"{attr}_ctrl", ctrl)

    def on_field_change(self, event, attr=None, type_cast=float):
        if attr:
            if isinstance(event.GetEventObject(), wx.Choice):
                value = event.GetString()
            else:  # wx.TextCtrl or wx.CheckBox
                value = event.GetEventObject().GetValue()
            if type_cast == bool:
                value = bool(value)
            elif type_cast != str:
                try:
                    value = type_cast(value)
                except ValueError:
                    value = None
            setattr(self.settings, attr, value)
        if self.auto_filename_ctrl.GetValue():
            self.update_filename()
        self.validate_and_update()

    def on_auto_filename(self, event):
        self.settings.auto_filename = self.auto_filename_ctrl.GetValue()
        if self.settings.auto_filename:
            self.update_filename()
        self.validate_and_update()

    def update_filename(self):
        new_filename = self.settings.generate_filename()
        if self.filename_ctrl.GetValue() == new_filename:
            return
        self.filename_ctrl.Unbind(wx.EVT_TEXT)
        self.filename_ctrl.SetValue(new_filename)
        self.filename_ctrl.Bind(wx.EVT_TEXT, self.on_field_change)

    def on_preset_select(self, event):
        preset_name = self.presets_combo.GetStringSelection()
        if preset_name:
            self.settings = self.presets.load_preset(preset_name)
            self.update_controls()
            self.validate_and_update()

    def update_controls(self):
        for attr in self.settings.to_dict().keys():
            ctrl = getattr(self, f"{attr}_ctrl", None)
            if ctrl:
                if isinstance(ctrl, wx.TextCtrl):
                    ctrl.Unbind(wx.EVT_TEXT)
                    ctrl.SetValue(str(getattr(self.settings, attr)))
                    ctrl.Bind(wx.EVT_TEXT, lambda evt: self.on_field_change(evt, attr, type(ctrl)))
                elif isinstance(ctrl, wx.Choice):
                    ctrl.Unbind(wx.EVT_CHOICE)
                    ctrl.SetStringSelection(str(getattr(self.settings, attr)))
                    ctrl.Bind(wx.EVT_CHOICE, lambda evt: self.on_field_change(evt, attr, str))
                elif isinstance(ctrl, wx.CheckBox):
                    ctrl.Unbind(wx.EVT_CHECKBOX)
                    ctrl.SetValue(getattr(self.settings, attr))
                    ctrl.Bind(wx.EVT_CHECKBOX, lambda evt: self.on_field_change(evt, attr, bool))

    def on_save(self, event):
        default_dir = os.path.expanduser("~/gcode/tests")
        if not os.path.exists(default_dir):
            default_dir = os.path.expanduser("~/gcode")
        if not os.path.exists(default_dir):
            default_dir = os.path.expanduser("~")
        with wx.FileDialog(self, "Save G-code file", defaultDir=default_dir,
                           defaultFile=f"{self.settings.filename}.gcode",
                           wildcard="G-code files (*.gcode)|*.gcode",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_OK:
                path = fileDialog.GetPath()
                with open(path, 'w') as f:
                    f.write(self.gcode_text.GetValue())
                self.presets.save_preset(self.settings, path)

    def validate_and_update(self):
        valid, errors = self.generator.validate()
        self.save_button.Enable(valid)
        gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
        self.gcode_text.SetValue(gcode)
        self.canvas.set_gcode(gcode)
