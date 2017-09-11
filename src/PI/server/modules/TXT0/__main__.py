#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from ftrobopy import ftrobopy
from .TrafficLights import TrafficLights


class Interface():
    def __init__(self):
        self.IF = ftrobopy('10.16.1.4')
        self.TrafficLights = TrafficLights(self.IF, 4, 5, 6)
        self.TrafficLights.set_pattern('red', [True, True, True, True])
        self.TrafficLights.set_new()
