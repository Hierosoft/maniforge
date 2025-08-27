# Training Disclosure for hierosoft-logistics
This Training Disclosure, which may be more specifically titled above here (and in this document possibly referred to as "this disclosure"), is based on **Training Disclosure version 1.1.4** at https://github.com/Hierosoft/training-disclosure by Jake Gustafson. Jake Gustafson is probably *not* an author of the project unless listed as a project author, nor necessarily the disclosure editor(s) of this copy of the disclosure unless this copy is the original which among other places I, Jake Gustafson, state IANAL. The original disclosure is released under the [CC0](https://creativecommons.org/public-domain/cc0/) license, but regarding any text that differs from the original:

This disclosure also functions as a claim of copyright to the scope described in the paragraph below since potentially in some jurisdictions output not of direct human origin, by certain means of generation at least, may not be copyrightable (again, IANAL):

Various author(s) may make claims of authorship to content in the project not mentioned in this disclosure, which this disclosure by way of omission unless stated elsewhere implies is of direct human origin unless stated elsewhere. Such statements elsewhere are present and complete if applicable to the best of the disclosure editor(s) ability. Additionally, the project author(s) hereby claim copyright and claim direct human origin to any and all content in the subsections of this disclosure itself, where scope is defined to the best of the ability of the disclosure editor(s), including the subsection names themselves, unless where stated, and unless implied such as by context, being copyrighted or trademarked elsewhere, or other means of statement or implication according to law in applicable jurisdiction(s).

Disclosure editor(s): Hierosoft LLC

Project author: Hierosoft LLC

This disclosure is a voluntary of how and where content in or used by this project was produced by LLM(s) or any tools that are "trained" in any way.

The main section of this disclosure lists such tools. For each, the version, install location, and a scope of their training sources in a way that is specific as possible.

Subsections of this disclosure contain prompts used to generate content, in a way that is complete to the best ability of the disclosure editor(s).

tool(s) used:
- Grok

Scope of use: code described in subsections--typically modified by hand to improve logic, variable naming, integration, etc.

## documentation/mjpg-streamer.service
- 2025-08-20 https://grok.com/share/c2hhcmQtMg%3D%3D_d11a9ba0-49ba-49b3-89be-b09db3a5cc7c

is there a modern and maintained version of mjpg-streamer

I used jacksonliam/mjpg-streamer and did make and sudo make install, but dont' know how to set it up to run automatically

I can't get it to work:
```
i@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ cat /home/pi/mjpg-streamer.sh
#!/bin/bash

cd /home/pi/mjpg-streamer/mjpg-streamer-experimental/ || exit $?

LD_LIBRARY_PATH=.

./mjpg_strea‌​mer -o "output_http.so -w ./www" -i "input_uvc.so"

pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ cd /home/pi/mjpg-streamer/mjpg-streamer-experimental/
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ LD_LIBRARY_PATH=.
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ ./mjpg_strea‌​mer -o "output_http.so -w ./www" -i "input_uvc.so"
-bash: ./mjpg_strea‌​mer: No such file or directory
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ export LD_LIBRARY_PATH=.
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ ./mjpg_strea‌​mer -o "output_http.so -w ./www" -i "input_uvc.so"
-bash: ./mjpg_strea‌​mer: No such file or directory
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ ls *
CMakeLists.txt   input_file.so  LICENSE     mjpg_streamer    mjpg_streamer@.service  output_rtsp.so  README.md  utils.c
Dockerfile       input_http.so  makedeb.sh  mjpg_streamer.c  output_file.so          output_udp.so   start.sh   utils.h
docker-start.sh  input_uvc.so   Makefile    mjpg_streamer.h  output_http.so          postinstall.sh  TODO

_build:
CMakeCache.txt  CMakeFiles  cmake_install.cmake  install_manifest.txt  Makefile  mjpg_streamer  plugins

cmake:
FindGphoto2.cmake  FindProtobuf-c.cmake  FindZeroMQ.cmake  mjpg_streamer_utils.cmake

plugins:
input_control  input.h     input_opencv  input_raspicam     input_uvc         output_file  output_http  output_udp     output_zmqserver
input_file     input_http  input_ptp2    input_testpicture  output_autofocus  output.h     output_rtsp  output_viewer

scripts:
make_deb.sh  mjpg-streamer.default  mjpg-streamer.init  mjpg-streamer.service  README.md

www:
bodybg.gif     favicon.png        java.html                        jquery.js              jquery.ui.custom.css     sidebarbg.gif       stream_simple.html
cambozola.jar  fix.css            javascript.html                  jquery.rotate.js       jquery.ui.tabs.min.js    spinbtn_updn.gif    style.css
control.htm    functions.js       javascript_motiondetection.html  JQuerySpinBtn.css      jquery.ui.widget.min.js  static.html         videolan.html
example.jpg    index.html         javascript_simple.html           JQuerySpinBtn.js       LICENSE.txt              static_simple.html
favicon.ico    java_control.html  java_simple.html                 jquery.ui.core.min.js  rotateicons.png          stream.html
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ ls *.so
input_file.so  input_http.so  input_uvc.so  output_file.so  output_http.so  output_rtsp.so  output_udp.so
```

I fixed the invisible/unicode characters but now I get:
```
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: -1
 i: Format............: JPEG
 i: TV-Norm...........: DEFAULT
ERROR opening V4L interface: No such file or directory
 i: init_VideoIn failed
 ```

