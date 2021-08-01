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
  - For ABS: Extrusion:220C, Bed:110C
  - For PLA: Extrusion:210C, Bed:90C (92 is recommended for FilaPrint)
- Click "Next"
- For Filament Profiles, choose "(All)" printers and "(All)" types, then click "All" under Profile.
- Click "Next"
- For the update settings, leave the boxes checked or unchecked as desired then press "Next".
- Check "Export full pathnames of models and parts sources into 3mf and amf files" to avoid hassles--you can uncheck the option later before exporting models for sharing.
- Click "Next"
- Choose "Expert mode" to make all settings visible. Only check "Use inches" if your engineering software is used with inches as the units and you will mostly be printing your own models. Otherwise, leave it unchecked for compatibility with downloaded models without scaling them.
- Click "Finish".
