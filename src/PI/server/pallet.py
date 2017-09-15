#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import random


def findPalletID(stack):
    usedIDs = []
    for x in stack:
        usedIDs.append(x.id)
    if len(usedIDs) == 0:
        return(1)
    while True:
        rand = random.randint(1, 49)
        if rand not in usedIDs:
            return(rand)


class Palllet():
    def __init__(self, ident):
        self.id = ident
        self._pos = 0
        self.lastStamp = 0
        self.POSF1 = 0
        self.POSSLED = 1
        self.POSF2 = 2
        self.POSHRL = 3
        self.positions = [self.POSF1, self.POSSLED, self.POSF2, self.POSHRL]

    @property
    def pos(self):
        return(self._pos)

    @pos.setter
    def pos(self, pos):
        assert(type(pos) == int)
        if pos in self.positions:
            self._pos = pos
