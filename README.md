# R2X 14T
The R2X 14T is a mod by Jake Gustafson for the *MakerBot Replicator 2X* (possibly compatible with clones such as FlashForge Creator Pro). The name "Axle Media" is a registered fictitious name in Pennsylvania and should be only used if the mod is done by Jake Gustafson.

The mod utilizes the BIGTREETECH SKR V1.4 Turbo and most of the hardware from the MakerBot Replicator 2X. The fork of Marlin 2.0 ([https://github.com/poikilos/Marlin/tree/bugfix-2.0.x-r2x](https://github.com/poikilos/Marlin/tree/bugfix-2.0.x-r2x)) only contains changes to platformio.ini, Configuration.h, and Configuration_adv.h.


## Project Status

Using a later version of the bugfix branch on the upstream repository is desirable, while utilizing the platformio.ini, Configuration.h, and Configuration\_adv.h from the fork. Updating will provide M154 position auto-report, which the BIGTREETECH TFT35 (and other models) can utilize (the setting must be enabled in _both_ the Marlin Configuration.h and in the TFT firmware configuration file as per the [BTT Touchscreen readme](https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware)).

## Hardware Changes

The main goal was to improve bed adhesion and eliminate skipping on the extruders and z axis. The solutions used are:

- Remove the grease from the z-axis and apply PTFE-based dry lube (did the same for all other axes).
- Improved drivers
    - requires: new mainboard (The BTT SKR V1.4 Turbo mainboard allows using improved stepper drivers and slicer software)
        - requires: thermistors
            - requires: drilling holes for the thermistors (or getting new heater blocks in this case)
        - provides: all new electronics (forums indicate the stock mosfets on the Mightyboard aren’t that great and that people often replace them)
- FilaPrint bed surface:
    - provides: heat-responsive bed surface (Adhesion increases when hot; ABS parts detach easily when cooled to around 70 C and self-detach at a lower temperature — PLA+ detach easily around 35 C then self-detach around 25 C)
- BLTouch Smart V3.1
    - requires: Marlin 2.0 (which requires a new mainboard, generally, though an old fork of Marlin exists that may work with one or more Mightyboard hardware versions)
    - provides: mesh bed leveling (The firmware is set to 25-point probing and bilinear interpolation; Auto Bed Leveling in the menu runs the process then asks to save to EEPROM; The printer automatically uses this as long as the start G-code loads the stored mesh–the firmware is also set to load it on startup)
- Copperhead throats
    - requires: new standard-style threaded heater blocks (which also hold thermistors without modifications and provide more room for cooling ducts); new dual-extruder threaded motor mount block (“cold block”; hand machined from a large heatsink so that block and fins are a continuous piece of metal).
        - requires: drilling out the heater blocks to hold the large MakerBot heater cartridges (switching to standard heater cartridges is also possible)

## Slicer Settings

While tweaking, ensure your filament is dry before assuming that surface flaws are due to slicing or hardware issues. Consider using a drybox system such as by printing [Complete IKEA Drybox Solution 10.6 liter / 358 oz](https://www.thingiverse.com/thing:4682691) by crashdebug December 11, 2020.

Temperatures: For printing ABS, a bed temperature of 105 C recommended by the FilaPrint manual works well. A nozzle temperature of 230 C works well for high speeds up to 100 mm/s according to the MakerBot website (even with PLA, they say).

Bed Adhesion: Ensure you load the saved mesh in the start G-code for mesh bed leveling (this may not be necessary since the firmware is set to load it at startup). Using regular ABS (tested MakerBot that was sitting out) with the FilaPrint surface requires about 150% overextrusion on the first layer for large models and 200% (or 150% and a raft) for small models. The PrusaSlicer (or Slic3r) raft detaches well for ABS (but not so well as Cura’s when using PLA+).

### Making Sneaky Firmware Overextrusion Optional
I was able to get bed adhesion with higher extrusion for the first layer, even without a raft.

The first layer extrusion that worked is 150%.
(using FilaPrint's recommended 105 C bed temp for ABS)

For smaller models such as Benchy, I either need to use 200% for the 1st layer or a raft. Using that much overextrusion for the first layer will require turning up the elephant's foot compensation and I may make a profile for small models.

The Makerbot Replicator 2X had hardware overextrusion--it had 96.275 steps per mm in the Mightyboard firmware but on the new BTT SKR V1.4 Turbo mainboard I started there and calibrated it to 91.46125. To gain back that overextrusion for ABS, I'm experimenting with a 1.05 extrusion multiplier for the whole print since they may have found that to help with ABS errors and set the z-steps sneakily (unless 96.275 steps per mm was merely an error on their part).

I'll provide profiles for Cura and PrusaSlicer.
