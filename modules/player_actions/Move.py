#!/usr/local/bin/python3

import textwrap
from modules.bgcolors import BgColors

class aMove(object):

	@classmethod
	def move(cls, dx, dy, player):
		if not player.has_light():
			print( BgColors.NORMAL + textwrap.fill("It is too dark to see.  You must discover how to light the way before continuing.  Use the [search] command to view items within the room, or the [i] command to view items within your inventory.\n",70) )
		else:
			# set the previous location x,y to the current location x,y before we change rooms/tiles so we know where we were at the last move
			player.prev_location_x = player.location_x
			player.prev_location_y = player.location_y
			# set the new coordinates x and y for moving
			player.location_x += dx
			player.location_y += dy
			
			intro_text = player.world.tile_exists(player.location_x, player.location_y).intro_text(player)
			if intro_text :
				print(BgColors.NORMAL + "\n" + textwrap.fill( intro_text, 70)  + BgColors.ENDC)
				#print( re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', BgColors.NORMAL + player.world.tile_exists(player.location_x, player.location_y).intro_text().replace(r'\n','\n'), flags=re.M) )
			
			# set the bool for knowing if we have visited this room/tile before
			player.world.tile_exists(player.location_x, player.location_y).visited = True
	
	@classmethod
	def move_north(cls, **kwargs):
		player = kwargs['player']
		cls.move(dx=0, dy=-1, player=player)
	
	@classmethod
	def move_south(cls, **kwargs):
		player = kwargs['player']
		cls.move(dx=0, dy=1, player=player)
	
	@classmethod
	def move_east(cls, **kwargs):
		player = kwargs['player']
		cls.move(dx=1, dy=0, player=player)
	
	@classmethod
	def move_west(cls, **kwargs):
		player = kwargs['player']
		cls.move(dx=-1, dy=0, player=player)