```
 i@buzzy:~ $ Connection to buzzy closed by remote host.
Connection to buzzy closed.
owner@roamtop:~$ ssh buzzy
Linux buzzy 6.1.0-38-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.147-1 (2025-08-02) x86_64
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Aug 17 20:46:58 2025 from 192.168.1.161
pi@buzzy:~ $ v4l2-ctl --list-devices
ICT Camera: ICT Camera (usb-0000:00:14.0-2):
/dev/video0
/dev/video1
/dev/media0
pi@buzzy:~ $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: -1
 i: Format............: JPEG
 i: TV-Norm...........: DEFAULT
ERROR opening V4L interface: No such file or directory
 i: init_VideoIn failed
pi@buzzy:~ $ v4l2loopback-ctl list
-bash: v4l2loopback-ctl: command not found
pi@buzzy:~ $ cat /home/pi/mjpg-streamer.sh
#!/bin/bash
cd /home/pi/mjpg-streamer/mjpg-streamer-experimental/ || exit $?
LD_LIBRARY_PATH=.
#./mjpg_strea‌​mer -o "output_http.so -w ./www" -i "input_uvc.so"
./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so"
pi@buzzy:~ $ nano /home/pi/mjpg-streamer.sh
pi@buzzy:~ $ cat /pi/mjpg-streamer.sh
cat: /pi/mjpg-streamer.sh: No such file or directory
pi@buzzy:~ $ cat /home/pi/mjpg-streamer.sh
#!/bin/bash
cd /home/pi/mjpg-streamer/mjpg-streamer-experimental/ || exit $?
LD_LIBRARY_PATH=.
#./mjpg_strea‌​mer -o "output_http.so -w ./www" -i "input_uvc.so"
./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so -d /dev/video0"
pi@buzzy:~ $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: (null)
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: -1
 i: Format............: JPEG
 i: TV-Norm...........: DEFAULT
 i: init_VideoIn failed

```


```
pi@buzzy:~ $ v4l2-ctl -d /dev/video0 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
Type: Video Capture
[0]: 'YUYV' (YUYV 4:2:2)
Size: Discrete 1920x1080
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 160x120
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 176x144
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 320x240
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 352x288
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 640x360
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 640x480
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 800x600
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 848x480
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1024x768
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x800
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x720
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
[1]: 'MJPG' (Motion-JPEG, compressed)
Size: Discrete 1920x1080
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 160x120
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 176x144
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 320x240
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 352x288
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 640x360
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 640x480
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 800x600
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 848x480
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1024x768
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x800
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x720
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
pi@buzzy:~ $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: JPEG
 i: TV-Norm...........: DEFAULT
Unable to set format: 1196444237 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
```

