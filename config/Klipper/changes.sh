#!/bin/bash
# cd ~/printer_data/config || exit 1
mv bigtreetech-mmb-cubic.cfg hardware-bigtreetech-mmb-cubic.cfg
mv voronlegacy.cfg hardware-main-voronlegacy.cfg
mv extruder-bondtech-lgx.cfg hardware-extruder-bondtech-lgx.cfg
mv extruder-a3s.cfg hardware-extruder-a3s.cfg
mv display-not-emulated.cfg hardware-display-not-emulated.cfg
mv display-emulated.cfg hardware-display-emulated.cfg
mv creatorpro.cfg hardware-main-creatorpro.cfg
mv cancel.cfg macros-cancel.cfg
mv build-mesh.cfg macros-mesh-management.cfg
mv voronlegacy-A3S-non-integrated-39mm-motors-not-recommended.cfg hardware-main-voronlegacy-A3S-non-integrated-39mm-motors-not-recommended.cfg
mv printer.UNUSED-last-MakerBotR2X_BTTSKR14Turbo.cfg hardware-main-UNUSED-MakerBotR2X_BTTSKR14Turbo.cfg
mv print_start-voronlegacy-see-start_end_macros-instead.cfg macros-UNUSED-print_start-voronlegacy-see-start_end_macros-instead.cfg
mv pressure-advance-FlexionHT.cfg macros-pressure-advance-FlexionHT.cfg
mv load-unload-voronlegacy.cfg macros-load-unload-voronlegacy.cfg
mv load-unload-FFCP.cfg macros-load-unload-FFCP.cfg
mv input_shaper-resonance_test.cfg hardware-input_shaper-resonance_test.cfg
mv homing_override.cfg macros-homing_override.cfg
mv heater_bed-dc-a3s.cfg hardware-heater_bed-dc-a3s.cfg
mv heater_bed-ac.cfg hardware-heater_bed-ac.cfg
mv bigtreetech-mmb-cubic.cfg hardware-bigtreetech-mmb-cubic.cfg
mv G29.cfg macros-G29.cfg
mv filament-sensor-btt-sfs-v2.0.cfg hardware-filament-sensor-btt-sfs-v2.0.cfg
mv start-end-macros.cfg macros-main.cfg
mv start-end-macros--creatorpro.cfg macros-main-creatorpro.cfg
mv start-end-macros-0.4-nozzle.cfg macros-main-0.4-nozzle.cfg
mv set-temperature.cfg macros-temperature.cfg
mv M300.cfg macros-M300.cfg
mv M420.cfg macros-M420.cfg
mv M600.cfg macros-M600.cfg
mv M601.cfg macros-M601.cfg
mkdir -p old
mv printer-20* old/

sed -i 's|include set-temperature.cfg|include macros-temperature.cfg|g' hardware-main-UNUSED-MakerBotR2X_BTTSKR14Turbo.cfg
sed -i 's|include bigtreetech-mmb-cubic.cfg|include hardware-bigtreetech-mmb-cubic.cfg|g' printer.cfg
sed -i 's|include voronlegacy.cfg|include hardware-main-voronlegacy.cfg|g' printer.cfg
sed -i 's|include extruder-bondtech-lgx.cfg|include hardware-extruder-bondtech-lgx.cfg|g' hardware-main-voronlegacy.cfg
sed -i 's|include extruder-a3s.cfg|include hardware-extruder-a3s.cfg|g' hardware-main-voronlegacy.cfg
sed -i 's|include display-not-emulated.cfg|include hardware-display-not-emulated.cfg|g' printer.cfg
sed -i 's|include display-emulated.cfg|include hardware-display-emulated.cfg|g' printer.cfg
sed -i 's|include creatorpro.cfg|include hardware-main-creatorpro.cfg|g' printer.cfg
sed -i 's|include cancel.cfg|include macros-cancel.cfg|g' printer.cfg
sed -i 's|build-mesh.cfg|macros-mesh-management.cfg|g' macros-M420.cfg
# sed -i 's|include voronlegacy-A3S-non-integrated-39mm-motors-not-recommended.cfg|include hardware-main-voronlegacy-A3S-non-integrated-39mm-motors-not-recommended.cfg|g' printer.cfg
# sed -i 's|include printer.UNUSED-last-MakerBotR2X_BTTSKR14Turbo.cfg|include hardware-main-UNUSED-MakerBotR2X_BTTSKR14Turbo.cfg|g' printer.cfg
# sed -i 's|include print_start-voronlegacy-see-start_end_macros-instead.cfg|include macros-UNUSED-print_start-voronlegacy-see-start_end_macros-instead.cfg|g' printer.cfg
sed -i 's|include pressure-advance-FlexionHT.cfg|include macros-pressure-advance-FlexionHT.cfg|g' printer.cfg
sed -i 's|include pressure-advance-FlexionHT.cfg|include macros-pressure-advance-FlexionHT.cfg|g' hardware-main-UNUSED-MakerBotR2X_BTTSKR14Turbo.cfg
sed -i 's|include load-unload-voronlegacy.cfg|include macros-load-unload-voronlegacy.cfg|g' printer.cfg
sed -i 's|include load-unload-FFCP.cfg|include macros-load-unload-FFCP.cfg|g' printer.cfg
sed -i 's|include input_shaper-resonance_test.cfg|include hardware-input_shaper-resonance_test.cfg|g' printer.cfg
sed -i 's|include homing_override.cfg|include macros-homing_override.cfg|g' hardware-main-voronlegacy.cfg
sed -i 's|include homing_override.cfg|include macros-homing_override.cfg|g' hardware-main-voronlegacy-A3S-non-integrated-39mm-motors-not-recommended.cfg
sed -i 's|include heater_bed-dc-a3s.cfg|include hardware-heater_bed-dc-a3s.cfg|g' hardware-main-voronlegacy.cfg
sed -i 's|include heater_bed-dc-a3s.cfg|include hardware-heater_bed-dc-a3s.cfg|g' hardware-main-voronlegacy-A3S-non-integrated-39mm-motors-not-recommended.cfg
sed -i 's|include heater_bed-ac.cfg|include hardware-heater_bed-ac.cfg|g' printer.cfg
sed -i 's|include G29.cfg|include macros-G29.cfg|g' printer.cfg
sed -i 's|include filament-sensor-btt-sfs-v2.0.cfg|include hardware-filament-sensor-btt-sfs-v2.0.cfg|g' printer.cfg
sed -i 's|include start-end-macros.cfg|include macros-main.cfg|g' printer.cfg
# sed -i 's|M300.cfg|include macros-M300.cfg|g' printer.cfg  # was never used before renamed
sed -i 's|M420.cfg|include macros-M420.cfg|g' printer.cfg
sed -i 's|M600.cfg|include macros-M600.cfg|g' printer.cfg
sed -i 's|M601.cfg|include macros-M601.cfg|g' printer.cfg
