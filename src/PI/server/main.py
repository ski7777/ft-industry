#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import modules.IF0.__main__ as IF0Mod
IF0 = IF0Mod.Interface()
F1 = IF0.F1
F2 = IF0.F2
Sled = IF0.Sled

Sled.initialize(home=False)
F1.initialize()
F2.initialize()
Sled.home()
