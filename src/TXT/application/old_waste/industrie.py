#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from _thread import start_new_thread
from TouchStyle import *
import sys
import os
import com
#RND:[POS, [ORDER], initiate]
#POS: 1: HRL
pallet_stack = {}
global confirm_str
global errorcode
push_button = com.push_button()
traffic_lights = com.traffic_lights()
traffic_lights.set_pattern('red', [True, True, True, True])
traffic_lights.set_new()
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
        lbl.setWordWrap(True);
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

class FtcGuiApplication(TouchApplication):

    def __init__(self, args):
        self.IF1 = com.com_stack()
        self.IF1.setio(1, 1)
        self.IF1.start_recieving()
        self.TX = com.com_stack()
        self.TX.setio(2, 2)
        self.TX.start_recieving()
        TouchApplication.__init__(self, args)
        print('-----READY-----')
        # create the empty main window
        self.w = TouchWindow("Industrie")
        menu = self.w.addMenu()
        menu_about = menu.addAction("About")
        menu_about.triggered.connect(self.show_about)
        self.vbox = QVBoxLayout()
        self.vbox.addStretch()
        ###
        self.b_start_workflow = ShadowButton("start_if")
        self.b_start_workflow.setText("Einlagern")
        self.b_start_workflow.clicked.connect(self.to_HRL)
        self.vbox.addWidget(self.b_start_workflow)
        ###
        self.b_start_HRL = ShadowButton("start_HRL")
        self.b_start_HRL.setText("Auslagern")
        self.b_start_HRL.clicked.connect(self.from_HRL)
        self.vbox.addWidget(self.b_start_HRL)
        ###
        self.vbox.addStretch()
        ###
        self.w.centralWidget.setLayout(self.vbox)
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
            #com.sound(14, 20)
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
        print("start workflow")
        ###IF F1 -> FS
        traffic_lights.set_pattern('red', [False, False, False, False])
        traffic_lights.set_pattern('yellow', [True, True, True, True])
        traffic_lights.set_new()
        time.sleep(2) ##Check Avaible
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
            return
        rnd = self.IF1.start_trans(14, True)
        if rnd == None:
            self.show_error('0x01 (IF)')
            self.IF1.kill_trans(rnd)
            return
        found = False
        while True:
            if found == True:
                break
            for search_item in self.IF1.get_answers(rnd):
                if search_item[1] == 5:
                    found = True
            time.sleep(0.5)
        self.IF1.kill_trans(rnd)
        ### HRL
        pallet_rnd = 1
        print('LEN: ' + str(len(pallet_stack.keys())))
        while str(pallet_rnd) in pallet_stack.keys():
            #print('plus' + str(pallet_rnd))
            pallet_rnd += 1
        print('PALLET RND: ' + str(pallet_rnd))
        print(pallet_stack)
        pallet_stack[str(pallet_rnd)] = [1, ['ORDER']]
        print(pallet_stack)
        start_new_thread(self.HRL_send, (True, pallet_rnd,))
        ### Fs -> F2
        rnd = self.IF1.start_trans(11, True)
        if rnd == None:
            self.show_error('0x01 (IF)')
            self.IF1.kill_trans(rnd)
            return
        found = False
        while True:
            if found == True:
                break
            for search_item in self.IF1.get_answers(rnd):
                if search_item[1] == 5:
                    found = True
            time.sleep(0.5)
        self.IF1.kill_trans(rnd)
        print('----------')

    def from_HRL(self):
        print('start Auslagern')
        ConfirmationDialog('Vorgang Starten?', 'YES', 'NO').exec_()
        if confirm_str == 'YES':
            pass
        else:
            return
        ###HRL
        #chang later
        print(pallet_stack)
        pallet_rnd = int(input('Enter Pallet ID:'))
        start_new_thread(self.HRL_send, (False, pallet_rnd,))
        ###F2 -> Fs
        rnd = self.IF1.start_trans(17, True)
        if rnd == None:
            #com.sound(14, 20)
            self.show_error('0x02 (IF)')
            return
        else:
            found = False
            while True:
                if found == True:
                    break
                for search_item in self.IF1.get_answers(rnd):
                    if search_item[1] == 5:
                        found = True
                time.sleep(0.5)
            self.IF1.kill_trans(rnd)
        print('----------')
    def show_about(self):
        dialog = AboutDialog(self.w)
        dialog.exec_()

    def show_error(self, _c):
        global errorcode
        errorcode = _c
        dialog = ErrorDialog(self.w)
        dialog.exec_()
if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