```
pi@buzzy:~ $ v4l2-ctl -d /dev/video1 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
Type: Video Capture
pi@buzzy:~ $ v4l2-ctl -d /dev/video0 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
Type: Video Capture
[0]: 'YUYV' (YUYV 4:2:2)
Size: Discrete 1920x1080
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 160x120
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 176x144
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 320x240
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 352x288
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 640x360
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 640x480
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 800x600
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 848x480
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1024x768
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x800
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x720
Interval: Discrete 0.100s (10.000 fps)
Interval: Discrete 0.200s (5.000 fps)
[1]: 'MJPG' (Motion-JPEG, compressed)
Size: Discrete 1920x1080
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 160x120
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 176x144
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 320x240
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 352x288
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 640x360
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 640x480
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.067s (15.000 fps)
Size: Discrete 800x600
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 848x480
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1024x768
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x800
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
Size: Discrete 1280x720
Interval: Discrete 0.033s (30.000 fps)
Interval: Discrete 0.040s (25.000 fps)
Interval: Discrete 0.050s (20.000 fps)
Interval: Discrete 0.200s (5.000 fps)
pi@buzzy:~ $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: JPEG
 i: TV-Norm...........: DEFAULT
Unable to set format: 1196444237 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
pi@buzzy:~ $ nano /home/pi/mjpg-streamer.sh
pi@buzzy:~ $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: YUYV
 i: JPEG Quality......: 80
 i: TV-Norm...........: DEFAULT
Unable to set format: 1448695129 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
pi@buzzy:~ $ v4l2-ctl --list-devices
ICT Camera: ICT Camera (usb-0000:00:14.0-3):
/dev/video0
/dev/video1
/dev/media0
pi@buzzy:~ $ v4l2-ctl -d /dev/video1 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
Type: Video Capture
pi@buzzy:~ $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: YUYV
 i: JPEG Quality......: 80
 i: TV-Norm...........: DEFAULT
Unable to set format: 1448695129 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
pi@buzzy:~ $ nano /home/pi/mjpg-streamer.sh
pi@buzzy:~ $ /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video1
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: YUYV
 i: JPEG Quality......: 80
 i: TV-Norm...........: DEFAULT
Unable to set format: 1448695129 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
pi@buzzy:~ $ cat /home/pi/mjpg-streamer.sh
#!/bin/bash
cd /home/pi/mjpg-streamer/mjpg-streamer-experimental/ || exit $?
LD_LIBRARY_PATH=.
#./mjpg_strea‌​mer -o "output_http.so -w ./www" -i "input_uvc.so"
./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so -d /dev/video1 -r 640x480 -f 30 -y"
pi@buzzy:~ $ ls -l /dev/video*
crw-rw---- 1 root video 81, 0 Aug 17 20:54 /dev/video0
crw-rw---- 1 root video 81, 1 Aug 17 20:54 /dev/video1
pi@buzzy:~ $ groups
pi adm tty dialout cdrom sudo audio video plugdev games users input netdev lpadmin gpio i2c spi network
pi@buzzy:~ $ sudo apt update
Hit:1 http://deb.debian.org/debian bookworm InRelease
Hit:2 http://deb.debian.org/debian-security bookworm-security InRelease
Hit:3 http://deb.debian.org/debian bookworm-updates InRelease
Hit:4 http://archive.raspberrypi.org/debian bookworm InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
All packages are up to date.
W: http://archive.raspberrypi.org/debian/dists/bookworm/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.
N: Repository 'Debian bookworm' changed its 'non-free component' value from 'non-free' to 'non-free non-free-firmware'
N: More information about this can be found online in the Release notes at: https://www.debian.org/releases/bookworm/i386/release-notes/ch-information.html#non-free-split
pi@buzzy:~ $ sudo apt install fswebcam
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  linux-compiler-gcc-10-x86 linux-headers-5.10.0-35-common linux-kbuild-5.10
Use 'sudo apt autoremove' to remove them.
The following NEW packages will be installed:
  fswebcam
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 51.8 kB of archives.
After this operation, 144 kB of additional disk space will be used.
Get:1 http://deb.debian.org/debian bookworm/main i386 fswebcam i386 20140113-2 [51.8 kB]
Fetched 51.8 kB in 0s (305 kB/s)
Selecting previously unselected package fswebcam.
(Reading database ... 171410 files and directories currently installed.)
Preparing to unpack .../fswebcam_20140113-2_i386.deb ...
Unpacking fswebcam (20140113-2) ...
Setting up fswebcam (20140113-2) ...
Processing triggers for man-db (2.11.2-2) ...
pi@buzzy:~ $ fswebcam -d /dev/video0 -r 640x480 test.jpg
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
No input was specified, using the first.
Error selecting input 0
VIDIOC_S_INPUT: Device or resource busy
pi@buzzy:~ $ sudo fswebcam -d /dev/video0 -r 640x480 test.jpg
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
No input was specified, using the first.
Error selecting input 0
VIDIOC_S_INPUT: Device or resource busy
pi@buzzy:~ $ nano /home/pi/mjpg-streamer.sh
pi@buzzy:~ $ cat /home/pi/mjpg-streamer.sh
#!/bin/bash
cd /home/pi/mjpg-streamer/mjpg-streamer-experimental/ || exit $?
LD_LIBRARY_PATH=.
#./mjpg_strea‌​mer -o "output_http.so -w ./www" -i "input_uvc.so"
./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30 -y"
pi@buzzy:~ $ sudo /home/pi/mjpg-streamer.sh
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: YUYV
 i: JPEG Quality......: 80
 i: TV-Norm...........: DEFAULT
Unable to set format: 1448695129 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
pi@buzzy:~ $ sudo nano /etc/systemd/system/mjpg-streamer.service
pi@buzzy:~ $ sudo systemctl daemon-reload
pi@buzzy:~ $ sudo systemctl enable mjpg-streamer.service --now
Created symlink /etc/systemd/system/multi-user.target.wants/mjpg-streamer.service → /etc/systemd/system/mjpg-streamer.service.
pi@buzzy:~ $ sudo systemctl status mjpg-streamer.service
× mjpg-streamer.service - MJPG-Streamer Service
     Loaded: loaded (/etc/systemd/system/mjpg-streamer.service; enabled; preset: enabled)
     Active: failed (Result: exit-code) since Sun 2025-08-17 20:57:11 EDT; 4s ago
   Duration: 11ms
    Process: 2191 ExecStart=/home/pi/mjpg-streamer.sh (code=exited, status=1/FAILURE)
   Main PID: 2191 (code=exited, status=1/FAILURE)
        CPU: 11ms
Aug 17 20:57:11 buzzy mjpg_streamer[2192]: MJPG-streamer [2192]: Frames Per Second.: 30
Aug 17 20:57:11 buzzy mjpg_streamer[2192]: MJPG-streamer [2192]: Format............: YUYV
Aug 17 20:57:11 buzzy mjpg_streamer[2192]: MJPG-streamer [2192]: JPEG Quality......: 80
Aug 17 20:57:11 buzzy mjpg_streamer[2192]: MJPG-streamer [2192]: TV-Norm...........: DEFAULT
Aug 17 20:57:11 buzzy mjpg_streamer[2192]: MJPG-streamer [2192]: init_VideoIn failed
Aug 17 20:57:11 buzzy systemd[1]: mjpg-streamer.service: Scheduled restart job, restart counter is at 5.
Aug 17 20:57:11 buzzy systemd[1]: Stopped mjpg-streamer.service - MJPG-Streamer Service.
Aug 17 20:57:11 buzzy systemd[1]: mjpg-streamer.service: Start request repeated too quickly.
Aug 17 20:57:11 buzzy systemd[1]: mjpg-streamer.service: Failed with result 'exit-code'.
Aug 17 20:57:11 buzzy systemd[1]: Failed to start mjpg-streamer.service - MJPG-Streamer Service.
pi@buzzy:~ $ dmesg | grep -i video
dmesg: read kernel buffer failed: Operation not permitted
pi@buzzy:~ $ sudo dmesg | grep -i video
[ 0.294948] pci 0000:00:02.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
[ 9.931174] videodev: Linux video capture interface: v2.00
[ 10.502384] usbcore: registered new interface driver uvcvideo
[ 11.767964] ACPI: video: Video Device [GFX0] (multi-head: yes rom: no post: no)
[ 11.768706] input: Video Bus as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/LNXVIDEO:00/input/input10
pi@buzzy:~ $ sudo apt install libjpeg-dev
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
libjpeg-dev is already the newest version (1:2.1.5-2).
The following packages were automatically installed and are no longer required:
  linux-compiler-gcc-10-x86 linux-headers-5.10.0-35-common linux-kbuild-5.10
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
pi@buzzy:~ $ ./mjpg_streamer -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080" -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30 -v^C
pi@buzzy:~ $ cd mjpg-streamer/mjpg-streamer-experimental/
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ ./mjpg_streamer -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080" -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30 -v"
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
UVC webcam grabber: option '-vf' requires an argument
 ---------------------------------------------------------------
 Help for input plugin..: UVC webcam grabber
 ---------------------------------------------------------------
 The following parameters can be passed to this plugin:
 [-d | --device ].......: video device to open (your camera)
 [-r | --resolution ]...: the resolution of the video device,
                          can be one of the following strings:
                          QQVGA QCIF CGA QVGA CIF PAL
                          VGA SVGA XGA HD SXGA UXGA
                          FHD
                          or a custom value like the following
                          example: 640x480
 [-f | --fps ]..........: frames per second
                          (camera may coerce to different value)
 [-q | --quality ] .....: set quality of JPEG encoding
 [-m | --minimum_size ].: drop frames smaller then this limit, useful
                          if the webcam produces small-sized garbage frames
                          may happen under low light conditions
 [-e | --every_frame ]..: drop all frames except numbered
 [-n | --no_dynctrl ]...: do not initalize dynctrls of Linux-UVC driver
 [-l | --led ]..........: switch the LED "on", "off", let it "blink" or leave
                          it up to the driver using the value "auto"
 [-t | --tvnorm ] ......: set TV-Norm pal, ntsc or secam
 [-u | --uyvy ] ........: Use UYVY format, default: MJPEG (uses more cpu power)
 [-y | --yuv ] ........: Use YUV format, default: MJPEG (uses more cpu power)
 [-fourcc ] ............: Use FOURCC codec 'argopt',
                          currently supported codecs are: RGB24, RGBP
 [-timestamp ]..........: Populate frame timestamp with system time
 [-softfps] ............: Drop frames to try and achieve this fps
                          set your camera to its maximum fps to avoid stuttering
 [-timeout] ............: Timeout for device querying (seconds)
 [-dv_timings] .........: Enable DV timings queriyng and events processing
 ---------------------------------------------------------------
 Optional parameters (may not be supported by all cameras):
 [-br ].................: Set image brightness (auto or integer)
 [-co ].................: Set image contrast (integer)
 [-sh ].................: Set image sharpness (integer)
 [-sa ].................: Set image saturation (integer)
 [-cb ].................: Set color balance (auto or integer)
 [-wb ].................: Set white balance (auto or integer)
 [-ex ].................: Set exposure (auto, shutter-priority, aperature-priority, or integer)
 [-bk ].................: Set backlight compensation (integer)
 [-rot ]................: Set image rotation (0-359)
 [-hf ].................: Set horizontal flip (true/false)
 [-vf ].................: Set vertical flip (true/false)
 [-pl ].................: Set power line filter (disabled, 50hz, 60hz, auto)
 [-gain ]...............: Set gain (auto or integer)
 [-cagc ]...............: Set chroma gain control (auto or integer)
 ---------------------------------------------------------------
input_init() return value signals to exit
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ ./mjpg_streamer -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080" -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30"
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: JPEG
 i: TV-Norm...........: DEFAULT
Unable to set format: 1196444237 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
pi@buzzy:~/mjpg-streamer/mjpg-streamer-experimental $ ./mjpg_streamer -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080" -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30 -y"
MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: 30
 i: Format............: YUYV
 i: JPEG Quality......: 80
 i: TV-Norm...........: DEFAULT
Unable to set format: 1448695129 res: 640x480
Init v4L2 failed !! exit fatal
 i: init_VideoIn failed
```

