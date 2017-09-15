#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import time

import modules.IF0.__main__ as IF0Mod
import modules.TXT0.__main__ as TXT0Mod
from pallet import *

IF0 = IF0Mod.Interface()
F1 = IF0.F1
F2 = IF0.F2
Sled = IF0.Sled

TXT0 = TXT0Mod.Interface()
TrafficLights = TXT0.TrafficLights
HRL = TXT0.HRL

lastInit = 0


def INITall():
    HRL.initialize()
    Sled.initialize(home=False)
    F1.initialize()
    F2.initialize()
    Sled.home()
    HRL.waitInitialize()
    lastInit = time.time()


INITall()
palletStack = []
print("Please check that no pallets are in the storage and the program has just started!")
input("Press enter to continue!")
print("Now you can add pallets!")
while True:
    more = input("Do you want to add more pallets? enter 'y' for yes, press enter to continue!")
    try:
        if not more.lower()[0] == 'y':
            break
    except:
        break
    print("Put the new pallet on the belt and press any key to continue!")
    input()
    Sled.goPosBelt(Sled.POSBELTHANDOVER)
    F1.moveForward()
    Sled.moveLeft()
    F2.moveLeft()
