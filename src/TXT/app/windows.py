#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from _thread import start_new_thread    # import simple thread starter
import __main__ as main                 # import main script variables
from style import *                     # import application style lib
import logic                            # import logic to access logic variables
# import basic functions of python
import time
bash = logic.bash



class ConfirmationDialog(PlainDialog):
    # generate a confirmation dialog based on PlainDialog

    def __init__(self, str, t1, t2, time):
        PlainDialog.__init__(self)
        # initialize return variable
        self.data = None
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        lbl = QLabel(str)
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl)

        button_box = QWidget()
        button_layout = QHBoxLayout()
        button_box.setLayout(button_layout)

        button_layout.addStretch()

        self.t1_but = QPushButton(t1)
        self.t1_but.clicked.connect(self.on_button_clicked)
        button_layout.addWidget(self.t1_but)

        button_layout.addStretch()

        t2_but = QPushButton(t2)
        t2_but.clicked.connect(self.on_button_clicked)
        button_layout.addWidget(t2_but)

        button_layout.addStretch()

        self.layout.addStretch()
        self.layout.addWidget(button_box)
        self.layout.addStretch()
        # initialize self kill timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.kill_self)
        self.timer.start(time)
        # initiate button check
        start_new_thread(self.button_check, ())
        self.setLayout(self.layout)

    def on_button_clicked(self):
        self.timer.stop()
        self.data = self.sender().text()
        self.close()

    def button_check(self):
        while True:
            if main.push_button.get_state() == True:
                # trigger t1 if button was pressed
                self.t1_but.click()
            time.sleep(0.1)

    def get(self):
        # return button data
        return(self.data)

    def kill_self(self):
        # sotp timer and kill dialog
        self.timer.stop()
        self.close()


class AboutDialog(TouchDialog):
    # generate about dialog

    def __init__(self, parent):
        self.text = '<h2><font color="#fcce04">Industrieanlage</font></h2>' \
            '<b>Industrieanlage gebaut aus fischertechnik</b><br>' \
            '2016, ski7777 and ski3989<br>' \
            '<h2><font color="#fcce04">Credits</font></h2>' \
            '<b>ftrobopy<b>' \
            '<br>Thorsten Stuehn<br>' \
            '<b>Robo TXT ftcommunity Firmware</b>' \
            '<br>All developers at<br>' \
            '<br><a href="https://github.com/ftCommunity/ftcommunity-TXT">https://github.com/ftCommunity/ftcommunity-TXT</a><br>' \
            '<b>App Icon</b>'\
            '<br><a href="https://www.iconfinder.com/icons/174753/screw_icon#size=128">https://www.iconfinder.com/icons/174753/screw_icon#size=128</a><br>'
        TouchDialog.__init__(self, "About", parent)
        self.txt = QTextEdit()
        self.txt.setReadOnly(True)
        self.font = QFont()
        self.font.setPointSize(16)
        self.txt.setFont(self.font)
        self.txt.setHtml(self.text)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.txt)
        self.centralWidget.setLayout(self.vbox)


class ErrorDialog(TouchDialog):
    # generate error dialog

    def __init__(self, parent, _c):
        TouchDialog.__init__(self, "ERROR", parent)
        self.text = '<center><img src="/media/sdcard/apps/8f06f80c-dfb1-4c13-bc3f-3c806eff1edc/qr/1.png" alt="Error getting image">' \
                    '<b>ERROR ' + _c + '<b>' \
                    '<br>Please call the owner' \
                    '<br>Bitte rufe den Besitzer dieses Modells' \
                    '</center>'
        self.txt = QTextEdit()
        self.txt.setReadOnly(True)
        self.font = QFont()
        self.font.setPointSize(16)
        self.txt.setFont(self.font)
        self.txt.setHtml(self.text)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.txt)
        self.centralWidget.setLayout(self.vbox)


class NewPalletWaitDialog(PlainDialog):
    # generate a dialog in which the user can see howto add a pllaet to F1 and can abort adding a new pallet

    def __init__(self):
        PlainDialog.__init__(self)
        self.layout = QVBoxLayout()
        self.lbl = QLabel('Please Wait!')
        self.lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl)
        self.layout.addStretch()
        self.abort_but = QPushButton('Abort')
        self.abort_but.clicked.connect(self.abort_but_triggered)
        self.layout.addWidget(self.abort_but)
        self.layout.addStretch()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_F1)
        self.timer.start(100)
        self.setLayout(self.layout)

    def check_F1(self):
        # wait for F1 free
        if logic.F1 == 0:
            # reservate F1 for new pallet
            logic.F1 = 1000
            # stop timer and kill dialog
            self.timer.stop()
            self.close()

    def abort_but_triggered(self):
        # stop timer and kill dialog
        self.timer.stop()
        self.close()


class NewOrderDialog(TouchDialog):
    # generate a dilog to enter the order

    def __init__(self, parent):
        TouchDialog.__init__(self, "New Order", parent)
        self.data = None
        self.layout = QVBoxLayout()
        # for TEST
        self.lbl = QLabel('Test only')
        self.layout.addWidget(self.lbl)
        self.layout.addStretch()
        self.ok_but = QPushButton('Send')
        self.ok_but.clicked.connect(self.save)
        self.layout.addWidget(self.ok_but)
        self.layout.addStretch()
        self.centralWidget.setLayout(self.layout)

    def save(self):
        # save data to variable and close dialog
        self.data={}
        self.close()

    def get(self):
        # return order data
        return(self.data)