Ok! Killing the other processes and adding the service and restarting it after killing the process got it video0 working. Now lets make sure the exposure is high but auto exposure is on and frame rate is low to allow that to work well. This is for moonraker+fluidd

My version is better, and it works when run manually but not with systemctl start mjpg-streamer.
```
$journalctl -u mjpg-streamer
Aug 17 20:57:10 buzzy systemd[1]: Started mjpg-streamer.service - MJPG-Streamer Service.
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: starting application
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]: MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]:  i: Using V4L2 device.: /dev/video0
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]:  i: Desired Resolution: 640 x 480
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]:  i: Frames Per Second.: 30
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]:  i: Format............: YUYV
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]:  i: JPEG Quality......: 80
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]:  i: TV-Norm...........: DEFAULT
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]: Unable to set format: 1448695129 res: 640x480
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]: Init v4L2 failed !! exit fatal
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2182]:  i: init_VideoIn failed
Aug 17 20:57:10 buzzy systemd[1]: mjpg-streamer.service: Main process exited, code=exited, status=1/FAILURE
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: Using V4L2 device.: /dev/video0
Aug 17 20:57:10 buzzy systemd[1]: mjpg-streamer.service: Failed with result 'exit-code'.
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: Desired Resolution: 640 x 480
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: Frames Per Second.: 30
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: Format............: YUYV
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: JPEG Quality......: 80
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: TV-Norm...........: DEFAULT
Aug 17 20:57:10 buzzy mjpg_streamer[2182]: MJPG-streamer [2182]: init_VideoIn failed
Aug 17 20:57:10 buzzy systemd[1]: mjpg-streamer.service: Scheduled restart job, restart counter is at 1.
Aug 17 20:57:10 buzzy systemd[1]: Stopped mjpg-streamer.service - MJPG-Streamer Service.
Aug 17 20:57:10 buzzy systemd[1]: Started mjpg-streamer.service - MJPG-Streamer Service.
Aug 17 20:57:10 buzzy mjpg_streamer[2185]: MJPG-streamer [2185]: starting application
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2185]: MJPG Streamer Version: git rev: 310b29f4a94c46652b20c4b7b6e5cf24e532af39
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2185]:  i: Using V4L2 device.: /dev/video0
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2185]:  i: Desired Resolution: 640 x 480
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2185]:  i: Frames Per Second.: 30
Aug 17 20:57:10 buzzy mjpg-streamer.sh[2185]:  i: Format............: YUYV
```

