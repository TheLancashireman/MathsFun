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
# To start with, all squares are white.
#
# Professor Stewart's Cabinet of Mathematical Curiosities, page 141
# See also: https://en.wikipedia.org/wiki/Langton%27s_ant
#
# This implementation uses curses to plot the ant's movement in a terminal window (e.g. xterm)
# It should run on most unixy OSes and maybe on others if you install the right bits.
# Make your terminal window as large as possible.

import time
import curses

grid = {}				# True = black, False = white
ant_dir = 0				# 0 = east, 1 = south, 2 = west, 3 = north
ant_pos = (0, 0)		# 
grid[ant_pos] = False	# The ant's initial square is white. Initialisation avoids a try..except

offx = 0				# These are calculated from the window size so that the ant starts in the centre.
offy = 0

dir_char = ['E', 'S', 'W', 'N']		# The ant is represented at each tick by a character showing its direction

use_curses = True		# Set to False to get a log of the moves instead of a TUI image.
delay = 0.01			# Choose the tick interval. Real numbers are allowed.

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
	time.sleep(delay)

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
		if old_colour:
			ch = '*'
		else:
			ch = ' '
		window.addch(old_pos[1] + offy, old_pos[0] + offx, ch)
		window.addch(ant_pos[1] + offy, ant_pos[0] + offx, dir_char[ant_dir])
		window.refresh()
	else:
		print(old_pos, old_colour, ant_pos, dir_char[ant_dir])

	time.sleep(delay);
