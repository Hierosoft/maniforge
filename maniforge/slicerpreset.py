import json
import os
from decimal import Decimal

class SlicerPreset:
    PA_round = -4
    Z_round = -3
    XY_round = -4
    EXT_round = -5
    GLYPH_PADDING_HORIZONTAL = 1
    GLYPH_PADDING_VERTICAL = 1
    ENCROACHMENT = 1/3

    START_GCODES = {
        'klipper': """
            PRINT_START ; Start macro
            ; START_PRINT ; Start macro (alternate / official start macro name)
        """,
        'rrf3': """
            G28                 ; Home all axes
            G90                 ; Absolute XYZ
            G1 Z5 F100          ; Z raise
            M190 S[BED_TEMP]    ; Set & wait for bed temp.
            M109 S[HOTEND_TEMP] ; Set & wait for hotend temp.
            G32                 ; Run bed.g macro
            G28 Z               ; Home Z
        """,
        'marlin1_1_9': """
            G28                 ; Home all axes
            G90                 ; Absolute XYZ
            G1 Z5 F100          ; Z raise
            M190 S[BED_TEMP]    ; Set & wait for bed temp
            M109 S[HOTEND_TEMP] ; Set & wait for hotend temp
            ;G29                ; Auto bed leveling
        """,
        'marlin1_1_8': """
            G28                 ; Home all axes
            G90                 ; Absolute XYZ
            G1 Z5 F100          ; Z raise
            M190 S[BED_TEMP]    ; Set & wait for bed temp
            M109 S[HOTEND_TEMP] ; Set & wait for hotend temp
            ;G29                ; Auto bed leveling
        """
    }

    END_GCODES = {
        'klipper': "PRINT_END ; End macro. Change name to match yours",
        'rrf3': "M0 ; Stop",
        'marlin1_1_9': "M501 ; Load settings from EEPROM (to restore previous values)",
        'marlin1_1_8': "M501 ; Load settings from EEPROM (to restore previous values)"
    }

    def __init__(self):
        self.settings_version = 3
        self.acceleration = 750
        self.acceleration_enable = False
        self.anchor_layer_line_ratio = 140
        self.anchor_option = "anchor_frame"
        self.anchor_perimeters = 4
        self.bed_shape = "Rect"
        self.bed_temp = 60
        self.bed_x = 200
        self.bed_y = 200
        self.corner_angle = 90
        self.echo = True
        self.end_gcode = ""
        self.expert_mode = False
        self.ext_mult = 0.98
        self.extruder_name = ""
        self.extruder_name_enable = False
        self.fan_speed = 100
        self.fan_speed_firstlayer = 0
        self.filament_diameter = 1.75
        self.filename = "pa_pattern"
        self.firmware = "klipper"
        self.fw_retract = False
        self.height_firstlayer = 0.25
        self.height_layer = 0.2
        self.hotend_temp = 200
        self.line_ratio = 112.5
        self.lineno_no_leading_zero = False
        self.nozzle_diameter = 0.4
        self.num_layers = 4
        self.origin_center = False
        self.pa_end = 0.08
        self.pa_smooth = False
        self.pa_start = 0
        self.pa_step = 0.005
        self.pattern_options_enable = False
        self.pattern_spacing = 2
        self.print_dir = 0
        self.printer = None
        self.retract_dist = 0.5
        self.speed_firstlayer = 30
        self.speed_perimeter = 100
        self.speed_retract = 35
        self.speed_travel = 120
        self.speed_unretract = 35
        self.start_gcode = ""
        self.start_gcode_no_heating = False
        self.start_gcode_no_homing = False
        self.tool_index = 0
        self.use_lineno = True
        self.wall_count = 3
        self.wall_side_length = 30.0
        self.zhop_enable = True
        self.zhop_height = 0.1
        self.auto_filename = True

    def to_dict(self):
        return {key: value for key, value in vars(self).items() if not key.startswith('_')}

    def from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save_to_file(self, path):
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def load_from_file(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                if data.get('settings_version') == self.settings_version:
                    self.from_dict(data)

    def start_gcode_text(self, replace=False):
        gcode = self.start_gcode or self.START_GCODES[self.firmware]
        gcode = gcode.strip()
        if not replace:
            return gcode
        # Process line by line to avoid regex recursion issues
        lines = gcode.split('\n')
        filtered_lines = []
        for line in lines:
            stripped_line = line.strip()
            if not (stripped_line.startswith('M104 S0') or stripped_line.startswith('M140 S0') or stripped_line.startswith('M109 S0') or stripped_line.startswith('M190 S0')):
                filtered_lines.append(line)
        gcode = '\n'.join(filtered_lines)
        lines = gcode.split('\n')  # Update lines after filtering
        if not self.start_gcode_no_heating:
            if '[HOTEND_TEMP]' not in gcode:
                if not any(line.strip().startswith('G28') and not line.strip().lstrip('G28').strip().startswith('Z') for line in lines):
                    gcode = f"M109 S[HOTEND_TEMP] ; Set & wait for hotend temp\n{gcode}"
                else:
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if line.strip().startswith('G28') and not line.strip().lstrip('G28').strip().startswith('Z'):
                            new_lines.append("M109 S[HOTEND_TEMP] ; Set & wait for hotend temp")
                    gcode = '\n'.join(new_lines)
            if '[BED_TEMP]' not in gcode:
                if not any(line.strip().startswith('G28') and not line.strip().lstrip('G28').strip().startswith('Z') for line in lines):
                    gcode = f"M190 S[BED_TEMP] ; Set & wait for bed temp\n{gcode}"
                else:
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if line.strip().startswith('G28') and not line.strip().lstrip('G28').strip().startswith('Z'):
                            new_lines.append("M190 S[BED_TEMP] ; Set & wait for bed temp")
                    gcode = '\n'.join(new_lines)
        if not self.start_gcode_no_homing and not any(line.strip().startswith('G28') and not line.strip().lstrip('G28').strip().startswith('Z') for line in lines):
            gcode = f"G28 ; Home all axes\n{gcode}"
        return (gcode
                .replace('[HOTEND_TEMP]', str(self.hotend_temp))
                .replace('[BED_TEMP]', str(self.bed_temp))
                .replace('[EXTRUDER_NAME]', self.extruder_name)
                .replace('[TOOL_INDEX]', str(self.tool_index))
                .replace('{first_layer_temperature}', str(self.hotend_temp))
                .replace('[first_layer_temperature]', str(self.hotend_temp))
                .replace('{first_layer_bed_temperature}', str(self.bed_temp))
                .replace('[first_layer_bed_temperature]', str(self.bed_temp))
                .replace('{chamber_temperature}', '0')
                .replace('[chamber_temperature]', '0')
                .replace('{nozzle_temperature_initial_layer}', str(self.hotend_temp))
                .replace('[nozzle_temperature_initial_layer]', str(self.hotend_temp))
                .replace('{bed_temperature_initial_layer_single}', str(self.bed_temp))
                .replace('[bed_temperature_initial_layer_single]', str(self.bed_temp))
                .replace('{material_print_temperature}', str(self.hotend_temp))
                .replace('{material_bed_temperature}', str(self.bed_temp))
                .replace('{build_volume_temperature}', '0')
                .strip())

    def end_gcode_text(self):
        return (self.end_gcode or self.END_GCODES[self.firmware]).strip()

    def bed_x_value(self):
        return self.bed_x

    def bed_y_value(self):
        return self.bed_x if self.bed_shape == "Round" else self.bed_y

    def origin_center_value(self):
        return self.bed_shape == "Round"

    def generate_filename(self):
        bed_y = self.bed_y if self.bed_shape != "Round" else self.bed_x
        return (f"pa_pattern-{self.bed_x}x{bed_y}-"
                f"{self.hotend_temp}C-{self.bed_temp}C@"
                f"{self.speed_firstlayer}-{self.speed_perimeter}mms-"
                f"{self.pa_start}to{self.pa_end}-step{self.pa_step}-"
                f"r{self.retract_dist}at{self.speed_retract}")
