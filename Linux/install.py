#!/usr/bin/env python
import shutil
from datetime import date
import time
import os
from xml.etree import ElementTree
from subprocess import call

symbol_dirs = ['/usr/share/X11/xkb/symbols', '/etc/X11/xkb/symbols']
rules_dir = '/usr/share/X11/xkb/rules'

def add_layout():
    for symbol_dir in symbol_dirs:
        if os.path.exists(symbol_dir):
            shutil.copyfile('gelatin_ansi-iso.xkb', os.path.join(symbol_dir, 'gelatin'))
            shutil.copyfile(os.path.join(rules_dir, 'evdev.xml'), 'evdev.xml.backup' + date.today().isoformat())
            first = None
            for filename in [os.path.join(rules_dir, 'evdev.xml'), 'gelatin_evdev_section.xml']:
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
