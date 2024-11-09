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

### Git clone into this repository

cd to the folder this README is in

```
python -m venv .venv
.venv/bin/pip install requirements.txt
sudo .venv/bin/python answerphone.py # keyboard requires sudo
```

## Troubleshooting

### I'm getting a load of "Input overflowed" errors when I start recording

The script has made some wrong assumptions about your hardware, try changing `chunk` or `fs`

https://stackoverflow.com/questions/10733903
