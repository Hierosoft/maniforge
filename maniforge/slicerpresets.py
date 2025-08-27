import os
import json
from maniforge.slicerpreset import SlicerPreset

class SlicerPresets:
    def __init__(self):
        self.preset_dir = os.path.expanduser('~/.config/maniforge/presets')
        os.makedirs(self.preset_dir, exist_ok=True)

    def save_preset(self, settings, filename):
        preset_path = os.path.join(self.preset_dir, filename.replace('.gcode', '.json'))
        settings.save_to_file(preset_path)

    def load_preset(self, preset_name):
        preset_path = os.path.join(self.preset_dir, preset_name)
        settings = SlicerPreset()
        settings.load_from_file(preset_path)
        return settings

    def get_presets(self):
        return [f for f in os.listdir(self.preset_dir) if f.endswith('.json')]