WorkingDirectory isn't enough, you need the environment variable

Stay as close to the working code I said worked when run independently:

- paste my edited version of generated file:
```
[Unit]
Description=MJPG-Streamer Service
After=network.target dev-video0.device
Requires=network.target dev-video0.device

[Service]
User=pi
WorkingDirectory=/home/pi/mjpg-streamer/mjpg-streamer-experimental
Environment="LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer-experimental"
ExecStartPre=/bin/sh -c "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
ExecStart=/home/pi/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080" -i "input_uvc.so -d /dev/video0 -r 848x480 -f 2 -br 64"
#-ex auto: not available on GUCEE
#-br: brightness range is -64 to 64 on GUCEE
# GUCEE mjpeg formats: 848x480, 1280x720, others
ExecStop=/bin/sh -c "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
KillMode=control-group
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
Only fix the specific problems, don't keep refactoring, and stop talking about making a separate script, just focus on using systemd correctly. Here are the errors:
```
: enabled)


 Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
 Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
 Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
 Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
 MJPG-Streamer Service.
ice/start failed with result 'dependency'.
 Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
 Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}' | xargs -r kill -9 || true"
 MJPG-Streamer Service.
ice/start failed with result 'dependency'.
```

I already told you the output:
```
pi@buzzy:~ $ journalctl -u mjpg-streamer.service -b
Aug 19 08:33:54 buzzy systemd[1]: Dependency failed for mjpg-streamer.service - MJPG-Streamer Service.
Aug 19 08:33:54 buzzy systemd[1]: mjpg-streamer.service: Job mjpg-streamer.service/start failed with result 'dependency'.
Aug 19 13:20:13 buzzy systemd[1]: /etc/systemd/system/mjpg-streamer.service:10: Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}'>
Aug 19 13:20:13 buzzy systemd[1]: /etc/systemd/system/mjpg-streamer.service:13: Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}'>
Aug 19 13:24:13 buzzy systemd[1]: /etc/systemd/system/mjpg-streamer.service:10: Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}'>
Aug 19 13:24:13 buzzy systemd[1]: /etc/systemd/system/mjpg-streamer.service:13: Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}'>
Aug 19 13:26:02 buzzy systemd[1]: Dependency failed for mjpg-streamer.service - MJPG-Streamer Service.
Aug 19 13:26:02 buzzy systemd[1]: mjpg-streamer.service: Job mjpg-streamer.service/start failed with result 'dependency'.
Aug 19 13:30:19 buzzy systemd[1]: /etc/systemd/system/mjpg-streamer.service:10: Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}'>
Aug 19 13:30:19 buzzy systemd[1]: /etc/systemd/system/mjpg-streamer.service:15: Ignoring unknown escape sequences: "lsof /dev/video0 | awk 'NR>1 {print \$2}'>
Aug 19 13:31:55 buzzy systemd[1]: Dependency failed for mjpg-streamer.service - MJPG-Streamer Service.
Aug 19 13:31:55 buzzy systemd[1]: mjpg-streamer.service: Job mjpg-streamer.service/start failed with result 'dependency'.
```
We are not talking about overheating anymore, focus on these problems.

## [pressure advance]
Convert this to a wxPython program. Construct the filename field automatically whenever fields are edited if an "auto" checkbox below the filename edit box is checked (and construct the name when auto becomes checked). Instead of download, just save the file using a wx save file dialog defaulting to os expanduser ~/gcode/tests if present otherwise expand ~/gcode but if that doesn't exist then expand ~. Each time a file is saved, generated a preset with all fields. Use the filename, but instead of appending .gcode append .json. Make a presets drop-down box. If a preset is selected, load the json file. Store each preset json file in expanduser ~/.config/poikilospressureadvance/presets. Make the program modular and utilize the poikilospressureadvance/gcodefollower/init.py submodule (assume it it present and don't change it):

- paste gcodefollower.py (formerly `gcodefollower/__init__.py`)

Don't use placeholder code. The code where you said it was a placeholder is the core feature set! Translate the code as I said, referring to the files attached to the project, index.html and pressure_linear_advance.js especially. Instead of using the poikilospressureadvance folder, name the folder maniforge. Rename gcode_generator to pressureadvance.py, settings.py to slicersettings.py, Settings to SlicerSettings, ui_components.py to slicerwx.py, preset_manager.py to slicerpresets.py and assume all of the files are in a module called maniforge. Then rename main.py to pressure-advance.test. You are taking the html page along for the ride. Don't do that. Fully convert to wx and get rid of the wx.html2 dependency. Use wx.glcanvas.GLCanvas for the canvas. Generate the filename as follows: pa_pattern-214x214-210C-60C@10-50mms-0to1.1-step.025-r6.5at45 where 214x214 is bed size, 210 is extruder temperature, 60 is bed temperature, 10 is first layer speed, 50 is speed, 0 to 1.1 is start and end pressure advance, step.025 is step between 0 and 1.1, r6.5 is retraction length, 45 is retraction speed.

Change the round_nearest import to `from maniforge.mfmath import round_nearest`. Rename slicersettings.py to slicerpreset.py and the class from SlicerSettings to SlicerPreset. Also fix:
```
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 198, in create_setting_field
    ctrl = wx.TextCtrl(self.panel, value=str(getattr(self.settings, attr)), style=control_type)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: TextCtrl(): arguments did not match any overloaded call:
  overload 1: too many arguments
  overload 2: argument 'style' has unexpected type 'sip.wrappertype'
