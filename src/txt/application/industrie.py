#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from _thread import start_new_thread
from TouchStyle import *
import sys
import os
import copy
global confirm_str
global errorcode
import logic
global kill_full_screen
kill_full_screen = False
push_button = logic.push_button
traffic_lights = logic.traffic_lights
class ShadowButton(QToolButton):

    def __init__(self, iconname):
        QToolButton.__init__(self)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(QPointF(3, 3))
        self.setGraphicsEffect(shadow)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pix = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), iconname))
        icon = QIcon(pix)
        self.setIcon(icon)
        self.setIconSize(pix.size())

        # hide shadow while icon is pressed
    def mousePressEvent(self, event):
        self.graphicsEffect().setEnabled(False)
        QToolButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.graphicsEffect().setEnabled(True)
        QToolButton.mouseReleaseEvent(self, event)

class PlainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        if platform.machine() == "armv7l":
            size = QApplication.desktop().screenGeometry()
            self.setFixedSize(size.width(), size.height())
        else:
            self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)

        self.setObjectName("centralwidget")

    def exec_(self):
        QDialog.showFullScreen(self)
        QDialog.exec_(self)

class AboutDialog(TouchDialog):
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
               '<br><a href="https://www.iconfinder.com/icons/174753/screw_icon#size=128">https://www.iconfinder.com/icons/174753/screw_icon#size=128</a><br>' \
               '<img src="start.png" alt="Selfhtml">'
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
    def __init__(self, parent):
        global errorcode
        TouchDialog.__init__(self, "ERROR", parent)
        self.text = '<center><img src="/media/sdcard/apps/8f06f80c-dfb1-4c13-bc3f-3c806eff1edc/qr/1.png" alt="Error getting image">' \
                    '<b>ERROR ' + errorcode + '<b>' \
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

class ConfirmationDialog(PlainDialog):
    def __init__(self, str, t1, t2):
        PlainDialog.__init__(self)

        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.truestr = t1
        lbl = QLabel(str)
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl)

        button_box = QWidget()
        button_layout = QHBoxLayout()
        button_box.setLayout(button_layout)

        button_layout.addStretch()

        t1_but = QPushButton(t1)
        t1_but.clicked.connect(self.on_button_clicked)
        button_layout.addWidget(t1_but)

        button_layout.addStretch()

        t2_but = QPushButton(t2)
        t2_but.clicked.connect(self.on_button_clicked)
        button_layout.addWidget(t2_but)

        button_layout.addStretch()

        self.layout.addStretch()
        self.layout.addWidget(button_box)
        self.layout.addStretch()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.kill_self)
        self.timer.start(10000)
        start_new_thread(self.button_check, ())
        self.setLayout(self.layout)

    def on_button_clicked(self):
        global confirm_str
        confirm_str = self.sender().text()
        self.close()
    def kill_self(self):
        global confirm_str
        print('KILLING Dialog! Timeout!')
        self.timer.stop()
        confirm_str = None
        self.close()
    def button_check(self):
        while True:
            if push_button.get_state() == True:
                global confirm_str
                confirm_str = self.truestr
                self.close()
            time.sleep(0.2)

class InfoDialog(PlainDialog):
    def __init__(self, str):
        PlainDialog.__init__(self)
        self.showFullScreen()
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        lbl = QLabel(str)
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl)
        self.layout.addStretch()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.kill_self)
        self.timer.start(100)
        self.setLayout(self.layout)
    def kill_self(self):
        if kill_full_screen:
            kill_full_screen = False
            self.timer.stop()
            self.close()

