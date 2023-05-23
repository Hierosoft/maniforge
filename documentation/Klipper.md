Installs (optionally):
1) CancelObject			6) PrintTimeGenius
2) Bed Visualizer		7) UI Customizer
3) Firmware Updater
4) Terminal Commands Extended:
5) Active Filters Extended

Change ustreamer camera resolution:
```
sudo nano /etc/systemd/system/cam_octoprint.service
#change Exec as necessary then save
sudo systemctl daemon-reload
sudo systemctl restart cam_octoprint
```

Go to the web interface (<http://$HOST:5000/>) to set the stream URL.
Settings, Features, Webcam & Timelapse (URLs below are for ustreamer):
- Webcam, Stream URL http://`hostname`.local:8001?action=stream
- Timelapse, Snapshot URL http://buzzy.local:8001?action=snapshot
- Settings, OctoPrint, Plugin Manager, Install OctoKlipper plugin

Install Klipper firmware (These instructions assume BTT SKR 1.4 Turbo):
(See [Ender 6 - Klipper on SKR Board with stock touchscreen](https://www.youtube.com/watch?v=t1FgE3OgUA8))
- `git clone https://github.com/Klipper3d/klipper`
- run `./klipper/scripts/install-octopi.sh`
- `make menuconfig`
- [x] Enable extra low-level configuration options
- Micro-controller Architecture (LPC176x (Smoothieboard))
- Processor model (lpc1769 (120 MHz))
  - If you do not have the "Turbo" use 100 MHz
- Bootloader offset (16KiB bootloader (Smoothieware bootloader)) (<https://www.makenprint.uk/3d-printing/3d-firmware-guides/klipper/compiling-klipper-firmware/#BTT-SKR-V1.4-Turbo>)
- Communication interface (USB)
- USB ids (default is 1d50:6140 but `lsusb -v output` is `Bus 001 Device 002: ID 1d50:6029 OpenMoko, Inc. Marlin 2.0 (Serial)` apparently for SKR Mini v3)
- GPIO pins at startup: leave blank (<https://www.makenprint.uk/3d-printing/3d-firmware-guides/klipper/compiling-klipper-firmware/#BTT-SKR-V1.4-Turbo>)
- Exit menuconfig and save (creates `/home/pi/klipper/.config`)
- `make clean`
- `make`
- If using Ender3 Do *not* rename klipper.bin nor a filename like the last used one (See [6:34](https://www.youtube.com/watch?v=gfZ9Lbyh8qU&t=6m34s) in "Installing Klipper on the Creality Ender3 V2 (and other 32 bit creality printers" by NERO 3D)
```
find /dev/serial/by-path/
find /dev/serial/by-id/
```
- Set `BTT_DEV=` to the correct full path such as via `/dev/serial/by-path/pci-0000:00:1d.0-usb-0:2:1.0` then:
```
sudo service klipper stop
make clean  # essential according to users online!
make flash FLASH_DEVICE=$BTT_DEV
```
- Or, If won't go into bootloader mode and you're not using Ender3,
  see [skr 1.4 turbo bootloader](https://github.com/bigtreetech/BIGTREETECH-SKR-V1.3/issues/346)
  or [Skr 1.4 flashing issue](https://github.com/Klipper3d/klipper/issues/3355)
  or do:
  1. `MOUNT=sdf1` but change sdf to your MicroSD card (insert then type `lsblk`)
  2. `sudo mkdir /mnt/$DRIVE && sudo mount /dev/$DRIVE /mnt/$DRIVE`
  3. `make clean`
  4. `sudo cp out/klipper.bin /mnt/$DRIVE/firmware.bin` (If says IO error, confirm steps 1-2 are done correctly.
- `cp config/generic-bigtreetech-skr-v1.4.cfg /home/pi/printer.cfg`
