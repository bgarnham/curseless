#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from os import access, R_OK
from os.path import expanduser, normpath, isfile

def curseless(object, path):
    """curseless.curseless(object, string)
    called by less to which adds curses wrapper
    do not call directly, see curseless.less for details
    """
    if path == None:
        return
    else:
        path = normpath(expanduser(path))
    
    if not isfile(path) or not access(path, R_OK):
        text = path
    else:
        with open(path, 'rt') as f:
            text = f.read()

    #equivalent of stdscr, fullscreen window
    #ystart, xstart, height, width
    stdscr = curses.newwin(0, 0, curses.LINES-1, curses.COLS-1)
    # word wrap
    x = []
    maxlen = curses.COLS
    #split text to list on newlines and loop
    for i in text.split('\n'):
        start = 0
        end = 0
        while end < len(i):
            #if it's not the end of the string
            if start + maxlen < len(i):
                    # split off the string from the current start
                    # to the space closest to the max length
                    end = i.rfind(' ', start, start+maxlen) + 1
                    #if there are no spaces, cut off at max length
                    if end == 0:
                        end = maxlen
                    # append to temp array
                    x.append(i[start:end])
                    # set start position for next iteration
                    start = end
            else:
                # at end of string, append tail,
                # move to next string
                end = len(i)
                x.append(i[start:end])
    rows = len(x) + 10
    text = '\n'.join(x)

    def refresh_pad():
        pad.refresh(curr_row,0, 0,0, curses.LINES-1,curses.COLS-1)

    stdscr = curses.initscr()
    # suppress stdin output to to screen
    curses.noecho()
    # receive key input without [enter]
    curses.cbreak()
    # suppress cursor
    curses.curs_set(False)
    # overflowed window to display text
    pad = curses.newpad(rows, curses.COLS)
    # add test string to pad
    pad.addstr(0, 0, text.encode('utf-8'))
    #refresh pad to display new text
    # pad ul, window ul, window lr
    curr_row = 0
    refresh_pad()

    while True:
        k = stdscr.getch()
        if k == 113: # 'q'uit
            break
        if k == 258: # arrow down
            if curr_row < rows - curses.LINES:
                curr_row += 1
                refresh_pad()
        if k == 259: # arrow up
            if curr_row > 0:
                curr_row -= 1
                refresh_pad()
        if k == 338: # page down
            if curr_row + curses.LINES * 2 < rows:
                curr_row += curses.LINES
                refresh_pad()
            else:
                curr_row = rows - curses.LINES
                refresh_pad()
        if k == 339: # page up
            if curr_row - curses.LINES > 0:
                curr_row -= curses.LINES
                refresh_pad()
            else:
                curr_row = 0
                refresh_pad()
   
def less(path):
    """curseless.less(string)
    Python 2.7 / 3.6 curses terminal based text viewer.
    It currently takes a path string argument to display
    file at the given path. Note: less acts as a 
    calling function, placing curseless in a wrapper.
    It's a pretty safe bet that your terminal will not
    take kindly to you call curseless directly.
    """
    curses.wrapper(curseless, path)