```
The constructor documentation for TextCtrl is:
> __init__ (self, parent, id=ID_ANY, value=’’, pos=DefaultPosition, size=DefaultSize, style=0, validator=DefaultValidator, name=TextCtrlNameStr)
> Constructor, creating and showing a text control.
> Parameters:
> parent (wx.Window) – Parent window. Should not be None.
> id (wx.WindowID) – Control identifier. A value of -1 denotes a default value.
> value (string) – Default text value.
> pos (wx.Point) – Text control position.
> size (wx.Size) – Text control size.
> style (long) – Window style. See wx.TextCtrl.
> validator (wx.Validator) – Window validator.
> name (string) – Window name.
> . . .
> The horizontal scrollbar (wx``wx.HSCROLL`` style flag) will only be created for multi-line text controls. Without a horizontal scrollbar, text lines that don’t fit in the control’s size will be wrapped (but no newline character is inserted). Single line controls don’t have a horizontal scrollbar, the text is automatically scrolled so that the insertion point is always visible.
whereas you probably didn't mean to use style:
> This class supports the following styles:
> wx.TE_PROCESS_ENTER: The control will generate the event wxEVT_TEXT_ENTER that can be handled by the program. Otherwise, i.e. either if this style not specified at all, or it is used, but there is no event handler for this event or the event handler called wx.Event.Skip to avoid overriding the default handling, pressing Enter key is either processed internally by the control or used to activate the default button of the dialog, if any.
> wx.TE_PROCESS_TAB: Normally, TAB key is used for keyboard navigation and pressing it in a control switches focus to the next one. With this style, this won’t happen and if the TAB is not otherwise processed (e.g. by wxEVT_CHAR event handler), a literal TAB character is inserted into the control. Notice that this style has no effect for single-line text controls when using wxGTK.
> wx.TE_MULTILINE: The text control allows multiple lines. If this style is not specified, line break characters should not be used in the controls value.
> wx.TE_PASSWORD: The text will be echoed as asterisks.
> wx.TE_READONLY: The text will not be user-editable.
> wx.TE_RICH: Use rich text control under MSW, this allows having more than 64KB of text in the control. This style is ignored under other platforms and it is recommended to use wx.TE_RICH2 instead of it under MSW.
> wx.TE_RICH2: Use rich text control version 2.0 or higher under MSW, this style is ignored under other platforms. Note that this style may be turned on automatically even if it is not used explicitly when creating a text control with a long (i.e. much more than 64KiB) initial text, as creating the control would simply fail in this case under MSW if neither this style nor wx.TE_RICH is used.
> wx.TE_AUTO_URL: Highlight the URLs and generate the TextUrlEvents when mouse events occur over them.
> wx.TE_NOHIDESEL: By default, the Windows text control doesn’t show the selection when it doesn’t have focus - use this style to force it to always show it. It doesn’t do anything under other platforms.
> wx.HSCROLL: A horizontal scrollbar will be created and used, so that text won’t be wrapped.
> wx.TE_NO_VSCROLL: For multiline controls only: vertical scrollbar will never be created. This limits the amount of text which can be entered into the control to what can be displayed in it under wxMSW but not under wxGTK or wxOSX. Currently not implemented for the other platforms.
> wx.TE_LEFT: The text in the control will be left-justified (default).
> wx.TE_CENTRE: The text in the control will be centered (wxMSW, wxGTK, wxOSX).
> wx.TE_RIGHT: The text in the control will be right-justified (wxMSW, wxGTK, wxOSX).
> wx.TE_DONTWRAP: Same as wx.HSCROLL style: don’t wrap at all, show horizontal scrollbar instead.
> wx.TE_CHARWRAP: For multiline controls only: wrap the lines too long to be shown entirely at any position (wxUniv, wxGTK, wxOSX).
> wx.TE_WORDWRAP: For multiline controls only: wrap the lines too long to be shown entirely at word boundaries (wxUniv, wxMSW, wxGTK, wxOSX).
> wx.TE_BESTWRAP: For multiline controls only: wrap the lines at word boundaries or at any other character if there are words longer than the window width (this is the default).
> TE_CAPITALIZE: On PocketPC and Smartphone, causes the first letter to be capitalized.
>
> Note that alignment styles (wx``wx.TE_LEFT``, wx.TE_CENTRE and wx.TE_RIGHT) can be changed dynamically after control creation on wxMSW, wxGTK and wxOSX. wx.TE_READONLY, wx.TE_PASSWORD and wrapping styles can be dynamically changed under wxGTK but not wxMSW. The other styles can be only set during control creation.

Change the round_nearest import to from maniforge.mfmath import round_nearest. Rename slicersettings.py to slicerpreset.py and the class from SlicerSettings to SlicerPreset. Also fix:
`   File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 198, in create_setting_field  ctrl = wx.TextCtrl(self.panel, value=str(getattr(self.settings, attr)), style=control_type)  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  TypeError: TextCtrl(): arguments did not match any overloaded call:  overload 1: too many arguments  overload 2: argument 'style' has unexpected type 'sip.wrappertype'       `
The constructor documentation for TextCtrl is:
> **\_\_init\_\_** _(self, parent, id=ID\_ANY, value=’’, pos=DefaultPosition, size=DefaultSize, style=0, validator=DefaultValidator, name=TextCtrlNameStr)_
> Constructor, creating and showing a text control.
> Parameters:
> -   **parent** ([_wx.Window_](https://docs.wxpython.org/wx.Window.html#wx.Window "wx.Window")) – Parent window. Should not be `None`.
> -   **id** (_wx.WindowID_) – Control identifier. A value of -1 denotes a default value.
> -   **value** (_string_) – Default text value.
> -   **pos** ([_wx.Point_](https://docs.wxpython.org/wx.Point.html#wx.Point "wx.Point")) – Text control position.
> -   **size** ([_wx.Size_](https://docs.wxpython.org/wx.Size.html#wx.Size "wx.Size")) – Text control size.
> -   **style** (_long_) – Window style. See [wx.TextCtrl](https://docs.wxpython.org/wx.TextCtrl.html#wx-textctrl).
> -   **validator** ([_wx.Validator_](https://docs.wxpython.org/wx.Validator.html#wx.Validator "wx.Validator")) – Window validator.
> -   **name** (_string_) – Window name.
>
> Note that alignment styles (wxwx.TE\_LEFT, wx.TE\_CENTRE and wx.TE\_RIGHT) can be changed dynamically after control creation on wxMSW, wxGTK and wxOSX. wx.TE\_READONLY, wx.TE\_PASSWORD and wrapping styles can be dynamically changed under wxGTK but not wxMSW. The other styles can be only set during control creation.


You have to check the type in on_field_change and use the correct call depending on the widget type. For example, if type of event.GetEventObject() is a wx.Choice, the correct way to get the value is event.GetString()

I said event.GetString() and I meant it. widget.GetString in the case of wx.Choice requires the index. Also, try to fix round_nearest so the maximum recursion depth is not exceeded. If I do:
```
        try:
            return round_nearest(increased) / multiplier
        except RecursionError:
            print(f"increased={increased}, multiplier={multiplier}, original={original}")
            raise
