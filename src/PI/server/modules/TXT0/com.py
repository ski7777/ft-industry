#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import copy  # import lib for copying data structures
import random  # import random lib
import threading
import time

analog_threshold = 1500
com_speed = 0.1
com_values = [2, 5, 8, 11, 14, 17, 20]
com_target_diff = 0.1
com_wait_after_send = 5
global com_buffers                              # initialize communication buffer
com_buffers = {}


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
            return(_tliastval)


def send(o, speed, v):
    o.setLevel(512)
    time.sleep(speed * v)
    o.setLevel(0)


def send_set(o, speed, d):
    for send_bracket in d:
        send(o, speed, send_bracket)
        time.sleep(speed)


class com_stack(threading.Thread):

    def __init__(self, txt):
        threading.Thread.__init__(self)
        self.open_trans = []
        self.txt = txt
        x = 0
        global com_buffers
        while True:
            if x in com_buffers:
                x += 1
            else:
                com_buffers[x] = []
                break
        self.id = x
        globals()['stack_list_' + str(self.id)] = []

    def setio(self, _i, _o):
        self.input = self.txt.voltage(_i)
        self.output = self.txt.output(_o)

    def start_trans(self, _d, _reqa):
        self.values_to_chose = list(com_values)
        for x in self.open_trans:
            self.values_to_chose.remove(x)
        if len(self.values_to_chose) == 0:
            return
        new_rnd = random.choice(self.values_to_chose)
        self.open_trans.append(new_rnd)
        send_set(self.output, com_speed, [new_rnd, _d])
        sent_time = time.time()
        if _reqa == True:
            while sent_time + com_wait_after_send > time.time():
                for search_item in globals()['stack_list_' + str(self.id)]:
                    if search_item[0] == new_rnd:
                        if search_item[1] == 2:
                            globals()['stack_list_' + str(self.id)].remove(search_item)
                            return(new_rnd)
            return
        else:
            return(new_rnd)

    def add_trans(self, _uuid, _d, _reqa):
        if not _uuid in self.open_trans:
            return
        send_set(self.output, com_speed, [_uuid, _d])
        sent_time = time.time()
        if _reqa == True:
            while sent_time + com_wait_after_send > time.time():
                for search_item in globals()['stack_list_' + str(self.id)]:
                    if search_item[0] == _uuid:
                        if search_item[1] == 2:
                            globals()['stack_list_' + str(self.id)].remove(search_item)
                            return
            return
        else:
            return

    def get_answers(self, _uuid):
        if not _uuid in self.open_trans:
            return
        answers = []
        for search_item in globals()['stack_list_' + str(self.id)]:
            if search_item[0] == _uuid:
                answers.append(search_item)
        return(answers)

    def del_answers(self, _uuid):
        if not _uuid in self.open_trans:
            return
        for search_item in globals()['stack_list_' + str(self.id)]:
            if search_item[0] == _uuid:
                globals()['stack_list_' + str(self.id)].remove(search_item)
        return

    def kill_trans(self, _uuid):
        self.open_trans.remove(_uuid)
        for search_item in globals()['stack_list_' + str(self.id)]:
            if search_item[0] == _uuid:
                globals()['stack_list_' + str(self.id)].remove(search_item)
        self.values_to_chose = list(com_values)
        for x in self.open_trans:
            self.values_to_chose.remove(x)

    def run(self):
        #x = 0
        while True:
            uuid = get_target(recieve(self.input, analog_threshold), com_values, com_target_diff)
            command = get_target(recieve(self.input, analog_threshold), com_values, com_target_diff)
            add_list = [uuid, command]
            globals()['stack_list_' + str(self.id)].append(add_list)

    def start_recieving(self):
        self.start()
