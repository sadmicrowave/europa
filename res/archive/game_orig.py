#!/usr/local/bin/python3

import sys, re, inspect, os, textwrap, shutil, jsonpickle

from res.bgcolors import BgColors
from world import World
from player import Player
from modules import actions
from modules import tiles
from modules import items
from modules import armor
from modules import weapons
from modules import potions
from modules import enemies
from modules import merchants
from modules import repair
from modules import money

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



You awaken, dizzy and confused.  The room around you feels like it is 
spinning, and the lights are flickering uncontrollably making it, almost 
impossible to see.   Where are you? You feel your head to find a severe 
wound that is bleeding.  What day is it?  You look down, you are wearing 
some sort of uniform.  It looks dirty and torn like you've been in a wreck.  

	""")

	action = False
	
	# check if there is a game save file with a previously saved state
	if os.path.exists('gsave.pkl') :
		# prompt the user to answer if they want to load from a saved state
		action_input = input( BgColors.HEADER + 'Load Saved Game? [y/n]: ' + BgColors.ENDC).lower()
	else :
		# otherwise the action input should be defaulted to no
		action_input = 'n'
	# check to see if the user wants to load the previously saved game state from the save file
	while True:
		# if the answer is yes, they want to load from the previous save, then attempt to load
		if action_input.lower() == 'y' :
			# open the save state file
			with open('gsave.pkl', 'r') as output:
				# assign player object as the pickled object, decoded
				player = jsonpickle.decode(output.read())
				# assign the world object as the player.world property
				world = player.world
			break
		# if the user answered no, they do not want to load from saved state, then start a new game and load all objects with original states
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
			world.load_money()
			world.load_wallet()
			world.load_tiles()
			player = Player(world)
			break
			
		# if the user didn't answer with a yes or no response, then loop again with an error message
		if action_input.lower() not in ['y','n'] :
			print("{}You must provide a [y/n] answer!{}".format(BgColors.FAIL, BgColors.ENDC))
	
	# These lines load the starting room and display the text
	player.room = world.tile_exists(player.location_x, player.location_y)

	# print the room intro text
	print(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', "\n" + player.room.intro_text(), flags=re.M))
	print( textwrap.fill("Type 'help' to view a full list of available actions and ways to interact within the game.",70) )	
	
	# Start the game loop
	while player.is_alive() and not player.victory:
		try :
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
				# get the terminal size, in height and width
				s = shutil.get_terminal_size()
				# print a solid line above the "Action:" prompt line for content separation
				print("_" * s.columns)
				# prompt the user to input an action
				action_input = input( BgColors.HEADER + 'Action: ' + BgColors.ENDC).lower()
				#os.system('clear')
				print("\n")
				action_found = False
				# loop over all available actions for the current tile to check the user action against those available
				for action in available_actions:
					#  If the human player provided a matching hotkey, then we execute the associated action using the do_action method.
					if action_input.strip().split(' ')[0] in action.hotkey:
						action_found = True
						# if there is a space in the command input, then split the content on the space, and use the second item as the key/index passed to the action command
						if len(action_input.split(' ',1)) > 1:
							action.kwargs.update( {'item': action_input.split(' ',1)[1]} )
	
						player.do_action(action, **action.kwargs)
						
						break
				# if the action was not found in the available action list
				if not action_found:
					print("{}You can't do that! Choose an action from the list below.\nExample: '[command] [#]' to interact with an item.{}".format(BgColors.FAIL, BgColors.ENDC))

		except KeyboardInterrupt:
			# if the game encounters the kill command, key stroke then stop first, before exiting and make sure user has saved
			while True:
				# prompt user for a response to being sure they want to quit
				exit_input = input( BgColors.HEADER + '\nAre you sure you want to quit? Did you remember to save? [y/n]: ' + BgColors.ENDC).lower()
				# if they select yes, they still want to quit
				if exit_input.lower() == 'y' :
					# then exit the game program
					sys.exit() 
				
				# if they select no, then they still want to play the game, just break out of the loop
				elif exit_input.lower() == 'n' :
					break

				# if they don't input either yes or no, then explain that they must select y,n
				elif exit_input.lower() not in ['y','n'] :
					print("{}You must provide a [y/n] answer!{}".format(BgColors.FAIL, BgColors.ENDC))

	# if the player has died
	if not player.is_alive():
		print("\n{}You died...{}".format(BgColors.FAIL, BgColors.ENDC))
            
if __name__ == "__main__":
	play()