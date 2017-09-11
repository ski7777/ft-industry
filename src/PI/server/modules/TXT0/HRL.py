#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import time


class HRL():
    def __init__(self, com):
        self.com = com

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
