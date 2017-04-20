#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from _thread import start_new_thread    # import simple thread starter

# import basic functions of python
import os
import time


class bash():

    def __init__(self):
        # list of areas
        # the key is just for intermal use
        # name is shown on bash
        # data is a list of lines
        # max defines how much lines should be printed, 0 = all, n = n lines from the end
        self.content = {"logic": {"name": "Logic", "data": [], "max": 0},
                        "info": {"name": "Info", "data": [], "max": 10},
                        "com": {"name": "COM", "data": [], "max": 15}}
        self.content_order = ["info", "com", "logic"]
        self.rows, self.columns= self.getSize()  # calculate size of bash
        # init variables to save the content
        self.out = ""
        self.out_old = ""
        start_new_thread(self.thread, ())  # start worker

    def getSize(self):
        # get size
        rows, columns = os.popen('stty size', 'r').read().split()
        # convert to int
        rows = int(rows)
        columns = int(columns)
        return(rows, columns)

    def printline(self, line):
        # print line on bash (write it into string)
        # check whther there is enough space
        if self.rows <= 0:
            return
        self.out = self.out + "\n" + line[:self.columns]  # write line to string
        self.rows -= 1  # decrease row count

    def printCenter(self, text, fill=" "):
        # print line centered on bash (write it into string)
        space = self.columns - len(text)  # calculate space
        fill_first = int(round(space / 2))  # calcualte space in front of string
        line = ""  # init line variable
        # do not fill if line is to long
        if fill_first < 0:
            fill_first = 0
        # fill front of line
        for _ in range(fill_first):
            line = line + fill
        line = line + text  # add the main text
        fill_last = self.columns - len(line)  # calculate space at the end
        # do not fill if line is to long
        if fill_last < 0:
            fill_last = 0
        # fill end of line
        for _ in range(fill_last):
            line = line + fill
        self.printline(line)  # print line

    def output(self):
        self.out = ""#remove all content
        rows, self.columns= self.getSize()# calculate size of bash
        self.rows = rows#save amount of rows

        #some default printing
        self.printCenter("Status", "-")
        self.printline("Size: " + str(self.columns) + " x " + str(rows))
        #print each category
        for c in self.content_order:
            cat = self.content[c]
            self.printCenter(cat["name"], "-")#primt category name
            m = cat["max"]#get max line for this category
            #get all lines in case of infinitive
            if m == 0:
                d = cat["data"]
            #get x lines
            else:
                d = cat["data"][-m:]
            #print each line
            for line in d:
                self.printline(line)
            self.printline("")#print end line

        self.fill_empty()#fill empty lines

        self.rows = rows#save amount of rows
        #check whther output changed
        if self.out != self.out_old:
            print(self.out)#print output
            self.out_old = self.out#save current content as old data

    def fill_empty(self):
        # fill empty rows
        while self.rows > 1:
            self.printline("")

    def addData(self, cat, data):
        # add data (singleline/multiline)
        data = str(data)  # convert data to str
        d = data.split("\n")  # split by newline
        self.content[cat]["data"] = self.content[cat]["data"] + d  # add data to list

    def deleteData(self, cat):
        # delete data of category
        self.content[cat]["data"] = []

    def thread(self):
        # main thread to update bash
        time.sleep(3)  # waint some time
        while True:
            self.output()  # print on bash
            time.sleep(0.1)  # wait
