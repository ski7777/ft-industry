#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import time

import robointerface as RI


class Interface():
    def __init__(self):
        self.IF = RI.RoboInterface()
        self.F1 = F1(self.IF)
        self.F2 = F2(self.IF)
        self.Sled = Sled(self.IF)
        self.Stamp = Stamp(9, self.IF)

    def getSupplyVoltage(self):
        return(self.IF.av_to_v(self.IF.GetAV))


class Sled():
    def __init__(self, IF):
        self.MotSled = 3
        self.MotBelt = 2
        self.ButEnd = 4
        self.PhotoBelt = 3
        self.IF = IF

        self.isInit = False
        self.curPosBelt = -1
        self.curPosSled = -1

        self.POSBELTHOME = 0
        self.POSBELTHANDOVER = 1
        self.POSSLEDHOME = 0

    def initialize(self, home=True):
        if not self.IF.Digital(self.ButEnd):
            self.IF.SetMotor(self.MotSled, iSpeed=-3)
            while not self.IF.Digital(self.ButEnd):
                pass
        self.IF.SetMotor(self.MotSled)
        time.sleep(2)
        self.IF.SetMotor(self.MotSled, 's')

        self.IF.SetMotor(self.MotBelt)
        while True:
            if not self.IF.Digital(self.PhotoBelt):
                time.sleep(0.01)
                if not self.IF.Digital(self.PhotoBelt):
                    self.IF.SetMotor(self.MotBelt, 's')
                    break
        self.curPosBelt = self.POSBELTHOME
        if home:
            self.home()

    def home(self):
        if not self.IF.Digital(self.ButEnd):
            self.IF.SetMotor(self.MotSled, iSpeed=-3)
            while not self.IF.Digital(self.ButEnd):
                pass
            self.IF.SetMotor(self.MotSled, 's')
        self.curPosSled = self.POSSLEDHOME

    def goPosBelt(self, pos):
        if pos == self.POSBELTHOME:
            if self.curPosBelt != self.POSBELTHOME:
                self.IF.SetMotor(self.MotBelt)
                time.sleep(0.5)
                while True:
                    if not self.IF.Digital(self.PhotoBelt):
                        time.sleep(0.01)
                        if not self.IF.Digital(self.PhotoBelt):
                            self.IF.SetMotor(self.MotBelt, 's')
                            break
                self.curPosBelt = self.POSBELTHOME
        elif pos == self.POSBELTHANDOVER:
            if self.curPosBelt != self.POSBELTHANDOVER:
                self.goPosBelt(self.POSBELTHOME)
                self.IF.SetMotor(self.MotBelt)
                time.sleep(0.8)
                self.IF.SetMotor(self.MotBelt, 's')
                self.curPosBelt = self.POSBELTHANDOVER


class Belt():
    def __init__(self, Mot, PhotoInit, IF):
        self.Mot = Mot
        self.PhotoInit = PhotoInit
        self.IF = IF

        self.isInit = False
        self.curPosBelt = -1

        self.POSBELTHOME = 0

    def initialize(self):
        self.IF.SetMotor(self.Mot)
        time.sleep(0.5)
        while True:
            if not self.IF.Digital(self.PhotoInit):
                time.sleep(0.01)
                if not self.IF.Digital(self.PhotoInit):
                    self.IF.SetMotor(self.Mot, 's')
                    break
        self.curPos = self.POSBELTHOME

# This Belt can be adjusted
# class demoBelt(Belt):
#    def __init__(self, Mot, PhotoInit, IF):
#        super().__init__(Mot, PhotoInit, IF)


class Stamp():
    def __init__(self, Valve, IF):
        self.Valve = Valve
        self.IF = IF

        self.curPosStamp = 0

        self.POSSTAMPUP = 0
        self.POSSTAMPSOWN = 1

    def goPos(self, pos):
        if pos == self.POSSTAMPUP:
            self.IF.SetOutput(self.Valve, 0)
        elif pos == self.POSSTAMPSOWN:
            self.IF.SetOutput(self.Valve, 7)


class F1(Belt):
    def __init__(self, IF):
        super().__init__(1, 1, IF)
        self.POSBELTTAMP = 1

    def goPos(self, pos):
        if pos == self.POSBELTHOME:
            if self.curPosBelt != self.POSBELTHOME:
                self.initialize()
        elif pos == self.POSBELTTAMP:
            self.goPos(self.POSBELTHOME)
            self.IF.SetMotor(self.Mot, 'l', 3)
            time.sleep(0.5)
            while True:
                if not self.IF.Digital(self.PhotoInit):
                    time.sleep(0.01)
                    if not self.IF.Digital(self.PhotoInit):
                        time.sleep(0.1)
                        self.IF.SetMotor(self.Mot, 's')
                        break
            self.curPosBelt = self.POSBELTTAMP


class F2(Belt):
    def __init__(self, IF):
        super().__init__(4, 5, IF)
        self.PhotoEnd = 6
