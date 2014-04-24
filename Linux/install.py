#!/usr/bin/env python
import shututil
import date
import datetime
import os
from xml.etree import ElementTree
from future import with_statement
from subprocess import call

symbol_dirs = ['/usr/share/X11/xkb/symbols', '/etc/X11/xkb/symbols']


def add_layout():
    for symbol_dir in symbol_dirs:
        if os.path.exists(symbol_dir):
            shututil.copyfile('gelatin_ansi-iso.xkb', os.path.join(symbol_dir, 'gelatin'))
            shututil.copyfile(os.path.join(symbol_dir, 'evdev.xml', 'evdev.xml.backup' + date.isoformat(datetime.today())))
            first = None
            for filename in [os.path.join(symbol_dir, 'evdev.xml'), 'gelatin_evdev_section.xml']:
                data = ElementTree.parse(filename).getroot()
                if first is None:
                    first = data
                else:
                    first.extend(data)
            if first is not None:
                with open(os.path.join(symbol_dir, 'evdev.xml'), "w") as f:
                    f.write(ElementTree.tostring(first))  # write the new line before


def switch_layout():
    if call("setxkbmap -v us -variant gelatin"):
        print 'Successfully set keyboard to Gelatin'

if __name__ == "__main__":
    add_layout()
    switch_layout()
