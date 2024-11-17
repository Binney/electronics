# answerphone

## Setup

On a Pi Zero

### Install Pi OS on the Zero

Use the imager https://www.raspberrypi.com/software/

Step through the install wizard

Pick a username and password

Connect to wifi

`sudo raspi-conifg` -> Interface Options -> SSH -> Enable -> yes

Mouseover the wifi logo in the top right corner, note the IP

On your main computer, connect to the same network and do `ssh [username]@[ip]`, enter the same password you chose earlier

OK, ready to go!

### Disable HDMI audio

Had a load of problems with pi wanting to play through HDMI rather than over USB, so just disable it now.

```
sudo nano /boot/firmware/config.txt
```

Look for the line that says

```
dtoverlay=vc4-kms-v3d
```

and replace it with

```
dtoverlay=vc4-kms-v3d,noaudio
```

then reboot.

### Get the code running

Git clone into this repository

cd to the folder this README is in

```
sudo dpkg --configure -a # Update apt packages
sudo apt-get install portaudio10-dev # Prerequisite for pyaudio
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Now you can run the actual code:

```
sudo .venv/bin/python answerphone.py # keyboard requires sudo
```

### Get it to run on autostart

You can probably do this with wayfire.ini but my pi install wasn't having any of it, so let's use x11 instead

`sudo raspi-config` -> Advanced options -> Wayland -> X11 -> OK -> reboot

```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

Add a line at the bottom saying

```
@bash /home/dreamcat/electronics/answerphone/autostart.sh
```

Save and reboot

### Connect during the event

(Optional but recommended)

Set up a local hotspot so you can connect directly to the pi while it's on and check it's ok/troubleshoot.

Easiest to do through the desktop and you won't be able to do it all via ssh anyway as it involves disconnecting from the wifi.

Wifi icon in the top right corner of the screen -> click -> Advanced Options -> Create Wireless Hotspot -> WPA & WPA2 (can't seem to get WPA3 to work with a Zero?) -> choose a name and password you're satisfied aren't hackable during the event -> OK.

Note the IP address of the pi (hover over the wifi icon again).

Now you can connect to the pi wifi from another device and SSH in - from a laptop, or even a phone with something like juicessh installed.

## Troubleshooting

### I'm getting a load of "Input overflowed" errors when I start recording

The script has made some wrong assumptions about your hardware, try changing `chunk` or `fs`

https://stackoverflow.com/questions/10733903

### It's just super quiet

Well turn the volume up then

Do that while you have it plugged into a screen, or via ssh:

```
amixer scontrols
```

Note the control names, I had one called `Master` so I did

```
amixer -M sget Master
```

which said they were both at 40%, up that to 100%:

```
amixer -q -M sset Master 100%
```
