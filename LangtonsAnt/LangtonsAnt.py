#!/usr/bin/python3
#
# (c) David Haworth
#
# This file is part of MathsFun.
#
# MathsFun is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MathsFun is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MathsFun.  If not, see <http://www.gnu.org/licenses/>.


# Langtons Ant
#
# On each tick, the ant moves one square straight ahead.
# The vacated square inverts its colour.
# If the new square is white, the ant turns 90 degrees right.
# If the new square is black, the ant turns 90 degrees left.
#
# By default, all squares are white.
#
# Professor Stewart's Cabinet of Mathematical Curiosities, page 141
# See also: https://en.wikipedia.org/wiki/Langton%27s_ant
#
# This implementation uses curses to plot the ant's movement in a terminal window (e.g. xterm)
# It should run on most unixy OSes and maybe on others if you install the right bits.
# Make your terminal window as large as possible.
#
# Usage:
#	LangtonsAnt.py [-d delay] [-p presets]

import sys
import getopt
import time
import curses

usage = 'Usage: LangtonsAnt.py [-d delay]\n'

grid = {}				# True = black, False = white
ant_dir = 0				# 0 = east, 1 = south, 2 = west, 3 = north
ant_pos = (0, 0)		# Initial position in the "infinite" grid
grid[ant_pos] = False	# The ant's initial square is white. Initialisation avoids a try..except

offx = 0				# These are calculated from the window size so that the ant starts in the centre.
offy = 0

dir_char = ['E', 'S', 'W', 'N']		# The ant is represented at each tick by a character showing its direction
presets_file = None					# Filename of presets file (-p option)

use_curses = True		# Set to False to get a log of the moves instead of a TUI image.
delay = 0.01			# Choose the tick interval. Real numbers are allowed.

try:
	(opts, args) = getopt.gnu_getopt(sys.argv[1:], 'hd:p:', ['help', 'delay=', 'presets='])
except getopt.GetoptError as err:
	# print help information and exit
	print()
	print(err)  # will print something like "option -a not recognized"
	print(usage)
	exit(1)

for (opt, optarg) in opts:
	if opt == '-h' or opt == '--help':
		print()
		print(usage)
		exit(0)
	if opt == '-d' or opt == '--delay':
		delay = float(optarg)
	if opt == '-p' or opt == '--presets':
		presets_file = optarg

if use_curses:
	window = curses.initscr()
	curses.curs_set(0)
	window.clear()
	curses.doupdate()
	#window.addstr(0, 0, 'Langton\'s Ant')
	#window.refresh()
	#time.sleep(5)
	#window.addstr(0, 0, '              ')
	maxyx = window.getmaxyx()
	offx = maxyx[1] // 2
	offy = maxyx[0] // 2
	window.addch(offy, offx, dir_char[ant_dir])
	window.refresh()

if presets_file != None:
	f = open(presets_file, 'r')
	for l in f:
		l = l.rstrip().lstrip()
		if l == '' or l[0] == '#':
			pass	# Ignore comment lines and blank lines
		else:
			coords = l.split(' ')
			pos = (int(coords[0]), int(coords[1]))
#			print('pos = ', pos)		#DEBUG
			grid[pos] = True
			if use_curses:
				window.addch(offy - pos[1], offx + pos[0], '*')
				window.refresh()
	f.close()
	time.sleep(1)


def NextPos(pos, d):
	x = pos[0]
	y = pos[1]
	if d == 0:
		x = x+1
	elif d == 1:
		y = y+1
	elif d == 2:
		x = x-1
	else:
		y = y-1
	return (x, y)

while True:

	old_pos = ant_pos
	ant_pos = NextPos(ant_pos, ant_dir)

	try:
		colour = grid[ant_pos]
	except:
		grid[ant_pos] = False	# Uninitialised squares are white
		colour = False

	if colour:
		# Black square: turn left (decrement)
		ant_dir = ant_dir - 1
		if ant_dir < 0:
			ant_dir = 3
	else:
		# White square: turn right (increment)
		ant_dir = ant_dir + 1
		if ant_dir > 3:
			ant_dir = 0

	old_colour = not grid[old_pos]		# New colour of old square
	grid[old_pos] = old_colour			# No try..except here; the square is initialised

	# Update the grid
	if use_curses:
		time.sleep(delay);
		if old_colour:
			ch = '*'
		else:
			ch = ' '
		try:
			window.addch(offy - old_pos[1], offx + old_pos[0], ch)
			window.addch(offy - ant_pos[1], offx + ant_pos[0], dir_char[ant_dir])
			window.refresh()
		except:
			window.addstr(0, 0, 'Langton\'s Ant hit a brick wall :-)')
			window.addstr(1, 0, '')
			curses.curs_set(1)
			window.refresh()
			# Don't use curses.endwin() because it clears the screen.
			break
	else:
		print(old_pos, old_colour, ant_pos, dir_char[ant_dir])

