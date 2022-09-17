# Settings


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
- Regular Fan Speed at Height: 1.5 (default: calculated from Initial Layer Height)
  - If there are bridges on a low layer, reduce it to one fewer than that layer number instead of using mm.
