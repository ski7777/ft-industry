#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import com                              # import model´s communicaton lib
import json                             # import json lib for routing map
from _thread import start_new_thread    # import simple thread starter
# import basic functions of python
import time
from pathlib import Path

pallet_stack = {}  # initialize pallet stack
push_button = com.push_button(8)         # initialize push button
# initialize traffic lights
traffic_lights = com.traffic_lights(4, 5, 6)
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
# read station data from file
global model_map
model_map = json.loads(Path("stations.json").read_text())
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
        bash.addData("logic", 'DATA TO HRL:' + str(nbr0), str(nbr1), str(nbr2))
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
    model_map["stamp"]["pallet"] = 0


def generate_palled_ID():
    pallet_ID = 1
    while str(pallet_ID) in pallet_stack.keys():
        pallet_ID += 1
    return(pallet_ID)


def new_pallet(ID, order):
    # generate new pallet with order data and set it to F1
    model_map["stamp"]["pallet"] = ID
    # state:
    # 0: stuck
    # 1: moving
    pallet_stack[str(ID)] = {"time": time.time(), "data": order, "state": 0, "route": []}


def listPalletsByTime():
    data = {}
    for x, y in pallet_stack.items():
        data[y["time"]] = x
    ret_data = []
    for x in sorted(data):
        ret_data.append(data[x])
    return(ret_data)


def locatePallet(ID):
    for x, y in model_map.items():
        if y["pallet"] == int(ID):
            return(x)
    return(None)


def RoutePlanner(ID, dest):
    start = locatePallet(ID)
    route = []
    # The carriage is the center of the model so we have always a route which constits of two parts
    # build a route to the carriage
    pos = start
    while pos != "carriage":
        route.append(pos)
        pos = model_map[pos]["to_carriage"]
    route.pop(0)
    # no we reached the carriage
    # build the route from the carriage to the destination
    _rte = []
    pos = dest
    while pos != "carriage":
        _rte.append(pos)
        pos = model_map[pos]["to_carriage"]
    _rte.reverse()
    return(route + ["carriage"] + _rte)


def movePallet(ID):
    # get data
    dep = locatePallet(ID)
    dest = pallet_stack[ID]["route"][0]

    pallet_stack[ID]["state"] = 1  # set state to moving
    calls = {
        "stamp": {
            "carriage": [IF1, 14, True]
        },
        "carriage": {
            "scanner": [IF1, 11, True]
        },
        "scanner": {}}
    try:
        cmd = calls[dep][dest]  # get command ID
    except:
        bash.addData("info", "No route!")
        print(dep)
        print(dest)
        return
    bash.addData("info", "Route: " + dep + " -> " + dest + " CMD: " + str(cmd))
    if cmd[0].start_trans(cmd[1], cmd[2]) == None:
        bash.addData("info", "ERROR sending data")
    model_map[dep]["pallet"] = 0
    model_map[dest]["pallet"] = int(ID)
    pallet_stack[ID]["route"].pop(0)
    pallet_stack[ID]["state"] = 0


def logic_thread():
    while True:
        work_order = listPalletsByTime()  # calculate work order
        # print on bash
        bash.deleteData("logic")
        bash.addData("logic", "Work Order: " + str(work_order))
        bash.addData("logic", "Locations:")
        bash.addData("logic", json.dumps(model_map, indent=4, sort_keys=True))
        # print locations for each pallet
        if work_order != []:
            bash.addData("logic", "Locations:")
            for x in work_order:
                try:
                    bash.addData("logic", x + ": " + locatePallet(x) + ", " + str(pallet_stack[x]["route"]))
                except:
                    pass
        # calculate routes (to HRL) for each pallet
        for x in work_order:
            if pallet_stack[x]["route"] == []:
                pallet_stack[x]["route"] = RoutePlanner(x, "scanner")
                bash.addData("info", pallet_stack[x]["route"])
                free = True
                for y in pallet_stack[x]["route"]:
                    if model_map[y]["pallet"] != 0:
                        free = False
                        bash.addData("info", y)
                if free:
                    for y in pallet_stack[x]["route"]:
                        model_map[y]["pallet"] = 2000
                else:
                    pallet_stack[x]["route"] = []
        # move pallets to their destination
        for x in work_order:
            # check whether pallet is movaeable
            if pallet_stack[x]["route"] != [] and pallet_stack[x]["state"] == 0:
                start_new_thread(movePallet, (x,))
        time.sleep(0.1)
