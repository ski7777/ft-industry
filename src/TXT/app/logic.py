#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from _thread import start_new_thread    # import simple thread starter
import com                              # import model´s communicaton lib
# import basic functions of python
import time

pallet_stack = {}  # initialize pallet stack
push_button = com.push_button()         # initialize push button
# initialize traffic lights
traffic_lights = com.traffic_lights()
traffic_lights.set_pattern('red', [True, True, True, True])
traffic_lights.set_new()
# initialize IF1 communication
IF1 = com.com_stack()
IF1.setio(1, 1)
IF1.start_recieving()
# initialize TX communication
TX = com.com_stack()
TX.setio(2, 2)
TX.start_recieving()
# initialize model´s stations´ variables
global F1
global FS
global FS_POS
global F2
F1 = 0
FS = 0
FS_POS = 0  # Front Site is 0, Rear is 1
F2 = 0
bash = com.bash


def HRL_send(self, ea, nbr):
    # Send pallet_ID and input/output to TX
    # Initiate communication
    if ea == True:
        rnd = TX.start_trans(8, False)
    elif ea == False:
        rnd = TX.start_trans(5, False)
    else:
        # Return if data is invalid
        return
    if rnd == None:
        # retun in case of communication problems
        show_error('0x02 (TX)')
        return
    else:
        # Convert pallet_ID to special communication
        if nbr >= 1 and nbr <= 25:
            nbr0 = 2
        elif nbr >= 26 and nbr <= 50:
            nbr0 = 5
            nbr -= 25

        if nbr >= 1 and nbr <= 5:
            nbr1 = 2
        elif nbr >= 5 and nbr <= 10:
            nbr1 = 5
            nbr -= 5
        elif nbr >= 11 and nbr <= 15:
            nbr1 = 8
            nbr -= 10
        elif nbr >= 16 and nbr <= 20:
            nbr1 = 11
            nbr -= 15
        elif nbr >= 21 and nbr <= 25:
            nbr1 = 14
            nbr -= 20

        if nbr == 1:
            nbr2 = 2
        elif nbr == 2:
            nbr2 = 5
        elif nbr == 3:
            nbr2 = 8
        elif nbr == 4:
            nbr2 = 11
        elif nbr == 5:
            nbr2 = 14
        print('DATA TO HRL:' + str(nbr0), str(nbr1), str(nbr2))
        # send pallet_ID to TX
        time.sleep(0.5)
        TX.add_trans(rnd, nbr0, False)
        time.sleep(0.1)
        TX.add_trans(rnd, nbr1, False)
        time.sleep(0.1)
        TX.add_trans(rnd, nbr2, False)
        TX.kill_trans(rnd)


def abort_new_pallet():
    # clear F1
    global F1
    F1 = 0


def generate_palled_ID():
    pallet_ID = 1
    while str(pallet_ID) in pallet_stack.keys():
        pallet_ID += 1
    return(pallet_ID)


def new_pallet(ID, order):
    # generate new pallet with order data and set it to F1
    global F1
    F1 = ID
    pallet_stack[str(ID)] = [time.time(), [order]]
    # TEST; print out all pallets
    print(pallet_stack)
