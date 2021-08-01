; M104 S0 ; turn off temperature
; G28 X0  ; home X axis
; M84     ; disable motors
; ^ Above is the default PrusaSlicer code

G1 E-3 F2700 ;retract a bit
; ^ based on https://www.reddit.com/r/ender5/comments/kboyhg/ender_5_pro_micro_swiss_direct_drive_retract_at/

; Below is code from the BLTouch Smart V3.1 manual:
M104 S0 ; turn off temperature - Extruder
; M140 S0 ; turn off temperature - Bed
G28 X0 ; home X axis
G28 Y0 ; home Y axis ; changed by Poikilos from: G1 Y240 ; for harvest
G1 Z140 F1200 ; move bed down (added by Poikilos)
M84 ; disable motors

; M190 R45 ; wait for bed to cool to remove the print (added by Poikilos)
; ^ R waits for cooling or heating, S only for heating
M140 S0 ; turn off temperature - Bed (moved to here by Poikilos)
M117 At <40C parts detach from FilaPrint easily. 
