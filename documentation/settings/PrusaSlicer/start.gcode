; G28 ; home all axes
; G1 Z5 F5000 ; lift nozzle
; ^ Above is the default PrusaSlicer code

; layer_height = [layer_height]
; perimeter_speed = [perimeter_speed]
; fan_always_on = [fan_always_on]
; bridge_fan_speed = [bridge_fan_speed]
; cooling ("Enable auto cooling") = [cooling]
; perimeters = [perimeters]
; nozzle_diameter = [nozzle_diameter]


; Below is code from the BLTouch Smart V3.1 manual (modified by Poikilos):
; M106 S255 ; fan
; M190 S[first_layer_bed_temperature] ; set bed temp and wait
; ^ first_layer_bed_temperature
M190 S[bed_temperature] ; set bed temp and wait
; ^ bed_temperature
M109 S[first_layer_temperature_0] ; set nozzle temp and wait
M280 P0 S160 ; BLTouch alarm release
G4 P100 ; delay for BLTouch
G28 ; home
; G29 ; auto bed leveling
; G28 A  ; re-enable mesh leveling (same as M420 S or M420 S1; called here since G28 disables it)
M420 S1 ; Restore manual mesh instead of G29 re-probing (www.youtube.com/watch?v=eF060dBEnfs)
; ^ NOTE that braces even in comments cause a parsing error in PrusaSlicer

G92 E0 ; added by Poikilos
; G1 X60.0 Y-0.5 Z0.32 F7200; added by Poikilos
G1 Y50 X-1.0 Z0.22 F7200; added by Poikilos
; Purge line from "How to do a nozzle wipe before every print - Gcode Scripts part 2" (https://www.youtube.com/watch?v=6csbJ5965Bk) Nov 30, 2016 by Maker's Muse
; ^ NOTE that braces even in comments cause a parsing error in PrusaSlicer
; G1 Y-0.5 F500.0 ; move out of print volume
; ^ changed from -3 by Poikilos
; G1 X60.0 E9 F500.0 ; start purge
; G1 X100 E12.5 F500.0 ; finish purge line
; G1 X110 E18 F500.0 ; start purge (changed by Poikilos; doubled E)
; G1 Y110 F[travel_speed] ; start purge (changed by Poikilos; no E)  F[travel_speed] is way too slow for some reason (using mm/s as mm/min??)
G1 Y110 F18000.0 ; Fast travel to start purge position (300 mm/s) (changed by Poikilos; no E)
; G1 X35 Y-2.0 E45 F500.0 ; finish purge line (changed to .75E per 8mm & longer total by Poikilos; E was 12.5, distance was ~30)
; G1 Y20 X-2.0 E45 F500.0 ; finish purge line (changed to longer total by Poikilos; E was 12.5, distance was ~30)
; G1 Y20 X-2.0 Z0 E45 F3600.0
; ^ oozes after gets on bed, so decelerate manually:
G1 Y87.5 X-2.0 Z0 E9 F3600
G1 Y65 X-2.0 Z0 E7 F1800
G1 Y42.5 X-2.0 Z0 E4.5 F900
G1 Y20 X-2.0 Z0 E1 F450

G1 X-2.5 Z0.0 F3600.0 ; get behind the filament bump (or off edge of bed if allowed by configuration) to wipe more on the way (added by Poikilos)
G1 X0 Z0.05 Y87 F18000.0 ; super quick wipe onto edge of bed diagonally for safety (knock off excess; added by Poikilos)
G1 X0 Z0.05 F18000.0 ; wipe along edge of bed (added by Poikilos; formerly F3600)
G92 E0 ; added by Poikilos
