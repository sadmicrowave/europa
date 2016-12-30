#!/usr/local/bin/python3

import re, inspect, os, textwrap, shutil, jsonpickle

from res.bgcolors import BgColors
from world import World
from player import Player
from modules import actions
from modules import items
from modules import tiles

from jsonpickle.unpickler import Unpickler
 
# The only way the program stops is if the player wins, loses, or quits. To handle this behavior, 
# games usually run inside a loop. On each iteration, the game state is updated and input is received 
# from the human player. In graphical games, the loop runs many times per second. Since we dont need
# to continually refresh the players screen for a text game, our code will actually pause until the player provides input. 

def play():

	os.system('clear')
	print( """
 ______   ________   ______   _______     ___   _____  ____  _____       _       
|_   _ `.|_   __  |.' ____ \ |_   __ \  .'   `.|_   _||_   \|_   _|     / \      
  | | `. \ | |_ \_|| (___ \_|  | |__) |/  .-.  \ | |    |   \ | |      / _ \     
  | |  | | |  _| _  _.____`.   |  ___/ | |   | | | |    | |\ \| |     / ___ \    
 _| |_.' /_| |__/ || \____) | _| |_    \  `-'  /_| |_  _| |_\   |_  _/ /   \ \_  
|______.'|________| \______.'|_____|    `.___.'|_____||_____|\____||____| |____| 

Copyright (C) 2015  Corey Farmer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>                                                                                



	""")

	action = False
	
	if os.path.exists('gsave.pkl') :
		action_input = input( BgColors.HEADER + 'Load Saved Game? [y/n]: ' + BgColors.ENDC).lower()
	else :
		action_input = 'n'
	
	while True:
		if action_input.lower() == 'y' :
			
					
#			with open('gsave.pkl', 'rb') as output:
#				player = dill.load(output)
#			
#			print( player )
# 			with open('gsave.pkl', 'r') as output:
# 				world = World()
# 				# load all world objects
# 				world.load_armor()
# 				world.load_weapons()
# 				world.load_potions()
# 				world.load_barrier_items()
# 				world.load_items()
# 				world.load_notes()
# 				world.load_enemies()
# 				world.load_merchants()
# 				world.load_repair()
# 				world.load_gold()
# 				world.load_purse()
# 				world.load_tiles()
# 				
# 							
# 				player = jsonpickle.decode(output.read())
# 				world = player.world
# 				
# 				print ( player, player.__dict__ )
# 				#print( player.room )
# 				for k,v in player.__dict__.items():
# 					if hasattr(v,'py/object'):
# 						pass
# 					#if isinstance(v,str) :# or isinstance(v, dict):
# 					#	player.__dict__[k] = jsonpickle.decode(v)
# 				
# 				
# 				print ( player, player.__dict__ )		
			break
		elif action_input.lower() == 'n' :
			world = World()
			# load all world objects
			world.load_armor()
			world.load_weapons()
			world.load_potions()
			world.load_barrier_items()
			world.load_items()
			world.load_notes()
			world.load_enemies()
			world.load_merchants()
			world.load_repair()
			world.load_gold()
			world.load_purse()
			
			world.load_tiles()
			
			
			player = Player(world)
			break
			
		if action_input.lower() not in ['y','n'] :
			print("{}You must provide a [y/n] answer!{}".format(BgColors.FAIL, BgColors.ENDC))
			
	

	
	
		
	# These lines load the starting room and display the text
	player.room = world.tile_exists(player.location_x, player.location_y)
		
	print(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', "\n" + player.room.intro_text(), flags=re.M))
	print( "\n",textwrap.fill("Type 'help' to view a full list of available actions and ways to interact within the game.",70) )
	
	
	# Start the game loop
	while player.is_alive() and not player.victory:
	
		# The first thing the loop does is find out what room the player is in and then executes the behavior for that room.
		player.room = world.tile_exists(player.location_x, player.location_y)
		
		if not (isinstance(action, (actions.ItemAction,actions.HiddenAction))) and ( (issubclass(player.room.__class__, tiles.EnemyRoom) and isinstance(action, actions.Attack)) or issubclass(player.room.__class__, tiles.LeaveCaveRoom) ):
			player.room.modify_player(player)
		
		# Check again since the room could have changed the player's state
		if player.is_alive() and not player.victory:
			
			# display the mini help options for available options (not extended help view)
			if not isinstance(action, actions.HiddenAction):
				player.help()
			# find the user tile that the player is currently moving to
			player.room = world.tile_exists(player.location_x, player.location_y)
			# get the available actions for the room from the available actions method in each tile class
			available_actions = player.room.available_actions(player)
			
			s = shutil.get_terminal_size()
			print("_" * s.columns)
			action_input = input( BgColors.HEADER + 'Action: ' + BgColors.ENDC).lower()
			print("\n")
			action_found = False
			for action in available_actions:
				#  If the human player provided a matching hotkey, then we execute the associated action using the do_action method.
				if action_input.split(' ')[0] in action.hotkey:
					action_found = True
					
					#print( "Action:", action.__class__, isinstance(action, actions.PickUp), len([x for x in player.room.objects if not issubclass(x.__class__,items.Chest)]) )
								
					#if isinstance(action, actions.PickUp) : #and len([x for x in player.room.objects if not issubclass(x.__class__,items.Chest)]) > 1:		
					#if isinstance(action, (actions.ItemAction,actions.MerchantAction)) or (isinstance(action, actions.PickUp) and len(player.room.objects) > 1):
						#try:
							#print( 'hello:', action_input.split(' ',1)[1] )
					if len(action_input.split(' ',1)) > 1:
						action.kwargs.update( {'item': action_input.split(' ',1)[1]} )
						#except IndexError:
							#print( textwrap.fill("{}You must specify a value with an action!  There must be multiple items in the room. Use the search command to view items within the room.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
						#	break

					player.do_action(action, **action.kwargs)
					
					break
				
			if not action_found:
				print("{}You can't do that!{}".format(BgColors.FAIL, BgColors.ENDC))

			
	if not player.is_alive():
		print("\n{}You died...{}".format(BgColors.FAIL, BgColors.ENDC))
            
if __name__ == "__main__":
	play()