```
The output is
```
increased=0.0001, multiplier=0.001, original=(0.1, -3)
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 223, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 256, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 174, in generate_gcode
    z_hop()
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 132, in z_hop
    move(z=state['cur_z'] + self.settings.zhop_height, comment="z hop")
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 109, in move
    cmd.append(f"Z{self.round10(z, self.settings.Z_round)}")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 13, in round10
    return round_nearest(value, decimals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/mfmath.py", line 71, in round_nearest
    return _round_nearest(*args)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/mfmath.py", line 115, in _round_nearest
    return round_nearest(increased) / multiplier
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/mfmath.py", line 70, in round_nearest
    set_original(args)
RecursionError: maximum recursion depth exceeded
```

So, if precision is negative handle that using a separate int-based algorithm and round as necessary to match the behavior of the usage in the original html+JavaScript program.

Don't use round or you will end up with banker's rounding. If ones place precision is required, do
```
int(increased+.5)
```

```
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 232, in update_filename
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 185, in generate_filename
RecursionError: maximum recursion depth exceeded
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
    return apport_excepthook(binary, exc_type, exc_obj, exc_tb)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 79, in apport_excepthook
    binary = os.path.realpath(binary)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 435, in realpath
RecursionError: maximum recursion depth exceeded
Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.update_filename()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 232, in update_filename
    self.settings.filename = self.settings.generate_filename()
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 185, in generate_filename
    return (f"pa_pattern-{self.bed_x}x{self.bed_y_value()}-"
                                       ^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 223, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 256, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 141, in generate_gcode
    add_gcode(self.settings.start_gcode_text(replace=True))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 135, in start_gcode_text
    gcode = re.sub(r'M104 S0.*?\n', '', gcode)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 186, in sub
    return _compile(pattern, flags).sub(repl, string, count)
           ^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
    return apport_excepthook(binary, exc_type, exc_obj, exc_tb)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 79, in apport_excepthook
    binary = os.path.realpath(binary)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 435, in realpath
  File "<frozen posixpath>", line 459, in _joinrealpath
  File "<frozen posixpath>", line 63, in isabs
RecursionError: maximum recursion depth exceeded
Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 223, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 256, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 141, in generate_gcode
    add_gcode(self.settings.start_gcode_text(replace=True))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 135, in start_gcode_text
    gcode = re.sub(r'M104 S0.*?\n', '', gcode)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 186, in sub
    return _compile(pattern, flags).sub(repl, string, count)
           ^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
```

When "round" is selected:
```
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
RecursionError: maximum recursion depth exceeded

Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 221, in on_field_change
RecursionError: maximum recursion depth exceeded
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 269, in validate_and_update
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 27, in validate
RecursionError: maximum recursion depth exceeded
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
    return apport_excepthook(binary, exc_type, exc_obj, exc_tb)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 79, in apport_excepthook
    binary = os.path.realpath(binary)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 435, in realpath
RecursionError: maximum recursion depth exceeded

Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 269, in validate_and_update
    valid, errors = self.generator.validate()
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 27, in validate
    for key, value in self.settings.to_dict().items():
                      ^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 144, in start_gcode_text
    gcode = re.sub(pattern, '', gcode, flags=re.MULTILINE)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 186, in sub
    return _compile(pattern, flags).sub(repl, string, count)
           ^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 271, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 141, in generate_gcode
    add_gcode(self.settings.start_gcode_text(replace=True))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 148, in start_gcode_text
    gcode = '\n'.join(line for line in lines if not re.match(pattern, line))
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 148, in <genexpr>
    gcode = '\n'.join(line for line in lines if not re.match(pattern, line))
                                                    ^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
    return apport_excepthook(binary, exc_type, exc_obj, exc_tb)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 79, in apport_excepthook
    binary = os.path.realpath(binary)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 435, in realpath
  File "<frozen posixpath>", line 459, in _joinrealpath
  File "<frozen posixpath>", line 63, in isabs
RecursionError: maximum recursion depth exceeded

Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 144, in start_gcode_text
    gcode = re.sub(pattern, '', gcode, flags=re.MULTILINE)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 186, in sub
    return _compile(pattern, flags).sub(repl, string, count)
           ^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 271, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 141, in generate_gcode
    add_gcode(self.settings.start_gcode_text(replace=True))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 148, in start_gcode_text
    gcode = '\n'.join(line for line in lines if not re.match(pattern, line))
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 148, in <genexpr>
    gcode = '\n'.join(line for line in lines if not re.match(pattern, line))
                                                    ^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 144, in start_gcode_text
    gcode = re.sub(pattern, '', gcode, flags=re.MULTILINE)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 186, in sub
    return _compile(pattern, flags).sub(repl, string, count)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 283, in _compile
    flags = flags.value
            ^^^^^^^^^^^
  File "/usr/lib/python3.12/enum.py", line 212, in __get__
    return self.fget(instance)
           ^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 271, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 141, in generate_gcode
    add_gcode(self.settings.start_gcode_text(replace=True))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 148, in start_gcode_text
    gcode = '\n'.join(line for line in lines if not re.match(pattern, line))
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/slicerpreset.py", line 148, in <genexpr>
    gcode = '\n'.join(line for line in lines if not re.match(pattern, line))
                                                    ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 167, in match
    return _compile(pattern, flags).match(string)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 298, in _compile
    if not _compiler.isstring(pattern):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
```

It is not a circular symlink, and there is no need to do recursion the way you have. It isn't apport's fault either, you just made illogical code, that's all. Look again at the original JavaScript code (Ellis Pressure advance) and at wxPython (and other Python) documentation and examples and do it correctly. The problem isn't in my environment, nor with changes I made to your code. It is your fault.

```
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
RecursionError: maximum recursion depth exceeded
Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 221, in on_field_change
RecursionError: maximum recursion depth exceeded
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 269, in validate_and_update
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 27, in validate
RecursionError: maximum recursion depth exceeded
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
    return apport_excepthook(binary, exc_type, exc_obj, exc_tb)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 79, in apport_excepthook
    binary = os.path.realpath(binary)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 435, in realpath
RecursionError: maximum recursion depth exceeded
Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 269, in validate_and_update
    valid, errors = self.generator.validate()
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 27, in validate
    for key, value in self.settings.to_dict().items():
                      ^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 271, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 167, in generate_gcode
    move(x=x_offset, y=y_offset, f=self.settings.speed_travel, comment="move to start")
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 105, in move
    cmd.append(f"X{self.round10(x, self.settings.XY_round)}")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 13, in round10
    return round_nearest(value, decimals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
    return apport_excepthook(binary, exc_type, exc_obj, exc_tb)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 79, in apport_excepthook
    binary = os.path.realpath(binary)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 435, in realpath
  File "<frozen posixpath>", line 459, in _joinrealpath
  File "<frozen posixpath>", line 63, in isabs
RecursionError: maximum recursion depth exceeded
Original exception was:
Traceback (most recent call last):
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 222, in on_field_change
    self.validate_and_update()
  File "/home/owner/git/maniforge/maniforge/slicerwx.py", line 271, in validate_and_update
    gcode = "\n".join(errors) if errors else self.generator.generate_gcode()
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 167, in generate_gcode
    move(x=x_offset, y=y_offset, f=self.settings.speed_travel, comment="move to start")
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 105, in move
    cmd.append(f"X{self.round10(x, self.settings.XY_round)}")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owner/git/maniforge/maniforge/pressureadvance.py", line 13, in round10
    return round_nearest(value, decimals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
```


