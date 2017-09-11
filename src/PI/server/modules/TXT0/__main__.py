#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from ftrobopy import ftrobopy
import time
from .TrafficLights import TrafficLights
from .com import com_stack as ComStack
from .HRL import HRL


class Interface():
    def __init__(self):
        self.IF = ftrobopy('10.16.1.4')
        self.TrafficLights = TrafficLights(self.IF, 4, 5, 6)
        self.TrafficLights.set_pattern('red', [True, True, True, True])
        self.TrafficLights.set_new()
        self.TX = ComStack(self.IF)
        self.TX.setio(2, 2)
        self.TX.start_recieving()
        self.HRL = HRL(self.TX)
