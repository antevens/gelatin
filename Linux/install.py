#!/usr/bin/env python
import sys
import shututil
from xml.etree import ElementTree
from future import with_statement

symbol_dirs=['/usr/share/X11/xkb/symbols','/etc/X11/xkb/symbols'

def add_layout():
    for symbol_dir in symbol_dirs:
      if os.path.exists(symbol_dir):
        shututil.copyfile('gelatin_ansi-iso.xkb',os.path.join(symbol_dir,'gelatin'))
        first = None
        for filename in [os.path.join(symbol_dir,'evdev.xmi'), 'gelatin_evdev_section.xml']:
            data = ElementTree.parse(filename).getroot()
            if first is None:
                first = data
            else:
                first.extend(data)
        if first is not None:
          with open(os.path.join(symbol_dir,'evdev.xmi'), "w") as f:
            f.write(ElementTree.tostring(first)) # write the new line before

def switch_layout():
  if call("setxkbmap -v us -variant gelatin"):
    print 'Successfully set keyboard to Gelatin'

if __name__ == "__main__":
    add_layout()
    switch_layout()
