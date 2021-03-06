#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from bash import bash as BashHandler            # import bash lib
import ftrobopy                                 # import hardware i/o lib for fischertechnik
from _thread import start_new_thread            # import simple thread starter
import random                                   # import random lib
import copy                                     # import lib for copying data structures
# import basic functions of python
import time

txt = ftrobopy.ftrobopy('direct')     # initialize i/o communicaton
# initialize communication constants
analog_threshold = 1500
com_speed = 0.1
com_values = [2, 5, 8, 11, 14, 17, 20]
com_target_diff = 0.1
com_wait_after_send = 5
global com_buffers                              # initialize communication buffer
com_buffers = {}
bash = BashHandler()


class push_button():

    def __init__(self, p):
        self.button = txt.input(p)

    def get_state(self):
        if self.button.state() == 1:
            return(True)
        else:
            return(False)


class traffic_lights():

    def __init__(self, r, y, g):
        self.red = txt.output(r)
        self.yellow = txt.output(y)
        self.green = txt.output(g)
        self.data = {'red': [self.red, None, [False, False, False, False]],
                     'yellow': [self.yellow, None, [False, False, False, False]],
                     'green': [self.green, None, [False, False, False, False]]}
        self.data_new = {'red': [False, False, False, False],
                         'yellow': [False, False, False, False],
                         'green': [False, False, False, False]}
        start_new_thread(self.thread, ())

    def set_pattern(self, _color, _list):
        if _color in self.data.keys():
            self.data_new[_color] = _list

    def set_new(self):
        for _color, _data in self.data_new.items():
            self.data[_color][2] = _data

    def get_level(self, v):
        if v == True:
            return(512)
        else:
            return(0)

    def thread(self):
        while True:
            for phase in [0, 1, 2, 3]:
                for light in self.data.keys():
                    if self.data[light][1] != self.data[light][2][phase]:
                        self.data[light][1] = self.data[light][2][phase]
                        self.data[light][0].setLevel(self.get_level(self.data[light][2][phase]))
                time.sleep(0.125)
                for light in self.data.keys():
                    if self.data[light][1] != self.data[light][2][phase]:
                        self.data[light][1] = self.data[light][2][phase]
                        self.data[light][0].setLevel(self.get_level(self.data[light][2][phase]))
                time.sleep(0.125)


def get_digital(value, gd_threshold):
    if value >= gd_threshold:
        return True
    else:
        return False


def recieve(_i, _threshold):
    while get_digital(_i.voltage(), _threshold) == False:
        time.sleep(0.05)
    start = time.time()
    while get_digital(_i.voltage(), _threshold) == True:
        time.sleep(0.05)
    end = time.time()
    diff = end - start
    return(diff)


def get_target(_v, _tlist, _diff):
    for _tliastval in _tlist:
        listval = _tliastval / 10
        if (listval - _v > -0.2 and listval - _v < _diff) or (listval + _v > -0.2 and listval + _v < _diff):
            bash.addData("com", 'target ' + str(_tliastval))
            return(_tliastval)


def send(o, speed, v):
    o.setLevel(512)
    time.sleep(speed * v)
    o.setLevel(0)


def send_set(o, speed, d):
    for send_bracket in d:
        send(o, speed, send_bracket)
        time.sleep(speed)


def com_thread(_i, _ident):
    #x = 0
    while True:
        uuid = get_target(recieve(_i, analog_threshold), com_values, com_target_diff)
        command = get_target(recieve(_i, analog_threshold), com_values, com_target_diff)
        bash.addData("com", 'Adding to ' + str(_ident) + ' uuid ' + str(uuid) + ' command ' + str(command))
        add_list = [uuid, command]
        globals()['stack_list_' + str(_ident)].append(add_list)
        bash.addData("com", 'reading stack_list_' + str(_ident) + ': ' + str(globals()['stack_list_' + str(_ident)]))


