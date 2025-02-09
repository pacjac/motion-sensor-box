# YASB Temporal synchronisations

In order to enable precise, distributed measurements with multiple YASB boxes, gnss time synchronisation is required (see [gpsd.md](gpsd.md) for details). 

To set the system wide clock precisly, yasb relies on chrony and it's daemon chronyd. 

## Prerequisities

Please make sure you have a functioning GNSS sensor with a pps device. If not, please refere to [gpsd.md](gpsd.md)

## Installation

Install chrony from the distribution sources:

```
sudo apt install chrony -y
```

## Configuration

Chronys configuration file can be found at /etc/chrony.conf

Please paste the following into your configuration file

```
# Welcome to the chrony configuration file. See chrony.conf(5) for more
# information about usuable directives.
pool 2.debian.pool.ntp.org iburst

server 0.pool.ntp.org
server 1.pool.ntp.org
server 2.pool.ntp.org

initstepslew 30 0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org

# SHM0 from gpsd is the NEMA data at 4800bps, so is not very accurate
refclock SHM 0  delay 0.5 refid NEMA

# SHM1 from gpsd (if present) is from the kernel PPS_LDISC
# module.  It includes PPS and will be accurate to a few ns
# refclock SHM 1 offset 0.0 delay 0.1 refid NEMA+

# SOCK protocol also includes PPS data and 
# it also provides time within a few ns
refclock SOCK /var/run/chrony.ttySC0.sock delay 0.0 refid SOCK

# PPS is from the /dev/pps0 device.  Note that
# chronyd creates the /var/run/chrony.ttyS1.sock device, but
# gpsd creates the /dev/pps0 device
# openrc rules start gpsd /after/ chronyd, so /dev/pps0 
#   is not created until after chronyd is started
#   If you want to use pps0, either edit the openrc rules
#   or add this source after gpsd is started

refclock PPS /dev/pps0 refid PPS


# If you see something in ns... its good.
#          1 second =
#       1000 ms =
#    1000000 us =
# 1000000000 ns

logchange 0.5
local stratum 10

logdir /var/log/chrony

keyfile /etc/chrony/chrony.keys
commandkey 10

dumpdir /var/log/chrony
driftfile /var/log/chrony/chrony.drift

allow all

# This directive specify the location of the file containing ID/key pairs for
# NTP authentication.
keyfile /etc/chrony/chrony.keys

# Uncomment the following line to turn logging on.
log tracking measurements statistics

# Log files location.
logdir /var/log/chrony

# Stop bad estimates upsetting machine clock.
maxupdateskew 100.0

# This directive enables kernel synchronisation (every 11 minutes) of the
# real-time clock. Note that it can’t be used along with the 'rtcfile' directive.
rtcsync

# Step the system clock instead of slewing it if the adjustment is larger than
# one second, but only in the first three clock updates.
makestep 1 3

```
