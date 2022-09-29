# R2X 14T

Never again manually scrub through comparisons of the Configuration.h and Configuration_adv.h. Instead, shove metadata into H files of any structure using Python `deploy-marlin` (or the marlininfo Python module).

The R2X 14T is a mod by Jake Gustafson ("Poikilos") for the *MakerBot Replicator 2X* (possibly compatible with clones such as FlashForge Creator Pro). The name "Axle Media" is a registered fictitious name in Pennsylvania and should be only used if the mod is done by Jake Gustafson.

The mod utilizes the BIGTREETECH SKR V1.4 Turbo and most of the hardware from the MakerBot Replicator 2X. The fork of Marlin 2.0 ([https://github.com/poikilos/Marlin/tree/bugfix-2.0.x-r2x_t14](https://github.com/poikilos/Marlin/tree/bugfix-2.0.x-r2x_t14)) only contains changes to platformio.ini, Configuration.h, and Configuration_adv.h.

For usage and further details, see the Service Manual: [documentation/manual.md](https://github.com/poikilos/r2x_14t/blob/main/documentation/manual.md).


## How to use
If you are not compiling Marlin nor flashing/configuring a TFT, you can still use this project. See:
- [documentation/settings.md](documentation/settings.md)
- [config](config) for Slicer settings files
- [config/screens](config/screens) for screen configurations
- See also "[Hardware Changes](#hardware-changes)" below.

If you are compiling Marlin:

Using the deploy-marlin command, you don't need my (or anyone else's) versioned H files anymore! You can generate a modified H file from the originals! Steps:
- Go to a terminal
- run `python3 -m pip install --user https://github.com/poikilos/pycodetool/archive/refs/heads/master.zip`
- cd to your copy of Marlin that you want to modify (See "Configure Marlin"). Make a copy of it (you only have to copy the Configuration.h and Configuration_adv.h). Rename the folder to Marlin-R2X_14T so that the deploy script will auto-detect that it is R2X_14T not JGAURORA A3S or some other 3D printer (You can also add the option `--machine R2X_14T` instead).
- cd to the folder containing the copies you made.
- install meld and ensure it is in your system's PATH (so it can be run with `meld` in Terminal without a full path)
- run your copy of deploy-marlin using the full path such as: `python3 /home/owner/git/r2x_14t/deploy-marlin ~/git/Marlin`
  - where ~/git/Marlin is (the real Marlin, not the copy--where you want to compile). Follow additional instructions on screen if there are any issues.
- Meld should launch. If it doesn't, ensure it is installed and in the system or user PATH. You can also view the meld command that was displayed and compare those directories yourself. Potentially, you can just copy the files from the first directory to the next.
- A manual step still necessary for R2X_14T (or BTT boards in general): in platformio.ini, change the default_envs line to `default_envs = LPC1769`

### Configure Marlin
- Clone Marlin then switch to the bugfix branch (as per
hallski's Nov 23 '09 at 14:26 answer edited Dec 19, '21 <https://stackoverflow.com/a/1783426> on <https://stackoverflow.com/questions/1783405/how-do-i-check-out-a-remote-git-branch>):
```
mkdir ~/git
cd ~/git
git clone https://github.com/poikilos/r2x_14t
git clone https://github.com/MarlinFirmware/Marlin.git
cd Marlin
git switch bugfix-2.0.x
```
- Ensure you are on a Marlin bugfix-2.0.x subversion that says the same CONFIGURATION_H_VERSION in Marlin/Marlin/configuration.h as in r2x_14t/Marlin-R2X_14T/Marlin (The exact version on which that was based is in r2x_14t/Marlin-base/Marlin, which, if you have the same commit as noted in the r2x_14t git commit Summary, will match the one in Marlin exactly as checked via `./meld-both-with-Marlin-bugfix-2.0.x.sh` in a GNU+Linux OS).
  - However, this isn't critical anymore using the `deploy-marlin` script. If the version doesn't match, you can just merge changes manually now (requires meld).

You are probably done if you followed the steps this far. See "How to Use" to use `deploy-marlin` instead of manually editing files. If you are having trouble with the deploy script and your CONFIGURATION_H_VERSION matches the Marlin-R2X_14T directory, you can do it the old way: The safest way is using [Meld](https://meldmerge.org/): `meld ./Marlin-R2X_14T/ ../Marlin`. If you are sure the versions match, you may be able to copy all files from r2x_14t/Marlin-R2X_14T to Marlin (ensure that you confirm overwrite, or you may not have copied to the correct directory). On a GNU+Linux system that would be done via: `rsync -rt ./Marlin-R2X_14T/ ../Marlin` (On Windows via `pushconfig.bat`).

### Build and Install Marlin
- Complete the steps above ("Configure Marlin").
- Install the PlatformIO plugin for Visual Studio Code.
- In the PlatformIO tab, click "Open Project" then choose the "Marlin" directory (not "Marlin\Marlin") that you configured.
- Click the PlatformIO button on the left. Choose the "LPC1769" board (for BTT SKR V1.4 TURBO).
  - Under that, click "build" (Correct any errors. Report them at <https://github.com/poikilos/r2x_14t> if you made no changes to the configuration here).
    - (or "upload and monitor" if you have the device connected, but if that fails to upload, continue below)
  - Copy the firmware.bin file (location is shown in the output, such as `C:\Users\Jatlivecom\git\Marlin\.pio\build\LPC1769\firmware.bin`) to a microSD card.
  - Safely eject the microSD card.
  - Insert the microSD into a BTT SKR V1.4 TURBO board and restart it (The flashing process will automatically start when firmware.bin is present. Then it will rename firmware.bin to firmware.CUR).

### Configure the TFT
- Build TFT firmware update using `utilities/TFT24-build_SDCard.py`.
- Power off the mainboard.
- Connect EXP1 and EXP2
  - If using (or any MKS board apparently), cut off the notches and insert EXP1 and EXP2 the opposite way (resolves [#14 The display doesn't turn on with (only) EXP1 and EXP2 connected if using an A3S (MKS board) with a BTT TFT24 V1.0](https://github.com/poikilos/r2x_14t/issues/14)) as per [BigTreeTech Screens TFT24 V1.1 and TFT35 V3.0 Touch Screen Display compatible 12864LCD](https://www.youtube.com/watch?v=rexqrW6PbnQ) (See [15:29](https://www.youtube.com/watch?v=rexqrW6PbnQ&t=15m29s)).
- Insert the card into the display.
- Power on the mainboard (or power the display any other way) and the flashing process will start automatically.


## FlexionHT
The FlexionHT retrofit kit for the Replicator 2X is highly recommended. I ordered the Flexion on eBay and got the FlexionHT and it works fine and is suitable for flexible filament. Along with the FlexionHT retrofit kit you can use the printable parts below.

The ThingiVerse collection "[Poikilos R2X 14T mod and upgrades for Replicator 2X](https://www.thingiverse.com/poikilos/collections/poikilos-r2x-14t-mod-and-upgrades-for-replicator-2x)" also lists such parts.

### [Part Cooling Fan Duct for R2X 14T with FlexionHT](https://www.thingiverse.com/thing:5190784) CC BY 4.0 Poikilos on ThingiVerse
My BLTouch mount for the FlexionHT:
- For the top screw, using a set screw (headless) or no screw at all is better so as not to interfere with the cleaning wheel brush on the FlexionHT, so now the mount has clips and side shank holes to hold them down.
  - If you do use a screw in the top, going in more than about 2.5mm will cause the screw to block the long motor mount screws!
    - Some screw kits have nothing shorter than 8mm, so the shaft on the BLTouch mount has to be 5.5 (8-2.5) tall, but it is partly cut away to make room for the cleaning wheel brush. You can cut off this whole top brace if desired, especially if you use the side screw shank holes.
- The countersunk side screw shank holes are ideal for stability.
  - There are 4 holes in case you have the flexion mounted in the other orientation (rotated 180 degrees looking at the front). They are counter-sunk 90 degrees for metric screws.
  - Countersunk screws are measured from the head. The M3 screws must be at least 4mm (3.84562 to have 1mm of grab) and cannot be longer than 6.5 (3.84+2.84562=~6.69: 3.84 depth in holes, plus 2.84562 thickness of my BLTouch mount)
    - A rare but standard countersunk M3 computer screw is 6mm (M3x6, but typically closer to 1/4" long--actually ~5.82mm)

### [BLTouch Mount for FlexionHT on R2X 14T mod for MakerBot Replicator 2X](https://www.thingiverse.com/thing:5537397)

## Project Status

Using a later version of the bugfix branch on the upstream repository is desirable, while utilizing the platformio.ini, Configuration.h, and Configuration\_adv.h from the fork. Updating will provide M154 position auto-report, which the BIGTREETECH TFT35 (and other models) can utilize (the setting must be enabled in _both_ the Marlin Configuration.h and in the TFT firmware configuration file as per the [BTT Touchscreen readme](https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware)).

Updates to platformio.ini, Configuration.h and Configuration_adv.h that work with later commits of the Marlin bugfix-2.x.x branch will go here. For a fully-tested version or for earlier commit history, see <https://github.com/poikilos/Marlin/tree/bugfix-2.0.x-r2x_t14>.

For information on past and possible future changes to the factory design, see [contributing.md](contributing.md).


## Hardware Changes

The main goal was to improve bed adhesion and eliminate skipping on the extruders and z axis. The solutions used are:

- Remove the grease from the z-axis and apply PTFE-based dry lube (did the same for all other axes).
- Improved drivers
    - requires: new mainboard (The BTT SKR V1.4 Turbo mainboard allows using improved stepper drivers and slicer software)
        - requires: drill 4 #6-32 pilot holes for mainboard standoffs; screw in the standoffs; screw in the mainboard with M3 screws.
        - requires: thermistors
            - requires either:
                - FlexionHT
                - OR drilling holes for the thermistors (or getting new heater blocks in this case); drilling a hole in the bed for the thermistor, and a 2.5mm hole close enough so the screw head or washer holds the thermistor wires enough to keep the thermistor in place, then tapping the the 2.5 mm hole using a M3 tap.
        - provides: all new electronics (forums indicate the stock mosfets on the Mightyboard aren’t that great and that people often replace them) other than the endstops and motors.
- FilaPrint bed surface:
    - provides: heat-responsive bed surface (Adhesion increases when hot; ABS parts detach easily when cooled to around 70 C and self-detach at a lower temperature — PLA+ detach easily around 35 C then self-detach around 25 C)
- BLTouch Smart V3.1 (If you don't use this, I still suggest adding a ZMAX endstop [skip the steps about removing the ZMIN endstop in that case] to prevent the terrible clunking noise, though it technically only damages the end of the Z axis lead screw. The clunking doesn't seem to affect the follower significantly, but gums up its grease with metal shavings!)
    - requires:
      - Marlin 2.0 (which requires a new mainboard, generally, though an old fork of Marlin exists that may work with one or more Mightyboard hardware versions)
      - Move the Z endstop to the bottom ("right" in these cases means your right when you are looking at the back).
        - Remove the soft rear wall of the printer.
        - Unplug the Z axis endstop and remove the screws and then remove it.
        - Drill (2) holes in the z-axis mounting plate (removable back plate) spaced 3/4" (19.05mm) apart, with the hole centers being 62.5mm from the bottom of the back mounting plate; the first hole's center being about 3.75mm to the right of the right edge of the wiring harness bracket.
        - Make (2) 3mm spacers, around 6.5-8mm longnear the bottom rear of the board. For better stability, make some sord of 3rd spacer or add hot glue for spacing.
        - Unplug the other end of the endstop connector from the ZMIN port on the mainboard and plug it into the ZMAX port.
        - Change Configuration.h to use the ZMAX port.
    - provides: mesh bed leveling (The firmware is set to 25-point probing and bilinear interpolation; Auto Bed Leveling in the menu runs the process then asks to save to EEPROM; The printer automatically uses this as long as the start G-code loads the stored mesh–the firmware is also set to load it on startup)
- Copperhead throats
    - requires: new standard-style threaded heater blocks (which also hold thermistors without modifications and provide more room for cooling ducts); new dual-extruder threaded motor mount block (“cold block”; hand machined from a large heatsink so that block and fins are a continuous piece of metal).
        - requires: drilling out the heater blocks to hold the large MakerBot heater cartridges (switching to standard heater cartridges is also possible)
    - solves: Prevent print errors (drag) and failures (fatal clogs) caused by heat creep (expansion of filament at the upper part of the throats). The failure sometimes occurred with ABS but almost always occurred with PLA/PLA+.


### Optional Add-ons
- [Simplified & Enhanced Air Scrubber for 3M Filter such as for MakerBot Replicator 2X](https://www.thingiverse.com/thing:4871456) by Poikilos


## Slicer Settings

While tweaking, ensure your filament is dry before assuming that surface flaws are due to slicing or hardware issues. Consider using a drybox system such as by printing [Complete IKEA Drybox Solution 10.6 liter / 358 oz](https://www.thingiverse.com/thing:4682691) by crashdebug December 11, 2020.

Temperatures: For printing ABS, a bed temperature of 105 C recommended by the FilaPrint manual works well. A nozzle temperature of 230 C works well for high speeds up to 100 mm/s according to the MakerBot website (even with PLA, they say).

Bed Adhesion: Ensure you load the saved mesh in the start G-code for mesh bed leveling (this may not be necessary since the firmware is set to load it at startup). Using regular ABS (tested MakerBot that was sitting out) with the FilaPrint surface requires about 150% overextrusion on the first layer for large models and 200% (or 150% and a raft) for small models. The PrusaSlicer (or Slic3r) raft detaches well for ABS (but not so well as Cura’s when using PLA+).

For more information, see "First-time setup" in [documentation/manual.md](documentation/manual.md#first-time-setup).

### Bed Adhesion
I was able to get bed adhesion with higher extrusion for the first layer, even without a raft.

The first layer extrusion that worked is 150%.
(using FilaPrint's recommended 105 C bed temp for ABS)

For smaller models such as Benchy, I either need to use 200% for the 1st layer or a raft. Using that much overextrusion for the first layer will require turning up the elephant's foot compensation and I may make a profile for small models.

For more information, see "Bed Adhesion" in [documentation/manual.md](documentation/manual.md#bed-adhesion).


## Profiles
See "First-time Setup" in [documentation/manual.md](documentation/manual.md#first-time-setup).


## Making Modifications
To make modifications that differ from the current state of the r2x_14t project or to understand the inner workings, See [contributing.md](contributing.md).


## Development

### marlininfo
The marlininfo module is a Python module for modifying and deploying Configurations regardless of version.

In several variable names, "C_" or "c_" refers to Configuration.h
and "C_A_" or "c_a_" refers to Configuration_adv.h


### Measurements
If the metric measurements differ from the value converted to in this section, they are more accurate (~ means approximate), within about .04mm tolerance. Where the unit of measurement isn't specified, it is mm.

- Z-Axis endstop ("Right" means when looking at the board with the switch facing upward; width on x axis is first, then y, then the third dimension if present is thickness.)
  - The board is about 1+9/16" x 5/8" (39.6 x 16.1mm x 1.63mm)
  - The 3mm shank holes are 3/4" apart, starting ~1/8" (3.5mm) from the right edge and about 1/8" (3mm) from the top.
  - The endstop switch is 6.38 from the right edge, and the size of the switch is 12.81 x 6.5 (including the bumps on the bottom for the unused two M2 shank holes that are 6.33 apart) x 5.65 mm.
  - The leads stick out 1.89mm in the back.
