#!/usr/local/bin/python3

import textwrap
from modules.bgcolors import BgColors
from modules import items

class aUnEquip(object):
	
	@classmethod
	def __act__(cls, item=None, **kwargs):
		player = kwargs['player']
		
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = player.select_item(item, player.inventory)
		# if the user did not pass an item to interact with, then...
		else:
			# print an error message stating an item reference must be passed
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		if not list(filter(None.__ne__, item)):
			# print an error if the item cannot be found
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0]
			if isinstance(item, items.Wallet):
				print("{}You're going to need your wallet...{}".format(BgColors.FAIL, BgColors.ENDC))
				return
			# check if the item is equipped
			if item.is_equipped():
				# set the equipped status to false
				item.equip = False
				print("{}You unequiped the {}.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			# if the item is not equipped, then error
			else: 
				print("{}You don't have the {} equipped!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))		