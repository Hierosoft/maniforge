; M104 S0 ; turn off temperature
; G28 X0  ; home X axis
; M84     ; disable motors
; ^ default PrusaSlicer version <= 2.4.2 gcode

G91; Set relative positioning mode
G1 E-5 F600; retract filament slightly
M140 S0; Turn off the bed heater
M104 S0; Turn off the nozzle heater
G28 X; Home the X axis
G0 Y280 F600; Bring the bed to the front for easy print removal
M84; Turn off the motors
; (Pinces, 2018)

; References
; Pinches, S. (2018b, March 29). Starting & ending gcode. Retrieved November 8, 2019, from The Unofficial JGAurora Wiki website: https://jgaurorawiki.com/start-and-end-gcode
