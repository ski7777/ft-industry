#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import threading
import time

class TrafficLights(threading.Thread):

    def __init__(self, txt, r, y, g):
        threading.Thread.__init__(self)
        self.red = txt.output(r)
        self.yellow = txt.output(y)
        self.green = txt.output(g)
        self.data = {'red': [self.red, None, [False, False, False, False]],
                     'yellow': [self.yellow, None, [False, False, False, False]],
                     'green': [self.green, None, [False, False, False, False]]}
        self.data_new = {'red': [False, False, False, False],
                         'yellow': [False, False, False, False],
                         'green': [False, False, False, False]}
        self.start()

    def set_pattern(self, _color, _list):
        if _color in self.data.keys():
            self.data_new[_color] = _list

    def set_new(self):
        for _color, _data in self.data_new.items():
            self.data[_color][2] = _data

    def get_level(self, v):
        if v == True:
            return(512)
        else:
            return(0)

    def run(self):
        while True:
            for phase in [0, 1, 2, 3]:
                for light in self.data.keys():
                    if self.data[light][1] != self.data[light][2][phase]:
                        self.data[light][1] = self.data[light][2][phase]
                        self.data[light][0].setLevel(self.get_level(self.data[light][2][phase]))
                time.sleep(0.125)
                for light in self.data.keys():
                    if self.data[light][1] != self.data[light][2][phase]:
                        self.data[light][1] = self.data[light][2][phase]
                        self.data[light][0].setLevel(self.get_level(self.data[light][2][phase]))
                time.sleep(0.125)
