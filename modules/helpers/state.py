#!/usr/local/bin/python3

import sys, jsonpickle
from modules.bgcolors import BgColors
from modules.helpers.health import Health


class State(object):
	#################################################################################################################################
	# SETUP WAYS TO LEAVE THE GAME

	@classmethod
	def game_end(cls):
		print("\n{}You died...{}".format(BgColors.FAIL, BgColors.ENDC))
	
	@classmethod
	def exit(cls):
		"""Exit the game rooms to win."""
		# set victory variable within the player object to true, for the next while iteration within Game.py to detect victory
		#player.victory = True
		# print exit text
		print( textwrap.fill("Being lost in this cavern was terrible. but as you emerge, you find yourself on a mountain ridge, overlooking a lively city in the distance.  It's over.  You are safe.\n\n Thank you for playing.\n\n",70))
		cls.quit()
	
	@classmethod	
	def save(cls, **kwargs):
		"""Save the current state of the game."""
		try :
			# open the file to use for saving the game state, as writable
			with open('gsave.pkl', 'w') as output:
				# write the output of jsonpickling the Player object to the file
				output.write( jsonpickle.encode(kwargs['player']) )
			# print successful game save message
			print("{}Game state successfully saved.{}".format(BgColors.OKGREEN, BgColors.ENDC))
		except Exception as e:
			# if there was an error saving the game, then provide an error message
			print("{}There was an error saving the game.  Sorry.\n{}{}".format(BgColors.FAIL, e, BgColors.ENDC))
			
	
	@classmethod
	def quit(cls, **kwargs):
		"""Quit the current game, and save."""
		cls.save(**kwargs)
		sys.exit()
