#!/usr/bin/env python
import shutil
from datetime import date
import os
from xml.etree import ElementTree as et
from xml.dom import minidom
from subprocess import call

symbol_dirs = ['/usr/share/X11/xkb/symbols', '/etc/X11/xkb/symbols']
rules_dir = '/usr/share/X11/xkb/rules'


class XMLCombiner(object):
    def __init__(self, filenames):
        assert len(filenames) > 0, 'No filenames!'
        # save all the roots, in order, to be processed later
        self.roots = [et.parse(f).getroot() for f in filenames]

    def combine(self):
        for r in self.roots[1:]:
            # combine each element with the first one, and update that
            self.combine_element(self.roots[0], r)
        # return the string representation
        return et.tostring(self.roots[0],'utf-8', method="xml")

    def combine_element(self, one, other):
        """
        This function recursively updates either the text or the children
        of an element if another element is found in `one`, or adds it
        from `other` if not found.
        """
        # Create a mapping from tag name to element, as that's what we are fltering with
        mapping = {el.tag: el for el in one}
        for el in other:
            if len(el) == 0:
                # Not nested
                try:
                    # Update the text
                    mapping[el.tag].text = el.text
                except KeyError:
                    # An element with this name is not in the mapping
                    mapping[el.tag] = el
                    # Add it
                    one.append(el)
            else:
                try:
                    # Recursively process the element, and update it in the same way
                    self.combine_element(mapping[el.tag], el)
                except KeyError:
                    # Not in the mapping
                    mapping[el.tag] = el
                    # Just add it
                    one.append(el)


def add_layout():
    for symbol_dir in symbol_dirs:
        if os.path.exists(symbol_dir):
            shutil.copyfile('gelatin_ansi-iso.xkb', os.path.join(symbol_dir, 'gelatin'))
            shutil.copyfile(os.path.join(rules_dir, 'evdev.xml'), 'evdev.xml.backup' + date.today().isoformat())
            evdev = XMLCombiner((os.path.join(rules_dir, 'evdev.xml'), 'gelatin_evdev_section.xml')).combine()
            with open(os.path.join(rules_dir, 'evdev2.xml'), 'w') as output:
                output.write(evdev)


def switch_layout():
    if call(['setxkbmap', '-v', 'us', '-variant', 'gelatin']):
        print 'Successfully set keyboard to Gelatin'
    else:
        print 'Failed to set keyboard to Gelatin'

if __name__ == "__main__":
    add_layout()
    switch_layout()
