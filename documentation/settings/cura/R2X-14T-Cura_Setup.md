### Cura Setup

#### Add the printer
If you only need one printer, overwrite your cura directory in %APPDATA% (or in .config in GNU+Linux systems) with the included config/cura directory (See [readme.md](../../../readme.md)).

To add an additional printer instead, complete all of the steps in the "Add it as an additional printer" section.

##### Add it as an additional printer
- Preferences, Configure Cura
  - Printers, Add
    - Add a non-networked printer
    - In the "Custom" category choose "Custom FFF Printer" then click Add.
    - Paste the contents of [documentation/settings/cura/start.gcode](start.gcode) into the "Start G-code" field.
    - Paste the contents of [documentation/settings/cura/end.gcode](end.gcode) into the "End G-code" field.
    - Fill out the additional sections using the information below:

Printer Settings:
- W (Width): 236
- Y (Depth): 129
- Z (Height): 150
- Build Plate Shape: Rectangular
- Origin at center: False
- Heated be: True
- Heated build volume: False
- G-code flavor: Marlin

Printhead Settings:
(The settings above allow leaving the hotend assembly size at 0.)
- The hotend assembly values below may not stick at first, but enter them sequentially and they should all change by the time you move on from the last one and click another field.
  - X min: 0
  - Y min: 0
  - X max: 0
  - Y max: 0
- Gantry Height: 150
- Number of Extruders: 2
- Apply Extruder offsets to GCode: True

Extruder 1:
Nozzle size: 0.4
Compatible material diameter: 1.75
Nozzle offset X: 0.0
Nozzle offset Y: 0.0
Cooling Fan Number: 0

Extruder 2:
Nozzle size: 0.4
Compatible material diameter: 1.75
Nozzle offset X: 34.0
Nozzle offset Y: 0.0
Cooling Fan Number: 0


- After adding these settings in the "Add Printer" window, click "Next" to save the printer.
- Ensure "Custom FF Printer" is highlighted, then click "Rename"
- Name it "R2X 14T", OK

Using OctoPrint with Cura (optional):
If your 3D Printer is connected to an OctoPrint server, continue the steps below in the same panel (the "Printers" panel in the Preferences window).
- Ensure "R2X 14T" is setup according to the instructions above then highlight it.
- Click "Connect to OctoPrint"
- Choose or add the IP address.
  - Click "Request" to request an API key.
  - Log in on your OctoPrint web interface and get the API key.
  - Paste the API key into the program.
  - Check "Start print job after uploading"
  - Set other options as desired.
  - Close
  - If you have a webcam connected to the OctoPrint server and don't see the video capture under "Monitor"
    - Restart the OctoPrint server whenever you unplug the webcam and re-insert it. See:
      - <https://github.com/jacksonliam/mjpg-streamer/issues/246>
      - <https://github.com/FormerLurker/Octolapse/issues/501>
    - If it never worked before, ensure you first configure the OctoPrint server to show the video capture on the web interface (If not, use the OctoPrint documentation and forums to correct the problem).

Import the Material(s):
- Preferences, Configure Cura
- Choose "Materials" on the left.
- Import, navigate to your copy of the r2x_14t repo, then choose the material file from documentation, settings, cura, materials, then the directory matching your version or the most recent version. If import fails, select the Generic material of the same type (such as Generic ABS), click Create, then enter the settings such as from [documentation/settings/cura/materials/MakerBot_ABS.md](materials/MakerBot_ABS.md) or another md file in that directory.
- Repeat the step above for each additional material there if any.
- In the category matching the filament brand such as "MakerBot", highlight the material you want to use, then Click Activate.
- For every material you import, you can also click the star by it to make the outlined star filled to add it to favorites so that you can find it at the top of the list rather than inside of a category.

Import the Profile(s):
(The printing profiles are specific quality settings but may require that you install the printer and material(s) above first since some of the settings cascade down from those global settings unless the printing profile overrides them.)
- Preferences, Configure Cura
- Choose "Profiles" on the left.
- Import, navigate to your copy of the r2x_14t repo, then choose the material file from documentation, settings, cura, profiles, then the directory matching your version or the most recent version.
- Repeat the step above for each additional profile there if any.
- Click the profile you want to use then click "Activate" (or Close the Preferences window then choose the printing profile from the list in the custom panel on the right at any time).
