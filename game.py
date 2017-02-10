#!/usr/local/bin/python3

import sys, re, inspect, os, textwrap, shutil, jsonpickle, csv

from modules.bgcolors import BgColors
from modules.world import World
from modules.player import Player
from modules import actions
from modules import tiles
from modules import items
from modules import armor
from modules import weapons
from modules import serums
from modules import enemies
from modules import merchants
from modules import repair

from tkinter import *
from openpyxl import load_workbook
from jsonpickle.unpickler import Unpickler
 
# The only way the program stops is if the player wins, loses, or quits. To handle this behavior, 
# games usually run inside a loop. On each iteration, the game state is updated and input is received 
# from the human player. In graphical games, the loop runs many times per second. Since we dont need
# to continually refresh the players screen for a text game, our code will actually pause until the player provides input. 
class App :

	def __init__(self):
		# override the standard sys output to redirect the typical built-in print() command
		sys.stdout.write = self.print_redirect

		self.next_method 	= None
		self.action 		= None
		self.tag			= None

		########### SETUP THE GAME WINDOW FRAME #############
		# Initialize the tkinter object
		self.root = Tk()
		# set window opacity
		self.root.attributes('-alpha', 0.85)
		self.root.geometry("900x800")
		# set the application title
		self.root.title("Dispoina - Adventure Game")
		
		# bind an event exection on the "enter" key user event
		self.root.bind('<Return>', self.inputText)
		
		# Set the frame background, font color, and size of the text window
		self.mainframe = Text(self.root, bg='black', fg='white')
		self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S)) 
		
		# The "columnconfigure"/"rowconfigure" bits just tell Tk that if the main window is resized, the frame should expand to take up the extra space.
		self.mainframe.columnconfigure(0, weight=1)
		self.mainframe.rowconfigure(0, weight=1)
		
		### Create the textbox for inputting commands
		# Declare the textbox variable
		self.inputline = StringVar()
		# initialize the textbox widget
		self.inputline_entry = Entry(self.root, textvariable=self.inputline)
		self.inputline_entry.grid(sticky=(W,E,S))
		
		# focus the cursor in the inputline action box
		self.inputline_entry.focus_set()
	
		# make the application window expandable
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_rowconfigure(0, weight=1)
	
		# initialize all the Text widget tag configurations to be used to change colors later
		BgColors(self.mainframe)
		
		self.print_intro()
		# attempt to load previous game state, or create new game state if no previous is found
		self.load_game_state()
	
	
	def inputText(self, event):
		# get the text from the input box
		i = self.inputline.get().lower()
		# delete the contents from the input box
		self.inputline_entry.delete(0,'end')
		# send the contents of the input box to the print function
		print("\n" + BgColors.NORMAL + "Your Action: " + i )
		# execute the next method in line, set by previous call
		#eval('self.%s(%s)' % (self.next_method, i))
		self.next_method(i)
	
	
	def print_redirect(self, inputStr):
		# set an empty tag tuple
		#tag = ('NORMAL',)
		tag = None
		if BgColors.HEADER in inputStr :
			tag = ('HEADER',)
		elif BgColors.OKBLUE in inputStr :
			tag = ('OKBLUE',)
		elif BgColors.SKYBLUE in inputStr :
			tag = ('SKYBLUE',)
		elif BgColors.CADETBLUE in inputStr :
			tag = ('CADETBLUE',)
		elif BgColors.OKGREEN in inputStr :
			tag = ('OKGREEN',)
		elif BgColors.WARNING in inputStr :
			tag = ('WARNING',)
		elif BgColors.FAIL in inputStr :
			tag = ('FAIL',)
		elif BgColors.NORMAL in inputStr :
			tag = ('NORMAL',)
		elif BgColors.ENDC in inputStr:
			tag = ()
		
		if not tag and self.tag :
			tag = self.tag
			
		self.tag = tag
		
		
		# replace reference to [color] and [endc] identifier in text string
		inputStr = re.sub(r'(\[!\w+!])', '', inputStr)
		# add the text to the window widget
		self.mainframe.configure(state='normal')
		self.mainframe.insert("end-1c", inputStr, tag)
		self.mainframe.configure(state='disabled')
		# automtically scroll to the end of the mainframe window
		self.mainframe.see(END)
	
		
	
	def load_game_state(self):
		# check if there is a game save file with a previously saved state
		if os.path.exists('res/gsave.pkl') :
			# prompt the user to answer if they want to load from a saved state
			#action_input = input( BgColors.HEADER + 'Load Saved Game? [y/n]: ' + BgColors.ENDC).lower()
			print( BgColors.HEADER + '\n\nLoad Saved Game? [y/n]: ' + BgColors.ENDC )
			self.next_method = self.load_game_state_check
		# otherwise a save file was not found
		else :
			# create the world state from scratch
			self.create_new_world()
	
	
			
	def load_game_state_check(self, input):
		# if the answer is yes, they want to load from the previous save, then attempt to load
		if input.lower() == 'y' :
			# open the save state file
			with open('res/gsave.pkl', 'r') as output:
				# assign player object as the pickled object, decoded
				self.player = jsonpickle.decode(output.read())
				# assign the world object as the player.world property
				self.world = self.player.world
	
			self.load_starting_position()
		# if the user answered no, they do not want to load from saved state, then start a new game and load all objects with original states
		elif input.lower() == 'n' :
			self.create_new_world()
			
		# if the user didn't answer with a yes or no response, then loop again with an error message
		elif input.lower() not in ['y','n'] :
			print("{}You must provide a [y/n] answer!{}".format(BgColors.FAIL, BgColors.ENDC))
			self.load_game_state()
	
	
	
	
	def create_new_world(self):
		self.world = World()
		# load all world objects
		self.world.load_armor()
		self.world.load_weapons()
		self.world.load_serums()
		self.world.load_barrier_items()
		self.world.load_items()
		self.world.load_notes()
		self.world.load_enemies()
		self.world.load_merchants()
		self.world.load_repair()
		self.world.load_money()
		self.world.load_containers()
		self.world.load_wallet()
		self.world.load_tiles()
		self.player = Player(self.world)
		
		self.load_starting_position()


	def load_starting_position(self):
		# These lines load the starting room and display the text
		self.player.room = self.world.tile_exists(self.player.location_x, self.player.location_y)

		# print the room intro text
		#print(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', "\n" + BgColors.NORMAL + self.player.room.intro_text() + BgColors.ENDC, flags=re.M))
		print(BgColors.NORMAL + "─"*70)
		print(BgColors.NORMAL + "\n" + self.player.room.intro_text() + BgColors.ENDC)
		self.world.tile_exists(self.player.location_x, self.player.location_y).visited = True
		
		# start the main play execution sequence
		self.play()

	
	def play(self):
		
		# check if the player is alive, end game if not
		if not self.player.is_alive() :
			self.end_game()
		
		# if player is alive, and has not achieved victory, then continue with main logic
		elif not self.player.victory :
				
			# The first thing the loop does is find out what room the player is in and then executes the behavior for that room.
			self.player.room = self.world.tile_exists(self.player.location_x, self.player.location_y)
				
			if not (isinstance(self.action, (actions.ItemAction,actions.HiddenAction))) and ( (issubclass(self.player.room.__class__, tiles.EnemyRoom) and isinstance(self.action, actions.Attack)) or issubclass(self.player.room.__class__, tiles.LeaveCaveRoom) ):
				self.player.room.modify_player(self.player)

			# display the mini help options for available options (not extended help view)
			if not isinstance(self.action, actions.HiddenAction):
				self.player.help()
										
			# prompt the user to input an action
			#print(BgColors.HEADER + '\n\nAction: ' + BgColors.ENDC, end='')
			self.next_method = self.do_action_check
			self.inputline_entry.focus()

			
	
	def do_action_check(self, input):
		# get the available actions for the room from the available actions method in each tile class
		available_actions = self.player.room.available_actions(self.player)
		
		action_found = False
		for action in available_actions:
			#  If the human player provided a matching hotkey, then we execute the associated action using the do_action method.
			if input.strip().split(' ')[0] in action.hotkey:
				action_found = True
				# if there is a space in the command input, then split the content on the space, and use the second item as the key/index passed to the action command
				if len(input.split(' ',1)) > 1:
					action.kwargs.update( {'item': input.split(' ',1)[1]} )
				
				# set the instance action attribute for use in other class methods	
				self.action = action
				print("\n" + BgColors.NORMAL + "─"*70)
				self.player.do_action(action, **action.kwargs)
	
				break
		# if the action was not found in the available action list
		if not action_found:
			self.action = None
			print("\n" + BgColors.NORMAL + "─"*70)
			print("{}You can't do that! Choose an action from the list below.\nExample: '[command] [#]' to interact with an item.{}".format(BgColors.FAIL, BgColors.ENDC))
		
			#self.player.help()
		# execute the self.play() iteration again to maintain the loop
		self.play()
	
	
	def game_end(self):
		if not self.player.is_alive():
			print("\n{}You died...{}".format(BgColors.FAIL, BgColors.ENDC))
	
	
	def print_intro(self):
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



Type 'help' to view a full list of available actions and ways to 
interact within the game.                                                                           

""" )


class Environment:
	def __init__(self):
		self.map_file = 'res/map.xlsx'
		self.map_output = 'map.txt'
	
	# create the tab delimited file from the map xlsx document, if found
	def convert_xlsx(self):
		if os.path.isfile(self.map_file):
			wb = load_workbook(self.map_file)
			sh = wb.get_sheet_by_name(self.map_output)
			
			with open("res/%s" % self.map_output, 'w') as f:
				c = csv.writer(f, delimiter='\t')
				for r in sh.rows:
					c.writerow([cell.value for cell in r])




if __name__ == "__main__":
	try:
		e = Environment()
		e.convert_xlsx()

		a = App()
		a.root.mainloop()
		
		
	except Exception:
		raise
	
	