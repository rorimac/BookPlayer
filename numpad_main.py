#!/usr/bin/env python
# encoding: utf-8

"""
The main file for controlling the audio book reader through a numpad.
"""

__version_info__ = (0, 0, 1)
__version__ = '.'.join(map(str, __version_info__))
__author__ = "Andreas Söderlund"

from main import BookReader
from threading import Thread
try:
   # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk


class NumpadReader(BookReader):
        
        def __init__(self):
            BookReader.__init__()

            # Create self.book_options by reading the available books list
            self.read_book_options()
            self.position = 0
            self.number_books = len(self.book_options)

            # 0 is choosing book, 1 is listening to book
            self.mode = 0


        def read_book_options(self):
            bookfile = open('bookfile')
            bookstring = bookfile.read()
            # Split books on new line
            self.book_options = bookstring.split('\n')
            # If last element is empty string, remove it
            if not self.book_options[-1]:
                self.book_options[-1:] = []
            # Split book into name and id on delimiter ':'
            self.book_options = [individ_book.split(':') for individ_book in self.book_options]

        def navigate(self, n):
            # Navigate the books 
            self.position = (self.position + n)%self.number_books

        
        def key_pressed(self, event):
            # If in listening book mode
            if mode:
                if event.keysym in ['Right', 'KP_Right']:
                    pass
                elif event.keysym in ['Left', 'KP_Left']:
                    self.player.rewind(None)
                elif event.keysym in ['Up', 'KP_Up']:
                    self.player.status_light.action = 'blink_pauze'
                    self.player.mpd_client.pause()
                    self.mode = 0
                elif event.keysym in ['KP_begin', 'space']:
                    self.player.toggle_pause(None)
                elif event.keysym in ['Down', 'KP_Down']:
                    pass
            # If in choosing book mode
            else:
                if event.keysym in ['Right', 'KP_Right']:
                    self.navigate(1)
                    print '{}: {}'.format(self.position, self.options[self.position])
                elif event.keysym in ['Left', 'KP_Left']:
                    self.navigate(-1)
                    print '{}: {}'.format(self.position, self.options[self.position])
                elif event.keysym in ['Up', 'KP_Up']:
                    pass
                elif event.keysym in ['KP_begin', 'space']:
                    pass
                elif event.keysym in ['Down', 'KP_Down']:
                    self.mode = 1

if __name__ == '__main__':
    reader = NumpadReader()
    root = tk.Tk()
    root.bind_all('<Key>', reader.key_pressed)
    thread1 = Thread(target = reader.loop)
    thread2 = Thread(target = root.mainloop)
    thread1.setDaemon(True)
    thread2.setDaemon(True)
    thread1.start()
    thread2.start()
