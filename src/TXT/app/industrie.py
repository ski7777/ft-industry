#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from TouchStyle import *                # import PyQt, CFW Style and co.
from windows import *                   # import application´s windows
import logic                            # import the hardware logic
# import basic functions of python
import time
import sys
import os

push_button = logic.push_button        # initialize the pushbutton
traffic_lights = logic.traffic_lights


class FtcGuiApplication(TouchApplication):

    def __init__(self, args):
        TouchApplication.__init__(self, args)
        print('-----READY-----')
        # create the empty main window
        self.w = TouchWindow("Industrie")
        menu = self.w.addMenu()
        menu_about = menu.addAction("About")
        menu_about.triggered.connect(self.show_about)
        self.vbox = QVBoxLayout()
        self.new_vbox = QVBoxLayout()
        self.vbox.addStretch()
        ###
        self.b_new = ShadowButton("add")
        self.b_new.setText("Neue Bestellung")
        self.b_new.clicked.connect(self.to_HRL)
        self.vbox.addWidget(self.b_new)
        ###
        self.vbox.addStretch()
        ###
        self.b_get = ShadowButton("get")
        self.b_get.setText("Empfangen")
        # self.b_get.clicked.connect(self.get)
        self.vbox.addWidget(self.b_get)
        ###
        self.vbox.addStretch()
        self.w.centralWidget.setLayout(self.vbox)
        self.w.show()
        self.exec_()

    def to_HRL(self):
        traffic_lights.set_pattern('red', [False, False, False, False])
        traffic_lights.set_pattern('yellow', [True, True, False, False])
        traffic_lights.set_new()
        logic.wait_for_new_pallet()
        time.sleep(2)
        traffic_lights.set_pattern('yellow', [False, False, False, False])
        traffic_lights.set_pattern('green', [True, True, True, True])
        traffic_lights.set_new()
        confirm = ConfirmationDialog('Vorgang Starten?', 'YES', 'NO', 10000)
        confirm.exec_()
        confirm_str = confirm.get()
        print(confirm_str)
        traffic_lights.set_pattern('red', [True, True, True, True])
        traffic_lights.set_pattern('yellow', [False, False, False, False])
        traffic_lights.set_pattern('green', [False, False, False, False])
        traffic_lights.set_new()
        if confirm_str != 'YES':
            logic.abort_new_pallet()
            return
        logic.new_pallet(logic.generate_palled_ID(), 'TEST')

    def show_about(self):
        dialog = AboutDialog(self.w)
        dialog.exec_()

    def show_error(self, _c):
        dialog = ErrorDialog(self.w, _c)
        dialog.exec_()

if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
