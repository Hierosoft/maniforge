from decimal import Decimal
import math
import re
from maniforge.gcodefollower import GCodeFollower
from maniforge.mfmath import round_nearest

class PressureAdvance:
    def __init__(self, settings):
        self.settings = settings
        self.follower = GCodeFollower()

    def round10(self, value, decimals):
        return round_nearest(value, decimals)

    def fit_width(self):
        pa_count = math.floor((self.settings.pa_end - self.settings.pa_start) / self.settings.pa_step) + 1
        return (self.settings.wall_side_length * self.settings.wall_count + self.settings.pattern_spacing * (pa_count - 1))

    def fit_height(self):
        return self.settings.wall_side_length

    def validate(self):
        validation_fail = False
        errors = []

        # Check numeric inputs
        for key, value in self.settings.to_dict().items():
            if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool):
                if math.isnan(value) or value is None:
                    errors.append(f"{key} is not a valid number.")
                    validation_fail = True

        # Check filename
        if not self.settings.filename or self.settings.filename.strip() == "":
            errors.append("File name cannot be blank.")
            validation_fail = True

        # Check pattern spacing
        if self.settings.pattern_spacing < 1:
            errors.append("Pattern spacing must be at least 1mm.")
            validation_fail = True

        # Check corner angle
        if self.settings.corner_angle > 180:
            errors.append("Pattern angle must be <= 180 degrees.")
            validation_fail = True

        # Check PA range divisibility
        decimals = -self.settings.PA_round
        if not validation_fail:
            pa_range = self.round10(self.settings.pa_end - self.settings.pa_start, self.settings.PA_round)
            pa_step = self.settings.pa_step * math.pow(10, decimals)
            if (pa_range * math.pow(10, decimals)) % pa_step != 0:
                errors.append("PA range cannot be cleanly divided by PA step.")
                validation_fail = True

        # Check PA smooth for Klipper
        if not validation_fail and self.settings.firmware == 'klipper' and self.settings.pa_smooth and self.settings.pa_end > 0.2:
            errors.append("PA smooth cannot exceed 0.2.")
            validation_fail = True

        # Check PA start vs end
        if not validation_fail and self.settings.pa_end - self.settings.pa_start < 0:
            errors.append("PA start value cannot be higher than PA end value.")
            validation_fail = True

        # Check bed size constraints
        if not validation_fail:
            fit_width = self.fit_width()
            fit_height = self.fit_height()
            if self.settings.bed_shape == "Round":
                diameter = math.sqrt(fit_width**2 + fit_height**2)
                if diameter > self.settings.bed_x - 5:
                    errors.append(f"Pattern size (x: {round(fit_width)}, y: {round(fit_height)}) exceeds bed diameter.")
                    validation_fail = True
            else:
                if fit_width > self.settings.bed_x - 5:
                    errors.append(f"Pattern size (x: {round(fit_width)}, y: {round(fit_height)}) exceeds X bed size.")
                    validation_fail = True
                if fit_height > self.settings.bed_y - 5:
                    errors.append(f"Pattern size (x: {round(fit_width)}, y: {round(fit_height)}) exceeds Y bed size.")
                    validation_fail = True

        return not validation_fail, errors

    def generate_gcode(self):
        gcode = []
        state = {
            'cur_x': 0.0,
            'cur_y': 0.0,
            'cur_z': 0.0,
            'retracted': False,
            'hopped': False,
        }

        def add_gcode(cmd, comment=None):
            line = cmd
            if comment:
                line += f" ; {comment}"
            gcode.append(line)

        def move(x=None, y=None, z=None, e=None, f=None, comment=None):
            cmd = ["G1"]
            if x is not None:
                cmd.append(f"X{self.round10(x, self.settings.XY_round)}")
            if y is not None:
                cmd.append(f"Y{self.round10(y, self.settings.XY_round)}")
            if z is not None:
                cmd.append(f"Z{self.round10(z, self.settings.Z_round)}")
            if e is not None:
                cmd.append(f"E{self.round10(e, self.settings.EXT_round)}")
            if f is not None:
                cmd.append(f"F{self.round10(f * 60, 0)}")
            add_gcode(" ".join(cmd), comment)

        def retract():
            if self.settings.fw_retract:
                add_gcode("G10", "retract")
            else:
                move(e=-self.settings.retract_dist, f=self.settings.speed_retract, comment="retract")
            state['retracted'] = True

        def unretract():
            if self.settings.fw_retract:
                add_gcode("G11", "unretract")
            else:
                move(e=self.settings.retract_dist, f=self.settings.speed_unretract, comment="unretract")
            state['retracted'] = False

        def z_hop():
            if self.settings.zhop_enable and not state['hopped']:
                move(z=state['cur_z'] + self.settings.zhop_height, comment="z hop")
                state['hopped'] = True

        def z_unhop():
            if self.settings.zhop_enable and state['hopped']:
                move(z=state['cur_z'], comment="z unhop")
                state['hopped'] = False

        # Start G-code
        add_gcode(self.settings.start_gcode_text(replace=True))

        # Initialize printer
        add_gcode("G90", "absolute positioning")
        if self.settings.acceleration_enable:
            add_gcode(f"M204 S{self.settings.acceleration}", "set acceleration")
        if self.settings.extruder_name_enable and self.settings.extruder_name:
            add_gcode(f"ACTIVATE_EXTRUDER EXTRUDER={self.settings.extruder_name}")
        if self.settings.tool_index != 0:
            add_gcode(f"T{self.settings.tool_index}")

        # Calculate dimensions
        line_width = self.settings.nozzle_diameter * self.settings.line_ratio / 100
        line_width_firstlayer = self.settings.nozzle_diameter * self.settings.anchor_layer_line_ratio / 100
        pa_count = math.floor((self.settings.pa_end - self.settings.pa_start) / self.settings.pa_step) + 1
        bed_x = self.settings.bed_x_value()
        bed_y = self.settings.bed_y_value()
        origin_center = self.settings.origin_center_value()
        start_x = -bed_x / 2 if origin_center else 5
        start_y = -bed_y / 2 if origin_center else 5
        x_offset = start_x + self.settings.wall_side_length / 2
        y_offset = start_y + self.settings.wall_side_length / 2

        # Anchor frame/layer
        if self.settings.anchor_option == "anchor_frame":
            for _ in range(self.settings.anchor_perimeters):
                move(x=x_offset, y=y_offset, f=self.settings.speed_travel, comment="move to start")
                z_unhop()
                move(z=self.settings.height_firstlayer, comment="set first layer height")
                move(x=x_offset + self.settings.wall_side_length, e=line_width_firstlayer * self.settings.ext_mult, f=self.settings.speed_firstlayer, comment="print anchor")
                move(y=y_offset + self.settings.wall_side_length, e=line_width_firstlayer * self.settings.ext_mult, f=self.settings.speed_firstlayer)
                move(x=x_offset, e=line_width_firstlayer * self.settings.ext_mult, f=self.settings.speed_firstlayer)
                move(y=y_offset, e=line_width_firstlayer * self.settings.ext_mult, f=self.settings.speed_firstlayer)
                z_hop()
        elif self.settings.anchor_option == "anchor_layer":
            # Simplified anchor layer (full implementation requires complex path planning)
            pass  # Placeholder for anchor layer logic

        # Main pattern
        for layer in range(self.settings.num_layers):
            z = self.settings.height_firstlayer if layer == 0 else self.settings.height_firstlayer + (layer * self.settings.height_layer)
            move(z=z, comment=f"move to layer {layer + 1}")
            for pa_index in range(pa_count):
                pa_value = self.settings.pa_start + pa_index * self.settings.pa_step
                if self.settings.firmware == 'klipper':
                    add_gcode(f"SET_PRESSURE_ADVANCE ADVANCE={self.round10(pa_value, self.settings.PA_round)}")
                elif self.settings.firmware in ['marlin1_1_9', 'marlin1_1_8']:
                    add_gcode(f"M900 K{self.round10(pa_value, self.settings.PA_round)}")
                if self.settings.echo:
                    add_gcode(f"M117 PA {self.round10(pa_value, self.settings.PA_round)}")
                x_start = x_offset + pa_index * (self.settings.wall_side_length * self.settings.wall_count + self.settings.pattern_spacing)
                for wall in range(self.settings.wall_count):
                    x_wall = x_start + wall * self.settings.wall_side_length
                    move(x=x_wall, y=y_offset, f=self.settings.speed_travel, comment="move to pattern start")
                    z_unhop()
                    move(x=x_wall + self.settings.wall_side_length, e=line_width * self.settings.ext_mult, f=self.settings.speed_perimeter, comment="print wall")
                    move(y=y_offset + self.settings.wall_side_length, e=line_width * self.settings.ext_mult, f=self.settings.speed_perimeter)
                    move(x=x_wall, e=line_width * self.settings.ext_mult, f=self.settings.speed_perimeter)
                    move(y=y_offset, e=line_width * self.settings.ext_mult, f=self.settings.speed_perimeter)
                    z_hop()

        # End G-code
        add_gcode(self.settings.end_gcode_text())

        return "\n".join(gcode)
