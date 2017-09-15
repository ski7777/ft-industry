#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


class Palllet():
    def __init__(self, ident):
        self.id = ident
        self._pos = 0
        self.lastStamp = 0
    @property
    def pos(self):
        return(self._pos)

    @pos.setter
    def setPOS(self, pos):
        assert(type(pos) == int)
        if pos in range(5):
            self._pos = pos
