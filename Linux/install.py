#!/usr/bin/env python
import shutil
from datetime import date
import os
from xml.etree import ElementTree as et
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
                data = et.parse(filename).getroot()
                if first is None:
                    if data.find('gelatin'):
                        break
                    first = data
                    first_layout = first.find('layoutList')
                else:
                    layout_list = data.find('layoutList')
                    first_layout.extend(layout_list)

            if first is not None:
                with open(os.path.join(rules_dir, 'evdev.xml'), "w") as f:
                    f.write(et.tostring(first, encoding='utf-8'))


def switch_layout(variant=None):
    set_command = ['setxkbmap', '-v', 'gelatin']
    if variant is not None:
        set_command.extend(['-variant', variant])
    if call(set_command) == 0:
        print 'Successfully set keyboard to Gelatin'
    else:
        print 'Failed to set keyboard to Gelatin'
        print 'Debug information:'
        print call(set_command, '|', 'xkbcomp', '-')

if __name__ == "__main__":
    add_layout()
    switch_layout()
