; Cura variable reference:
; <http://files.fieldofview.com/cura/Replacement_Patterns.html>
; Below is code from the BLTouch Smart V3.1 manual
; except:
; - with Cura variables
; - bed temp moved to below auto home since UBL does temp automatically
;   (so adding another temp may differ and cause an unnecessary long delay)
;M106 S255 ; fan
; M190 S{print_bed_temperature} ; bed temp
; ^ M190 S(print_bed_temperature) deprecated

; INFO: The bed temperature is only correct when the other extruder is disabled in Cura!
; M140 S{material_bed_temperature_layer_0} ; Set Heat Bed temperature
; ^ M140 S(material_bed_temperature_layer_0)

; Comma is the subscript operator--See
; <https://community.ultimaker.com/topic/31181-dual-extruder-start-script-gcode-placeholders/>.
; M190 S{material_bed_temperature_layer_0, adhesion_extruder_nr}
; ^ M190 S(material_bed_temperature_layer_0, adhesion_extruder_nr)
; M190 S{material_bed_temperature_layer_0, extruder_nr}
; ^ M190 S(material_bed_temperature_layer_0, extruder_nr)
M190 S{material_bed_temperature_layer_0, initial_extruder_nr}
; ^ M190 S(material_bed_temperature_layer_0, initial_extruder_nr)

; adhesion_extruder_nr: {adhesion_extruder_nr}
; extruder_nr: {extruder_nr}
; initial_extruder_nr: {initial_extruder_nr}
; ^ initial_extruder_nr is "Application-defined" according to fieldofview.com.

; M190 S{default_material_bed_temperature}
; ^ M190 S(default_material_bed_temperature)
; {material_bed_temp_wait}
; ^ {material_bed_temp_wait}
;M109 S210 ; nozzle temp
M280 P0 S160
G4 P100 ; delay for BLTouch
M420 S1 ; Restore manual mesh instead of G29 re-probing (www.youtube.com/watch?v=eF060dBEnfs)
; ^ NOTE that braces even in comments cause a parsing error in PrusaSlicer
G28 ; home
; G29 ; auto bed leveling

;G1 X60.0 Y-0.5 Z0.32 F500.0; added by Poikilos
;G1 X50 Y-1.0 Z0.22 F3000.0; added by Poikilos

; Below is the Cura default start g-code:
;G28 ;Home
;G1 Z15.0 F6000 ;Move the platform down 15mm
;Prime the extruder
;G92 E0
;G1 F200 E3
;G92 E0

; Purge line from "How to do a nozzle wipe before every print - Gcode Scripts part 2" (https://www.youtube.com/watch?v=6csbJ5965Bk) Nov 30, 2016 by Maker's Muse
; ^ NOTE that braces even in comments cause a parsing error in PrusaSlicer
; G1 Y-0.5 F500.0 ; move out of print volume
; ^ changed from -3 by Poikilos
; G1 X60.0 E9 F500.0 ; start purge
; G1 X100 E12.5 F500.0 ; finish purge line
; G1 X110 E18 F500.0 ; start purge (changed by Poikilos; doubled E)
G1 X110 F3000.0 ; start purge (changed by Poikilos; no E)
G1 X80 Y-2.0 E30 F500.0 ; finish purge line (changed by Poikilos; E was 12.5)
G1 Y-2 F250.0 ; get behind the bump to wipe more on the way (added by Poikilos)

G92 E0 ; added by Poikilos
; G1 X60.0 Y-0.5 Z0.32 F500.0; added by Poikilos
G1 X50 Y-1.0 Z0.22 F3000.0; added by Poikilos
; Purge line from "How to do a nozzle wipe before every print - Gcode Scripts part 2" (https://www.youtube.com/watch?v=6csbJ5965Bk) Nov 30, 2016 by Maker's Muse
; ^ NOTE that braces even in comments cause a parsing error in PrusaSlicer
; G1 Y-0.5 F500.0 ; move out of print volume
; ^ changed from -3 by Poikilos
; G1 X60.0 E9 F500.0 ; start purge
; G1 X100 E12.5 F500.0 ; finish purge line
; G1 X110 E18 F500.0 ; start purge (changed by Poikilos; doubled E)
G1 X110 F{travel_speed} ; start purge (changed by Poikilos; no E)
; G1 X35 Y-2.0 E45 F500.0 ; finish purge line (changed to .75E per 8mm & longer total by Poikilos; E was 12.5, distance was ~30)
G1 X20 Y-2.0 E45 F500.0 ; finish purge line (changed to longer total by Poikilos; E was 12.5, distance was ~30)
G1 Y-2.5 F250.0 ; get behind the bump to wipe more on the way (added by Poikilos)
G92 E0 ; added by Poikilos
