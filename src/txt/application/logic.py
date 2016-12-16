#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from _thread import start_new_thread
pallet_stack = {}
import com
push_button = com.push_button()
traffic_lights = com.traffic_lights()
traffic_lights.set_pattern('red', [True, True, True, True])
traffic_lights.set_new()
IF1 = com.com_stack()
IF1.setio(1, 1)
IF1.start_recieving()
TX = com.com_stack()
TX.setio(2, 2)
TX.start_recieving()
global F1
global FS
global FS_POS
global F2
F1 = 0
FS = 0
FS_POS = 0 #Front Site is 0, Rear is 1
F2 = 0

def wait_for_new_pallet():
    global F1
    while F1 != 0:
        pass
    F1 = 1000
def abort_new_pallet():
    global F1
    F1 = 0
def generate_palled_ID():
    pallet_ID = 1
    while str(pallet_ID) in pallet_stack.keys():
        pallet_ID += 1
    reurn(pallet_ID)

def new_pallet(ID, order):
    global F1
    F1 = ID
    pallet_stack[str(pallet_rnd)] = [time.time(), [order]]
