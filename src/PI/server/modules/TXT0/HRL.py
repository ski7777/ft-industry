#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import time


class HRL():
    def __init__(self, com):
        self.com = com
        self.isInit = False
        self.Sled = None
        self.F2 = None

    def initialize(self, Sled, F2):
        self.Sled = Sled
        self.F2 = F2
        # TODO: Add init command or wait for fttxpy ;-)
        # send(...)
        time.sleep(2)
        self.isInit = True

    def waitInitialize(self):
        while not self.isInit:
            pass

    def moveIn(self, pallet):
        pos = pallet.pos
        assert(pos == pallet.POSF2)
        self.send(True, pallet.id)
        pallet.pos = pallet.POSHRL
        time.sleep(55)
        # TODO: Add finished button or wait for fttxpy ;-)

    def moveOut(self, pallet):
        pos = pallet.pos
        assert(pos == pallet.POSHRL)
        self.send(False, pallet.id)
        self.Sled.goPosBelt(self.Sled.POSBELTHANDOVER)
        self.F2.goFromHRL()
        self.Sled.goPosBelt(self.Sled.POSBELTHANDOVER)
        self.F2.waitHRLPallet()
        time.sleep(15)
        self.F2.moveRightTime(10)
        self.F2.initialize()
        pallet.pos = pallet.POSF2

    def send(self, ea, nbr):
        # Send pallet_ID and input/output to self.com
        # Initiate communication
        if ea == True:
            rnd = self.com.start_trans(8, False)
        elif ea == False:
            rnd = self.com.start_trans(5, False)
        else:
            # Return if data is invalid
            return
        if rnd == None:
            # retun in case of communication problems
            print('0x02 (self.com)')
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
            # send pallet_ID to self.com
            time.sleep(0.5)
            self.com.add_trans(rnd, nbr0, False)
            time.sleep(0.1)
            self.com.add_trans(rnd, nbr1, False)
            time.sleep(0.1)
            self.com.add_trans(rnd, nbr2, False)
            self.com.kill_trans(rnd)
