#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import robointerface as RI
import time


class Interface():
    def __init__(self):
        self.IF = RI.RoboInterface()
        self.F1 = Belt(1, 1, self.IF)
        self.F2 = F2(4, 5, self.IF)
        self.Sled = Sled(self.IF)


class Sled():
    def __init__(self, IF):
        self.MotSled = 3
        self.MotBelt = 2
        self.ButEnd = 4
        self.PhotoBelt = 3
        self.IF = IF

        self.isInit = False

    def initialize(self, home=True):
        if not self.IF.Digital(self.ButEnd):
            self.IF.SetMotor(self.MotSled, iSpeed=-3)
            while not self.IF.Digital(self.ButEnd):
                pass
        self.IF.SetMotor(self.MotSled)
        time.sleep(1)
        self.IF.SetMotor(self.MotSled, 's')

        self.IF.SetMotor(self.MotBelt)
        time.sleep(0.5)
        while True:
            if not self.IF.Digital(self.PhotoBelt):
                time.sleep(0.01)
                if not self.IF.Digital(self.PhotoBelt):
                    self.IF.SetMotor(self.MotBelt, 's')
                    break
        if home:
            self.home()

    def home(self):
        if not self.IF.Digital(self.ButEnd):
            self.IF.SetMotor(self.MotSled, iSpeed=-3)
            while not self.IF.Digital(self.ButEnd):
                pass
            self.IF.SetMotor(self.MotSled, 's')


class Belt():
    def __init__(self, Mot, PhotoInit, IF):
        self.Mot = Mot
        self.PhotoInit = PhotoInit
        self.IF = IF

        self.isInit = False

    def initialize(self):
        self.IF.SetMotor(self.Mot)
        time.sleep(0.5)
        while True:
            if not self.IF.Digital(self.PhotoInit):
                time.sleep(0.01)
                if not self.IF.Digital(self.PhotoInit):
                    self.IF.SetMotor(self.Mot, 's')
                    break

# This Belt can be adjusted
# class demoBelt(Belt):
#    def __init__(self, Mot, PhotoInit, IF):
#        super().__init__(Mot, PhotoInit, IF)


class F2(Belt):
    def __init__(self, Mot, PhotoInit, IF):
        super().__init__(Mot, PhotoInit, IF)
