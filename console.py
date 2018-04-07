#!/usr/bin/env python2
from __future__ import print_function
import cmd
import os
import re
import serial
import thread
import time
import readline
import atexit

commands = []
def mainLoop(threadName, delay):

    ser.read(1) # for /dev/tty.wchusbserial*
    count = 0
    while True:
        out = ''
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ("->%s" % out, end = '')


class MarlinConsole(cmd.Cmd):
    prompt = ""

    def do_listall(self, line):
        print(commands)

    def default(self, line):
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_test(self, *args):
        line = "G1 X440 Y440"
        ser.write("%s\n" % line)
        print ("<-%s" % line)

        line = "G1 X0 Y0"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_test1(self, *args):
        line = "G1 F4000"
        ser.write("%s\n" % line)
        print ("<-%s" % line)

        for i in range(0, 10):
            line = "G1 X0 Y0"
            ser.write("%s\n" % line)
            print ("<-%s" % line)

            line = "G1 X20 Y20"
            ser.write("%s\n" % line)
            print ("<-%s" % line)

    def do_pos(self, *args):
        """It sending M114 to Marlin and except position information
        """
        line = "M114"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_ms(self, *args):
        """
        """
        line = "M17"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_mp(self, *args):
        """
        """
        line = "M18"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_sp(self, *args):
        """
        """
        line = "G1 F%s" % args[0]
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_estop(self, *args):
        """
        """
        line = "M112"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_stop(self, *args):
        """
        """
        line = "M77"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_pause(self, *args):
        """
        """
        line = "M76"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_start(self, *args):
        """
        """
        line = "M75"
        ser.write("%s\n" % line)
        print ("<-%s" % line)
        commands.append(line)

    def do_exit(self, *args):
        return True


if __name__ == '__main__':

    print ('Select the serial port')
    devs = [f for f in os.listdir('/dev/') if re.match(r'tty\.|ttyU', f)]
    i = 1
    for dev in devs:
        print ("% d for /dev/" % i + dev)
        i += 1

    input = input()
    port = "/dev/%s" % devs[int(input)-1]

    print (port)
    try:
        historyFile = os.path.join(os.environ['HOME'], '.marlin_history')
        readline.read_history_file(historyFile)
        for line in open(historyFile).readlines():
            commands.append(line.strip())
    except IOError:
        pass
    #readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("bind ^I rl_complete")
    readline.set_history_length(1000)
    atexit.register(readline.write_history_file, historyFile)

    ser = serial.Serial(
        port=port,
        baudrate=115200,
    )
    if ser.isOpen():
        ser.close()
    ser.open()
    thread.start_new_thread(mainLoop, ("MainLoop", 1, ))

    mc = MarlinConsole()
    try:
        mc.cmdloop()
    except KeyboardInterrupt:
        mc.do_exit()
