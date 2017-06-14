#!/usr/local/bin/python3

import textwrap
from modules.bgcolors import BgColors
from modules import items
from modules.player_actions.Inventory import aInventory

class aDrop(object):
	
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
			print("{}That is not a valid item in your inventory!{}".format(BgColors.FAIL, BgColors.ENDC))
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)) :
			# set the correct item variable for interactions
			item = item[0]
			# if the item is instance of wallet, then provide error that we can't/shouldn't drop the wallet
			if isinstance(item, items.Wallet):
				print("{}You're going to need your wallet...{}".format(BgColors.FAIL, BgColors.ENDC))
				return
			
			article = 'an' if item.name[:1].lower() in ['a','e','i','o','u'] else 'the' if item.name[-1:].lower() == 's' else 'a'
			# otherwise, provide message that you dropped the item
			print("{}You dropped {} {}.{}".format(BgColors.WARNING, article, item.name, BgColors.ENDC))
			# remove the item from inventory
			player.inventory.remove(item)
			# set the item's equipped status to false
			item.equip = False
			# add the item to the room object so it is now part of the room
			player.room.add_item(item)
			# re-index the order of the indexing of the room items for interactions
			#player.room.reindex_items()
			aInventory.reindex_inventory(player)