class FtcGuiApplication(TouchApplication):

    def __init__(self, args):
        TouchApplication.__init__(self, args)
        print('-----READY-----')
        # create the empty main window
        self.generate_gui()
    def generate_gui(self):
        self.w = TouchWindow("Industrie")
        menu = self.w.addMenu()
        menu_about = menu.addAction("About")
        menu_about.triggered.connect(self.show_about)
        self.vbox = QVBoxLayout()
        self.new_vbox = QVBoxLayout()
        self.vbox.addStretch()
        ###
        self.b_start_workflow = ShadowButton("start_if")
        self.b_start_workflow.setText("Einlagern")
        self.b_start_workflow.clicked.connect(self.to_HRL)
        self.vbox.addWidget(self.b_start_workflow)
        ###
        self.vbox.addStretch()
        ###
        self.w.centralWidget.setLayout(self.vbox)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_vbox)
        self.timer.start(500)
        print(dir(self.w))
        self.w.show()
        self.exec_()
    def HRL_send(self, ea, nbr):
        if ea == True:
            rnd = self.TX.start_trans(8, False)
        elif ea == False:
            rnd = self.TX.start_trans(5, False)
        else:
            return
        if rnd == None:
            self.show_error('0x02 (TX)')
            return
        else:
            if nbr >= 1 and nbr <= 25:
                nbr0 = 2
            elif nbr >= 26 and nbr <= 50:
                nbr0 = 5
                nbr -= 25

            if nbr >= 1 and nbr <= 5:
                nbr1 = 2
            elif nbr >= 5 and nbr <= 10:
                nbr1 = 5
                nbr -= 5
            elif nbr >= 11 and nbr <= 15:
                nbr1 = 8
                nbr -= 10
            elif nbr >= 16 and nbr <= 20:
                nbr1 = 11
                nbr -= 15
            elif nbr >= 21 and nbr <= 25:
                nbr1 = 14
                nbr -= 20

            if nbr == 1:
                nbr2 = 2
            elif nbr == 2:
                nbr2 = 5
            elif nbr == 3:
                nbr2 = 8
            elif nbr == 4:
                nbr2 = 11
            elif nbr == 5:
                nbr2 = 14
            print('DATA TO HRL:' + str(nbr0), str(nbr1), str(nbr2))
            time.sleep(0.5)
            self.TX.add_trans(rnd, nbr0, False)
            time.sleep(0.1)
            self.TX.add_trans(rnd, nbr1, False)
            time.sleep(0.1)
            self.TX.add_trans(rnd, nbr2, False)
            self.TX.kill_trans(rnd)
    def to_HRL(self):
        traffic_lights.set_pattern('red', [False, False, False, False])
        traffic_lights.set_pattern('yellow', [True, True, False, False])
        traffic_lights.set_new()
        self.lbl = QLabel('Bitte Warten')
        self.lbl.setWordWrap(True)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.new_vbox.addStretch()
        self.new_vbox.addWidget(self.lbl)
        self.new_vbox.addStretch()
        logic.wait_for_new_pallet()
        time.sleep(5)
        traffic_lights.set_pattern('yellow', [False, False, False, False])
        traffic_lights.set_pattern('green', [True, True, True, True])
        traffic_lights.set_new()
        ConfirmationDialog('Vorgang Starten?', 'YES', 'NO').exec_()
        if confirm_str == 'YES':
            traffic_lights.set_pattern('red', [True, True, True, True])
            traffic_lights.set_pattern('yellow', [False, False, False, False])
            traffic_lights.set_pattern('green', [False, False, False, False])
            traffic_lights.set_new()
        else:
            traffic_lights.set_pattern('red', [True, True, True, True])
            traffic_lights.set_pattern('yellow', [False, False, False, False])
            traffic_lights.set_pattern('green', [False, False, False, False])
            traffic_lights.set_new()
            logic.abort_new_pallet()
            return
        logic.new_pallet(logic.generate_palled_ID())

    def show_about(self):
        dialog = AboutDialog(self.w)
        dialog.exec_()

    def show_error(self, _c):
        global errorcode
        errorcode = _c
        dialog = ErrorDialog(self.w)
        dialog.exec_()
    def show_vbox(self):
        self.vbox = copy.deepcopy(self.new_vbox)
if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
