# Contributing
This document describes the project status and reasons for making certain design choices. This information will help you make modifications to your firmware and changes to the r2x_14t's design.

(Project status [`x`=done, `-`=skipped])
- [-] Change additional author strings (Version.h didn't work)
```C
#define DETAILED_BUILD_VERSION "poikilos/bugfix-2.0.x-r2x_14t"
#define SOURCE_CODE_URL "github.com/poikilos/Marlin"
#define WEBSITE_URL "poikilos.org/r2x-14t"
```
- [x] Set UUID
```
// _UUID "d9556f29-45f8-4625-bd1c-746a006b8a02"
#define MACHINE_UUID "d9556f29-45f8-4625-bd1c-746a006b8a02"
```

For further project status notices, see "Project Status" in the [readme](readme.md#project-status).


## Implement SKR V1.4 TURBO changes
The video cited is [SKR V1.4 TURBO Marlin 2.0.3 Setup](https://youtube.com/watch?v=6uGqpCe3Am0&t=10m6s) by Chris Warkocki (<https://github.com/codiac2600>).
- [x] Uncomment the "MACHINE_UUID" line and change it to "#define MACHINE_UUID "d9556f29-45f8-4625-bd1c-746a006b8a02"
  (only for TCS' Replicator 2X)
- [x] [PID Tuning](https://reprap.org/wiki/PID_Tuning)
  - See Configuration.h line 492 for nozzles and further down for bed.
- dual nozzle changes
  - [x] E1_DRIVER_TYPE
  - [x] DEFAULT_AXIS_STEPS_PER_UNIT
  - [x] DEFAULT_MAX_FEEDRATE
  - [x] DEFAULT_MAX_ACCELERATION
- [-] ENDSTOP_INTERRUPTS_FEATURE ?
- calibrate `*AXIS_STEPS_PER_UNIT`
  - [-] x,y,z (used values from <https://3dprinting.stackexchange.com/a/678>)
  - [x] e0 & e1
    - stock firmware says (in a comment) "96275202 1,000,000" (96.2752, way different than Marlin default)
    - Set to 96.275 then calibrated to 95/100mm resulting in 91.46125
      - To use the factory extrusion, set flow to 105.26% (96.275/91.46125)
- [x] Make changes for BLTouch
  - Change `Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN` and settings near it
    - Codiac2600 says at 19:37 he will make a separate video for BLTouch
  - Change settings in Configuration_adv.h
- [x] `*_BED_SIZE`, `Z_MAX_POS`, and everything in between
- [x] Use `PROBING_HEATERS_OFF`
- [ ] Consider using `FIL_RUNOUT_*` (See 17:00 in codiac2600 video)
  - also set `*INVERTING` since is on when not out
- Consider skew calibration.
- [ ] add linear advance to start G-code (LIN_ADVANCE_K is set to 0.00 as per the video so G-code controls it; S-curve is enabled.).
- [x] Consider `TEMP_BED_WINDOW 3` `TEMP_BED_HYSTERESIS 8` as per v=6uGqpCe3Am0&t=10m6s (Will it fix the bed temp error? Try PID tuning first.)
  - [x] PID Tuning: <https://www.3dmakerengineering.com/blogs/3d-printing/pid-tuning-marlin-firmware> (See also <https://www.youtube.com/watch?v=rp3r921DBGI>)
    - [x] Enable PID tuning.
- [x] Add end g-code for moving the bed down to 130 or so (150 is too much, since homing with the probe requires it to move the bed downward for clearance first).
- [ ] Update poikilos.org/r2x-14t (page) and add a post explaining the modding process.

### Other Notes
- Z_PROBE_LOW_POINT is the max deviation across the bed (see documentation issue: <https://github.com/MarlinFirmware/Marlin/issues/11235>)
- Several settings were left at defaults (usually disabled) as per the video:
  - Encoder settings
  - Backlash
  - LED
  - Power recovery (requires separate component?)
  - firmware retraction
  - and others listed in my first commit's description even though the video changed them.
- [ ] Set ENDSTOP_INTERRUPTS_FEATURE?
- Consider updating the TFT24 firmware.

## Implement Replicator 2X changes.
See <http://iamanerd.org.uk/makerbot-replicator-2x-btt-skr-1-4-turbo/>
- [-] Consider using his suggested EO_AUTO_FAN_PIN setting

## Implement dual nozzle changes.
Dual-extruder changes are by RevoCayne on <https://reprap.org/forum/read.php?415,658217> (The asker's settings are wrong but the answers supply fixes).


## Implement BLTouch changes
- The following changes are from the manual for the BLTouch Smart V3.1 as found at antclabs.com.
  - [ ] Set the start G-code as specified in the BLTouch manual (with manual changes for a recent bugfix version of Marlin 2.0).
- (2021-05-06) From Crosslink's Jun 6, 2020 video [SKR 1.3 - BLtouch installation and Marlin 2.0 configuration](https://youtube.com/watch?v=7le9L2LMY-U).
  - NOZZLE_TO_PROBE_OFFSET appears to be 6.07 (tested using the dial in Marlin mode with the nozzle being 0.1 off of the bed)
    - +3.65 when not deployed
- From "BLtouch Bed Leveling Sensor - Everything Install - Chris's Basement"
  <https://www.youtube.com/watch?v=p504oU-D6iE&t=6m0s>
  - Do not define Z_MIN_PROBE_PIN.
    - Marlin\src\pins\lpc1768\pins_BTT_SKR_V1_4.h
      already defines `Z_MIN_PROBE_PIN` as `P0_10` (lpc1769\pins*TURBO includes it has no other related code)
- From [ABL offset guide including new probe Z offset wizard](https://www.youtube.com/watch?v=fN_ndWvXGBQ)
  Enable the wizard.
  - To use it, see Usage.

## Implement changes for hotend fan
- [x] No firmware changes are necessary: Use the variable-speed fan for the hotends and the always-on fans for the others.

## Making Sneaky Firmware Overextrusion Optional
The Makerbot Replicator 2X had hardware overextrusion--it had 96.275 steps per mm in the Mightyboard firmware but on the new BTT SKR V1.4 Turbo mainboard I started there and calibrated it to 91.46125. To gain back that overextrusion for ABS, I'm experimenting with a 1.05 extrusion multiplier for the whole print since they may have found that to help with ABS errors and set the z-steps sneakily (unless 96.275 steps per mm was merely an error on their part).

## Filament runount sensor
According to "BigTreeTech SKR V1.4 Mainboard - Full Install Part 1 - 2209 Drivers - Chris' Basement" Apr 15, 2020:
- If adding a filament runout sensor (connected starting at EN0), also remove the diag pin on each extruder driver.

## Other settings
- Consider using `Z_PROBE_END_SCRIPT`
- [x] Insert the included FAT32-formatted MicroSD card into the SKR board so it has more space for emulated EEPROM.
  - Fixes (`upload_port = COM5` doesn't fix):
```
Unable to find destination disk (Autodetect Error)
Please select it in platformio.ini using the upload_port keyword (https://docs.platformio.org/en/latest/projectconf/section_env_upload.html) or copy the firmware (.pio/build/LPC1769/firmware.bin) manually to
the appropriate disk
. . .
...*** [upload] COM5\firmware.bin: No such file or directory
```
- (How to do a nozzle wipe before every print - Gcode Scripts part 2)[https://www.youtube.com/watch?v=6csbJ5965Bk] Nov 30, 2016 by Maker's Muse
```
G1 Y-3.0 F500.0 ; move out of print volume
G1 X60.0 E9 F500.0 ; start purge
G1 X100 E12.5 F500.0 ; finish purge line
```


## Build & Upload
- Ensure PlatformIO is installed in Visual Studio Code
- Ensure that the bugfix-2.0.x-replicator2x branch of github.com/poikilos/Marlin is checked out or the bugfix branch of the upstream repo (recommended) with the Configuration.h, Configuration_adv.h, and platformio.ini here.
- Open the Marlin directory using PlatformIO
- Click the PlatformIO button on the left.
  - Click the build and (if successful) upload options under LPC1769 (SKR V1.4 TURBO)
