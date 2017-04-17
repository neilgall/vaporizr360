# Drive a Nikko Vaporizr using the Xbox360 controller!

The receiver board died in our Nikko Vaporizr so I swapped it out with the electronics from
another RC vehicle. Unfortunately the Nikko has separate left/right drive with no steering
and the replacement transmitter has conventional forward/back/left/right controls, with the
switch placements hard-wired on the circuit board. The only thing for it was to build a
Raspberry Pi controller and drive the car using an Xbox 360 controller. We'll aim for authentic
Forza controls!

Four GPIO signals from the Raspberry Pi are wired via simple NPN transistor circuits to the
left/right/forward/backwards switches on the transmitter circuit. These correspond to the
independent left and right forward and backwards drives on the Nikko. I have no idea what
switching frequency the RC electronics are capable of so we'll just do fake PWM in software
for now.

The code here relies on `xboxdrv` on the Raspberry Pi and Steven Jacobs' xbox.py Python
interface. It polls the controller at about 100Hz and updates the GPIO outputs accordingly.
The algorithm is very primitive for now, but we'll continue to work on it.
