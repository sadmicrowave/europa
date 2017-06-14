#!/usr/local/bin/python3

import textwrap
from modules import tiles
from modules.bgcolors import BgColors

class aMap(object):
	
	@classmethod
	def __act__(cls, item=None, **kwargs):
		"""Show the map of where the player has been."""
		player = kwargs['player']
		
		print(textwrap.fill("{}Printing map of where you have been.  Tiles are displayed with x,y coordinates for easy location reference.{}\n".format(BgColors.WARNING, BgColors.ENDC),70))
		
		# set grid to view.  Grid will present visited tiles/rooms within a x,y range of current location
		# set positive x,y grid ranges in tuple form
		axis_x = 10
		axis_y = 10
		
		normalized_grid_origin = (axis_x/2, axis_y/2)
		
		# create an empty list to hold the tiles where we have been
		buf = []
		tot = vis = enemy_tot = enemy_vis = 0
		# print the grid based on current coordinate view
		for key,tile in player.world.__dict__.items() :
			if isinstance(tile,tiles.MapTile) :
				tot += 1
				enemy_tot += 1 if isinstance(tile, tiles.EnemyRoom) else 0
				if tile.is_visited() :
					vis += 1
					enemy_vis += 1 if isinstance(tile, tiles.EnemyRoom) else 0
					
					# ensure the x,y axis position is within our range (set above) from center-tile (current location)
					if ( abs( tile.x - player.room.x ) <= normalized_grid_origin[0] ) and ( abs( tile.y - player.room.y ) <= normalized_grid_origin[1] ):
						# if the position logic is true, then add the tile to the buffer list for next iteration set
						buf.append( tile )
				
		buf = sorted(buf, key=lambda b:(b.y, b.x))
		
		print("\n{}World Stats: {}% Visited - {}/{} Areas. {}/{} Enemies. {}".format(BgColors.NORMAL, round(vis/tot*100,2), vis, tot, enemy_vis, enemy_tot, BgColors.ENDC))
		
		print("\n{}{} = Current Location".format(BgColors.WARNING, u"\u2588"*2))
		print("{}{} = 1st level".format(BgColors.SKYBLUE, u"\u2588"*2))
		print("{}{} = 2nd level".format(BgColors.CADETBLUE, u"\u2588"*2))
		
		line_text = ""
		# iterate over y axis grid range, each line will print a new position tile
		y_min = int(0 if player.room.y - normalized_grid_origin[1] < 0 else player.room.y - normalized_grid_origin[1])
		y_max =	int(axis_y if player.room.y + normalized_grid_origin[1] < axis_y else player.room.y + normalized_grid_origin[1])
		
		x_min = int(0 if player.room.x - normalized_grid_origin[0] < 0 else player.room.x - normalized_grid_origin[0])
		x_max = int(axis_x if player.room.x + normalized_grid_origin[0] < axis_x else player.room.x + normalized_grid_origin[0])

		for y in range(y_min,y_max) :
			# break to a new line and add the prefixing grid pipe
			#line_text += "\n{:<3}   | ".format(y)
			print("\n{}{:<4}| ".format(BgColors.NORMAL, y), end='' )
			# # iterate over y axis grid range, each line will print a new position tile
			#for x in range(0,axis_x) :
			for x in range(x_min,x_max) :
				found_x = False
				# iterate over the tiles in buf to get the x and y coordinate, to see if something exists on the x,y coordinate plane we are on currently
				for tile in buf :
					# if the tile x position matches the current iterated x range, and the y position matches the current iterated y range, then provide a square
					if tile.x == x and tile.y == y :
						found_x = True
						color_ = None
						if tile.floor == 1 :
							color_ = BgColors.SKYBLUE
						elif tile.floor == 2 :
							color_ = BgColors.CADETBLUE
						elif tile.floor == 3 :
							color_ = BgColors.WARNING
						else :
							color_ = BgColors.FAIL
						
						#line_text += "{} ".format(u"\u2588"*2) if tile.x == player.room.x and tile.y == player.room.y else "{} ".format(u"\u2591"*2)
						s = "{}{} ".format(BgColors.WARNING, u"\u2588"*2) if tile.x == player.room.x and tile.y == player.room.y else "{}{} ".format(color_, u"\u2588"*2)
						#s = "{}{} ".format(color_, "  ") if tile.x == player.room.x and tile.y == player.room.y else "{}{} ".format(BgColors.NORMAL, "  ")
						print(s, end='')
					
				# if we didn't find an x coordinate tile during our x axis loop, then provide empty spaces
				if not found_x :
					#line_text += "   "
					print("   ", end='' )

		#print( line_text )
		print('')
		
		# print bottom x axis grid
		print("      {}{}".format(BgColors.NORMAL, "―― "*axis_x)) # 2 underscores = 2 x axis spaces per tile
		# print the x coordinate integers
		x_axis_int = ''
		print( '    ',''.join([x_axis_int + " {}{} ".format(BgColors.NORMAL, x) for x in range(x_min,x_max)]) )
		
		
