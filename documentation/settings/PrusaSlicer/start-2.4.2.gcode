; G28 ; home all axes
; G1 Z5 F5000 ; lift nozzle
; ^ default PrusaSlicer version <= 2.4.2 gcode

; M420 S1 ; enable mesh bed leveling (Pinches, 2018a)

; A5 (not A5S) mesh bed leveling applies to A3S V1 (Pinches, 2019)

G28 ; Home all axis
; M420 S1 ; enable mesh bed leveling (Pinches, 2018a)
G1 Z15.0 F6000 ; Move up 15mm at 6000mm/min (note: more than the max speed set in the printer firmware)
M190 S[first_layer_bed_temperature] ; Set bed temp. (added by poikilos)
M140 S[first_layer_bed_temperature]  ; Wait for bed temp. (added by poikilos)
M109 S[first_layer_temperature_0]  ; Wait for all used extruders to reach temperature. (added by poikilos)
G92 E0 ; Reset extruder length to zero
G90 ; set absolute--Try to fix issue of line printing in air, possibly from relative positioning in last gcode used (added by Poikilos)
G1 X0.0 Y0.0 F1000.0 ; go to edge of print area
G1 Z0.200 F1000.0 ; Go to Start Z position
G1 X60.0 E9.0 F1000.0 ; intro line
;G1 X95.0 E46.5 F1000.0 ; intro line
G1 X164.0 E40 F1000.0 ; intro line (by Poikilos: 3x more to purge cooked filament; X168 is edge of bed clip, or X193 is edge of printable bed surface if using the x endstop pusher included with Poikilos' dual creality 4010 blowers mount)
G92 E0.0 ; reset extruder distance position
; Thanks to DaHai for the wipe script
; (Pinces, 2018b)


; Martin H. Jan 27, 2019 https://forum.repetier.com/discussion/6139/gcode-purge-line-before-print
; Pinches, S. (2018a, February 4). Mesh bed levelling. Retrieved November 6, 2019, from The Unofficial JGAurora Wiki website: https://jgaurorawiki.com/a5/mesh-bed-levelling-routine
; Pinches, S. (2018b, March 29). Starting & ending gcode. Retrieved November 8, 2019, from The Unofficial JGAurora Wiki website: https://jgaurorawiki.com/start-and-end-gcode
; Pinches, S. (2019, November 5). How to use mesh bed leveling on custom firmware _Reply_. Retrieved November 6, 2019, from The Unofficial JGAurora 3D Printer Forum website: https://jgauroraforum.com/discussion/896/how-to-use-mesh-bed-leveling-on-custom-firmware

; //action:showstart
