#!/usr/local/bin/python3

import textwrap

from modules.bgcolors import BgColors
from modules import items
from modules import armor
from modules import weapons
from modules.player_actions.Inventory import aInventory


class aPickUp (object):	
	
	@classmethod
	def __act__(cls, item=None, **kwargs):
		player = kwargs['player']
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = player.select_item(item, player.room.get_items())
		# if the user did not pass an item to interact with, then...
		else: 
			item = [x for x in player.room.get_items() if issubclass(x.__class__,(items.Lootable,items.Usable))]
			# if there are multiple items within the room that can be picked up, then return error stating the user must define an item to interact with
			if len(item) > 1:
				print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items. Use the [search] command to view items in the area.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
				return
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in the room! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return
		# if item is subclass of chest, then provide error message that you can not pick it up
		elif [x for x in [item] if issubclass(x.__class__,items.Container)]:
			print("{}You cannot pick this item up! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0] # if not isinstance(item, list) else item[0]
			if isinstance(item, items.Readable):
				print( textwrap.fill("{}You can't pickup a readable item. Use the [read] command to view the contents of this item.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
				return
			if isinstance(item, items.Backpack) :
				if item.level < player.backpack.level :
					print("{}Your current backpack size is larger than this one.  Don't downsize.{}".format(BgColors.WARNING, BgColors.ENDC))
				else :
					player.backpack = item
		
			# ensure that we have enough room in our backpack before we can pick up the item
			if player.get_inventory_size()+1 > player.backpack.level:
				# if the backpack does not have enough room, then provide error message back
				print( textwrap.fill("{}You don't have enough room in your backpack items. Find a larger backpack or drop items from your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
				return
			# remove the item from the room's list of items
			player.room.remove_item(item)
			# reindex the room index list
			player.room.reindex_items()
			# if the item is gold, then add the amount to your wallet
			if isinstance(item, items.Money):
				print( item )
				# add the gold amount to your wallet
				player.wallet.add_credits(item.cost)
			# if the item is an item
			elif isinstance(item, items.Item):
				article = 'an' if item.name[:1].lower() in ['a','e','i','o','u'] else 'the' if item.name[-1:].lower() == 's' else 'a'
				# print message that the player picked up the message
				print("{}You picked up {} {}!{}".format(BgColors.OKGREEN, article, item.name, BgColors.ENDC))
				# if the item is an instance of the armor or weapons class, then provide a message about remembering to equip your item
				if isinstance(item,armor.Armor) or isinstance(item,weapons.Weapon):
					print("{}Equip {} {} with the [equip] [#] command.{}".format(BgColors.WARNING, article, item.name, BgColors.ENDC))
				else :
					# provide a message about remembering to check your inventory for more stats about the item
					print("{}Check your inventory with the [i] command.{}".format(BgColors.WARNING, BgColors.ENDC))

				# add the item to the player inventory
				if not isinstance(item, items.Backpack):
					player.inventory.append(item)
				# reindex the player inventory based on our categorization rules
				#player.reindex_inventory()
				aInventory.reindex_inventory(player)