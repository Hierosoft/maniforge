# Settings
This is a collection of settings, including ones I generally always change if the settings are available when using any slicer.

## Cura
I always fix the following defaults.

### Walls
- (optional) Minimum Wall Line Width: .2 (default 0.34)

### Top/Bottom
Reduce print time
- Top Layers: 4 (default 5)
- Bottom Layers: 4 (default 5)

Increase top&bottom surface quality:
- Monotonic Top/Bottom Order: Yes

### Infill
Decrease material used, increase speed, reduce patterns seen in transparent material:
- Infill Pattern: Lightning

### Support
Make post-processing easier & reduce waste, pimples & inaccessible supports:
- Type: Tree
- (Type: Tree) Support Placement: Touching Buildplate
- Support overhang angle: 70 (default 50)

### Build Plate Adhesion
Reduce print time
- (Type: Raft) Raft Extra Margin: 5 (or 3; default 8)

### Cooling
Reduce warping, such as for HDglass PETG and some other materials or formulations of materials:
- Regular Fan Speed: 50.0
  - When using two Creality 4010 style fans (tested with WINSINN brand 24V), they twitch and don't turn until reaching at least 49/255 (19.22%)
- Regular Fan Speed at Height: 1.5 (default: calculated from Initial Layer Height)
  - If there are bridges on a low layer, reduce it to one fewer than that layer number instead of using mm.

### Speed
#### PETG
See also:
- [Utterly frustrated with PETG.](https://www.reddit.com/r/3Dprinting/comments/hya4xw/utterly_frustrated_with_petg/) by u/dolmdemon on Reddit.

##### FormFutura HDglass
The following apply to HDglass but some/all may apply to regular PETG.

See also:
- [Horizontal lines in test tower](https://forum.simplify3d.com/viewtopic.php?t=8770&start=30)

###### Direct Drive
- At 250C with a .4mm nozzle, 55mms at .16 layer height and .45 extrusion width is good enough for infill, but seems to be at the extremes of the volumetric speed.


## Minis
### The SiePie Small Minis Profile
The updated information discussing the profile and alternatives seems to have moved from 3dprintedtabletop.com to [lostadventures.co/pages/3d-printer-profiles](https://lostadventures.co/pages/3d-printer-profiles): "The Lost Adventures Company was created by Danny from 3D Printed Tabletop" -<https://lostadventures.co/pages/about>

Though the page says Cura improved and that a profile based on "Fine" works, the page doesn't describe exactly what settings to change. The SiePie profile still seems pretty good even for YOYI 85A TPU using bowden (JGAURORA A3S with TECBOSS 1.9mm ID 680mm tube; Other 1.9mm ID tubes should work about the same). I extracted the [profile](https://drive.google.com/file/d/1mgptwHLX3Al8MZ6-VH4dHklK_OAvftVs/view)'s metadata and I can see all that the only unique settings in there are:
```
quality_type = normal
adhesion_type = raft
layer_height = 0.08
layer_height_0 = 0.15
acceleration_travel = 5000
bottom_layers = 0
cool_fan_full_at_height = 0
infill_pattern = grid
infill_sparse_density = 100
raft_speed = 50.0
speed_infill = 80
speed_print = 25
speed_travel = 50
top_layers = 999999
```
- The top_layers trick forces the layers to print slow and with a solid pattern (unlike 100% infill or thicker walls).

### SiePie Large Minis
The extracted [profile](https://drive.google.com/file/d/11zgWHZbpnXP2Zl1bGod-h26Dxyaa4LEk/view) has only the following unique settings:
```
quality_type = normal
acceleration_travel = 5000
bottom_layers = 10
cool_fan_full_at_height = 0
infill_pattern = trihexagon
infill_sparse_density = 10
material_print_temperature = 205
raft_speed = 50.0
retraction_amount = 10
roofing_layer_count = 3
speed_infill = 80
speed_print = 60
speed_travel = 50
support_angle = 55
support_skip_some_zags = True
support_z_distance = 0.2
top_bottom_pattern = lines
top_layers = 10
adhesion_type = skirt
layer_height = 0.12
layer_height_0 = 0.15
support_enable = False
```
- The settings are a compromise between super quality and speed, so unlike SiePie's Small Minis profile, this one has infill and a thicker layer height.