class com_stack():

    def __init__(self):
        self.open_trans = []
        x = 0
        global com_buffers
        while True:
            if x in com_buffers:
                x += 1
            else:
                com_buffers[x] = []
                break
        self.ident = copy.deepcopy(x)
        bash.addData("com", 'Stack Ident: ' + str(x))
        bash.addData("com", 'SETTING stack_list_' + str(self.ident))
        globals()['stack_list_' + str(self.ident)] = []
        bash.addData("com", 'reading stack_list_' + str(self.ident) + ' : ' + str(globals()['stack_list_' + str(self.ident)]))

    def setio(self, _i, _o):
        bash.addData("com", 'Setting IO: ' + str(_i) + str(_o))
        self.input = txt.voltage(_i)
        self.output = txt.output(_o)

    def start_trans(self, _d, _reqa):
        self.values_to_chose = list(com_values)
        for x in self.open_trans:
            bash.addData("com", 'Chosen RND: ' + str(x))
            self.values_to_chose.remove(x)
        bash.addData("com", 'Free RNDs: ' + str(self.values_to_chose))
        if len(self.values_to_chose) == 0:
            bash.addData("com", 'NO MORE VAL')
            return
        new_rnd = random.choice(self.values_to_chose)
        self.open_trans.append(new_rnd)
        bash.addData("com", 'Sending data ' + str(_d) + ' to uuid ' + str(new_rnd))
        send_set(self.output, com_speed, [new_rnd, _d])
        sent_time = time.time()
        if _reqa == True:
            while sent_time + com_wait_after_send > time.time():
                for search_item in globals()['stack_list_' + str(self.ident)]:
                    if search_item[0] == new_rnd:
                        if search_item[1] == 2:
                            globals()['stack_list_' + str(self.ident)].remove(search_item)
                            bash.addData("com", 'Success')
                            return(new_rnd)
            bash.addData("com", 'ERROR')
            return
        else:
            bash.addData("com", 'Sended without requested answer')
            return(new_rnd)

    def add_trans(self, _uuid, _d, _reqa):
        if not _uuid in self.open_trans:
            return
        bash.addData("com", 'Adding data ' + str(_d) + ' to uuid ' + str(_uuid))
        send_set(self.output, com_speed, [_uuid, _d])
        sent_time = time.time()
        if _reqa == True:
            while sent_time + com_wait_after_send > time.time():
                for search_item in globals()['stack_list_' + str(self.ident)]:
                    if search_item[0] == _uuid:
                        if search_item[1] == 2:
                            globals()['stack_list_' + str(self.ident)].remove(search_item)
                            bash.addData("com", 'Success')
                            return
            bash.addData("com", 'ERROR')
            return
        else:
            bash.addData("com", 'Sended without requested answer')
            return

    def get_answers(self, _uuid):
        if not _uuid in self.open_trans:
            return
        answers = []
        for search_item in globals()['stack_list_' + str(self.ident)]:
            if search_item[0] == _uuid:
                answers.append(search_item)
        return(answers)

    def del_answers(self, _uuid):
        if not _uuid in self.open_trans:
            return
        bash.addData("com", 'Deleting answers of uuid ' + str(_uuid))
        for search_item in globals()['stack_list_' + str(self.ident)]:
            if search_item[0] == _uuid:
                globals()['stack_list_' + str(self.ident)].remove(search_item)
        return

    def kill_trans(self, _uuid):
        bash.addData("com", 'Killing all data for uuid ' + str(_uuid))
        self.open_trans.remove(_uuid)
        for search_item in globals()['stack_list_' + str(self.ident)]:
            if search_item[0] == _uuid:
                globals()['stack_list_' + str(self.ident)].remove(search_item)
        self.values_to_chose = list(com_values)
        for x in self.open_trans:
            bash.addData("com", 'Chosen RND: ' + str(x))
            self.values_to_chose.remove(x)
        bash.addData("com", 'Free RNDs: ' + str(self.values_to_chose))

    def start_recieving(self):
        start_new_thread(com_thread, (self.input, self.ident,))


def sound(_i, _t):
    txt.play_sound(_i, _t)
