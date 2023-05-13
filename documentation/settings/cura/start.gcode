
; Note that Cura automatically adds more before the below start G-code, such as setting the current tool to the initial extruder (See documentation/settings/cura/automatically_added_by_Cura-example.gcode on <https://github.com/poikilos/r2x_14t>).

; Cura variables reference:
; <http://files.fieldofview.com/cura/Replacement_Patterns.html>

; material_print_temperature: {material_print_temperature}
; material_print_temperature_layer_0: {material_print_temperature_layer_0}
; material_initial_print_temperature: {material_initial_print_temperature}
; material_final_print_temperature: {material_final_print_temperature}
; default_material_bed_temperature: {default_material_bed_temperature}
; material_bed_temperature: {material_bed_temperature}
; material_bed_temperature_layer_0: {material_bed_temperature_layer_0}


; Below is code from the BLTouch Smart V3.1 manual
; except:
; - with Cura variables
; - bed temp moved to below auto home since UBL does temp automatically
;   (so adding another temp may differ and cause an unnecessary long delay)
;M106 S255 ; fan
; M190 S{print_bed_temperature} ; bed temp
; ^ M190 S(print_bed_temperature) deprecated

; M190 S{default_material_bed_temperature}
; ^ M190 S(default_material_bed_temperature)
; {material_bed_temp_wait}
; ^ {material_bed_temp_wait}
;M109 S210 ; nozzle temp
M280 P0 S160
G4 P100 ; delay for BLTouch
; M420 S1 ; Restore manual mesh instead of G29 re-probing (www.youtube.com/watch?v=eF060dBEnfs)
; ^ NOTE that braces even in comments cause a parsing error in PrusaSlicer

G28 ; home
; G28 turns leveling off!! Turn on leveling on: G29 A ; or M420 S1
; See <https://marlinfw.org/docs/gcode/G029-ubl.html>
; G29 ; auto bed leveling
G29 A ; enable bed leveling (emulates M420 S1 if UBL; not required if RESTORE_LEVELING_AFTER_G28)
; M420 S1 ; already done by G29 A if AUTO_BED_LEVELING_UBL
; M420 S1 ; enable bed leveling *if* there is a valid mesh.
; Use G29 L1 in filament code if PLA bed temp mesh is stored in the first slot

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
; M190: wait for bed temp
; S<temp>: wait *only when heating* (for cooling also, use R<temp>)

; adhesion_extruder_nr: {adhesion_extruder_nr}
; extruder_nr: {extruder_nr}
; initial_extruder_nr: {initial_extruder_nr}
; ^ initial_extruder_nr is "Application-defined" according to fieldofview.com.
; travel_speed: {travel_speed}
; ^ travel speed may be in mm/s but should be in mm/minute. See <https://github.com/Ultimaker/Cura/issues/10636>.

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
; G1 Y2.0 F500.0 ; move out of print volume
; ^ changed from -3 by Poikilos
; G1 X60.0 E9 F500.0 ; start purge
; G1 X100 E12.5 F500.0 ; finish purge line
; G1 X110 E18 F500.0 ; start purge (changed by Poikilos; doubled E)
; G1 X110 F3000.0 ; start purge (changed by Poikilos; no E)
; G1 X80 Y0.5 E30 F500.0 ; finish purge line (changed by Poikilos; E was 12.5)
; G1 Y0.5 F250.0 ; get behind the line to wipe more on the way (added by Poikilos)


G92 E0 ; Say this offset is 0
G90 ; absolute positioning (G91 is relative)
G1 X-5 Y5 F9000
; ^ X<0 to go off the bed a single-extruder configuration.
G1 Z0 F9000
; ^ Do z last in case there is junk hanging off of the nozzle
; G1 X50 Y2.5 Z0.22 F(travel_speed); doesn't work due to Cura issue 10636
; ^ parenthesis since braces even in comments cause a parsing error in PrusaSlicer
G1 X-1 Y150 E44 F500.0 ; Purge backward. PLA max volumetric speed: about E22mm per 60mm 500mm/minute
; ^ higher volumetric speed may be possible without line causing back pressure
G1 Z0.0 F8000
; ^ Z ~0 to prepare to wipe off nozzle on edge of bed
G1 X0.0 F8000
G1 X1.0 Z0.05 F8000
; ^ actually wipe on edge of bed
; G1 Y1.3 F12000.0
; G1 X1.0 Y5 E44 F500.0 ; Purge backward.
; ^ Get behind the first line so nozzle gets wiped again by the line on the way out from here.
; Try to toss the line off of the bed (usually not possible without cooling, but such a delay causes purge to be useless, so skip everything below):
; G1 Y0 F12000.0
; G1 X2.4 F12000.0
; G1 Y10 Z-0.1 F12000.0
; G1 X0 Y150 F12000.0
; G1 X0 Y0 F12000.0
; G1 Z0 F12000.0
; G92 E-5 ; Say this offset is -1 (force extra extrusion at start)
