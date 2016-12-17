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
traffic_lights = logic.traffic_lights  # initialize the traffic lights


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
        self.b_new.clicked.connect(self.new_order)
        self.vbox.addWidget(self.b_new)
        ###
        self.vbox.addStretch()
        ###
        self.b_get = ShadowButton("get")
        self.b_get.setText("Empfangen")
        # currently a place holder for later use
        # self.b_get.clicked.connect(self.get)
        self.vbox.addWidget(self.b_get)
        ###
        self.vbox.addStretch()
        self.w.centralWidget.setLayout(self.vbox)
        self.w.show()
        self.exec_()

    def new_order(self):
        # show waiting traffic lights
        traffic_lights.set_pattern('red', [False, False, False, False])
        traffic_lights.set_pattern('yellow', [True, True, False, False])
        traffic_lights.set_new()
        # wait for F1 free and let the user abort waiting
        NewPalletWaitDialog().exec_()
        # check status of F1
        print(logic.F1)
        if logic.F1 != 1000:
            # abort
            traffic_lights.set_pattern('red', [True, True, True, True])
            traffic_lights.set_pattern('yellow', [False, False, False, False])
            traffic_lights.set_pattern('green', [False, False, False, False])
            traffic_lights.set_new()
            return
        # wait for more security
        time.sleep(2)
        # show ready traffic lights
        traffic_lights.set_pattern('yellow', [False, False, False, False])
        traffic_lights.set_pattern('green', [True, True, True, True])
        traffic_lights.set_new()
        # add order menu
        # ask user to satart the workflow
        confirm = ConfirmationDialog('Vorgang Starten?', 'YES', 'NO', 10000)
        confirm.exec_()
        # get values from confirmation dialog
        confirm_str = confirm.get()
        print(confirm_str)
        # show traffic lights stop
        traffic_lights.set_pattern('red', [True, True, True, True])
        traffic_lights.set_pattern('yellow', [False, False, False, False])
        traffic_lights.set_pattern('green', [False, False, False, False])
        traffic_lights.set_new()
        if confirm_str != 'YES':
            # abort new pallet if start not confirmed
            logic.abort_new_pallet()
            return
        logic.new_pallet(logic.generate_palled_ID(), 'TEST')

    def show_about(self):
        # open about dialog
        dialog = AboutDialog(self.w)
        dialog.exec_()

    def show_error(self, _c):
        # open error dialog
        dialog = ErrorDialog(self.w, _c)
        dialog.exec_()

if __name__ == "__main__":
    # start main application
    FtcGuiApplication(sys.argv)
