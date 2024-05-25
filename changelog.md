# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).


## [git] - 2024-05-25
### Added
- end G-code for Moonraker (Klipper web interface) timelapse.


## [git] - 2024-05-25
### Changed
- (PrusaSlicer/start.gcode) Purge off of bed to not waste any space. Remove negative numbers such as for Klipper (For same effect, just set bed size to wider than bed and keep using X_MAX homing).