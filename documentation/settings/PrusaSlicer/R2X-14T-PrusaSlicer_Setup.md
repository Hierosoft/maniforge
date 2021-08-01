### PrusaSlicer Setup

#### Add the printer
If you only need one printer, overwrite your PrusaSlicer directory in %APPDATA% (or in .config in GNU+Linux systems) with the included config/PrusaSlicer directory (See [readme.md](../readme.md)).
- Next, choose the path to the print bed texture if necessary: See "Apply a Bed Texture" in the [manual](../../manual.md).

To add an additional printer instead, complete all of the steps in the "Add it as an additional printer" section.

##### Add it as an additional printer
- Click the "Printer Settings" tab
- Click the drop-down box that contains the printer name and choose "Add/Remove Printers"
- Choose "Custom Printer" on the left.
- Check "Define a custom printer profile"
- Name it "R2X 14T"
- Click "Next"
- For "Firmware Type" choose "Marlin".
- Click "Next"
- In "Bed Shape and Size" use the following settings:
  - Size:  x:236  y:153
  - Origin:  x:0  y:0
  - For the texture, choose a texture if desired (See "Apply a Bed Texture" in the [manual](../../manual.md)).
- Click "Next"
- Set the values to match your nozzle and filament, such as:
  - Nozzle Diameter: 0.4
  - Filament Diameter: 1.75
- Click "Next
- For "Nozzle and Bed Temperatures" you can choose whatever is convenient and override it in material settings. For the recommended bed temperature, see the materials chart that came with your FilaPrint bed surface. For now, set:
  - For ABS: Extrusion:220C, Bed:110C (For FilaPrint, FilaFarm recommends 105C)
  - For PLA: Extrusion:210C, Bed:90C (For FilaPrint, FilaFarm recommends 92C)
- Click "Next"
- For Filament Profiles, choose "(All)" printers and "(All)" types, then click "All" under Profile.
- Click "Next"
- For the update settings, leave the boxes checked or unchecked as desired then press "Next".
- Check "Export full pathnames of models and parts sources into 3mf and amf files" to avoid hassles--you can uncheck the option later before exporting models for sharing.
- Click "Next"
- Choose "Expert mode" to make all settings visible. Only check "Use inches" if your engineering software is used with inches as the units and you will mostly be printing your own models. Otherwise, leave it unchecked for compatibility with downloaded models without scaling them.
- Click "Finish".

###### Add filaments
Next you must detach the printer definition from the Generic FFF Printer to be able to select built-in filaments (See [Custom Printer Profile and the Filament List](https://forum.prusaprinters.org/forum/prusaslicer/custom-printer-profile-and-the-filament-list/) (matches instructions below), [BUG REPORT: Prusa 2.2.0 does not show Filaments tab in Configuration Assistant](https://forum.prusaprinters.org/forum/prusaslicer/prusa-2-2-0-does-not-show-filaments-tab-in-configuration-assistant/) or [Filament settings disappeared on upgrade](https://github.com/prusa3d/PrusaSlicer/issues/3934)).
- Close any copies of PrusaSlicer.
- Open a text editor such as Notepad++ or Geany.
- File, Open
  - Navigate to `%APPDATA%` (or ~/.config on GNU+Linux systems).
  - Open your printer's ini file such as `PrusaSlicer/printer/Axle Media R2X 14T.ini`
  - Change `inherits = ` to `inherits = Original Prusa i3 MK3S`.
  - Ensure that the `printer_notes` variable is set to nothing (`printer_notes =`) so that it doesn't contain "PRINTER_HAS_BOWDEN" which is a value in the field used by the filament-specific Start G-code in various filament profiles to behave differently.
- Open PrusaSlicer
- Go to the "Printer Settings" tab
  - In "General", set:
    - Max print height: 150
    - Extruders: 2
    - Leave "Single Extruder Multi Material" unchecked.
  - In "Extruder 1" set:
    - Retraction:
      - Length: 0.5
  - In "Extruder 2" set all of the settings from "Extruder 1" above plus:
    - Extruder offset: x:34 y:0
  - In "Custom G-code":
    - For "Start G-code" paste the contents of [start.gcode](start.gcode)
    - For "End G-code" paste the contents of [end.gcode](end.gcode)

Now you can add new filaments or tweak the settings for direct drive, such as:
- Go to "Filament Settings"
- Choose "Generic ABS"
- In the "Filament" panel, set (only numbers, no symbols or units):
  - Nozzle temperatures to "220"
  - Density: `1.04` g/cm^3
  - Cost: `21.99` money/kg
  - Spool weight: `1000` g
  - Leave the other settings at their defaults (Color [or change it to your color], Bed temperatures: `110`, Diameter: `1.75`
- If you have used the exact values above, you can enter the following in the Notes tab (calculated by Cura):
  ```
Based on 1.75dia, $21.99/kg, Spool Weight 1000g, 1.04 g/cm^3, Cura calculates:
- Filament length: ~ 400 m
- Cost per Meter: ~ 0.06 $/m
```
- In the "Dependencies" tab:
  - Click "Detach from system preset".
  - Clear the "Compatible printers condition" field.
- On the right of the "Generic ABS (modified)" material name, click the save button, and name it: "MakerBot ABS"
- If you repeat the steps for each filament you want (especially clearing the "Compatible printers condition" field), you can hide the rest:
  - Go to the "Printer Settings" tab. In "Dependencies", click "Detach from system present".

