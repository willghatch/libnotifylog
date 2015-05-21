#!/usr/bin/env python2

import glib
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def notifications(bus, message, logfile="/var/log/libnotify.log"):
    logfile = open(logfile, "a")
    notification = list(message.get_args_list())
    output = ""
    if len(notification) < 5:
        # I don't actually know what the fields are, since I'm just hacking
        # at someone else's script here... I should check that out sometime.

        #output = "Short Notification: "+str(output)
        pass
    else:
        output = "program: "+notification[0]+" subject: "+notification[3]+" body: "+notification[4]
    output += "\n"
    logfile.write(str(output))
    logfile.close()

# main...
import sys
logto = "/var/log/libnotify.log"
if len(sys.argv) > 1:
    logto = sys.argv[1]

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(lambda bus, message:notifications(bus, message, logfile=logto))

mainloop = glib.MainLoop()
mainloop.run()

