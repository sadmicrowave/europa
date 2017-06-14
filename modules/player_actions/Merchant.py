#!/usr/local/bin/python3

import textwrap
from modules.bgcolors import BgColors
from modules import items
from modules import armor
from modules import weapons
from modules.player_actions.Inventory import aInventory


#################################################################################################################################
# SETUP THE ACTIONABLE ACTIONS FOR INTERACTING WITH A MERCHANT 

class Merchant(object):
	
	@classmethod
	def buy(cls, merchant, item=None, **kwargs):
		player = kwargs['player']
		
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = player.select_item(item, merchant[0].inventory)
		# if the user did not pass an item to interact with, then...
		else:
			# print an error message stating an item reference must be passed
			print( textwrap.fill("{}You must specify a value with an action! It looks like there are multiple items in the merchant's inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		if not list(filter(None.__ne__, item)):
			# print error stating the item selected is not a valid item within the container 
			print( "{}That is not an item in the merchant's inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC) )
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0] #if len(item) > 0 else None
			# check if there is enough room in the backpack to attempt to buy something else
			if not isinstance(item, items.Backpack) and player.get_inventory_size()+1 > player.backpack.level:
				print("""
{}You don't have enough room in your backpack items.  
Find a larger backpack or drop items from your inventory.{}""".format(BgColors.FAIL, BgColors.ENDC))

			# check to see if the player has enough money to purchase the item
			elif item.cost > player.wallet.value :
				# print error message stating there is not enough money to purchase item
				print("{}You don't have enough in your wallet to purchase the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			# otherwise, there is enough money, and there is enough room in the backpack to purchase, so...
			else:
				print("{}You bought the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
				# remove the cost of the item from the wallet			
				player.wallet.remove_credits(item.cost)
				# print a conditional message notifying the user that they should equip the item if it is of type weapon or armor
				if isinstance(item,armor.Armor) or isinstance(item,weapons.Weapon):
					print("{}Equip the {} with the [equip] command.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
				# if you bought a backpack, then set the backpack object of player to the new backpack
				if isinstance(item, items.Backpack):
					player.backpack = item			
				else:
					# otherwise, append the inventory item to the player's inventory
					player.inventory.append(item)
					aInventory.reindex_inventory(player)
				# remove the item from the merchant's inventory
				merchant[0].inventory.remove(item)
	
	@classmethod
	def sell(cls, merchant, item=None, **kwargs):
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
		if list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0]
			# if the item hp is 0, meaning the item is broken
			if item.hp <= 0 and not isinstance(item, items.Usable):
				# print error message stating the item can't be sold because it's broken
				print("{}You can not sell the {}, it is broken{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			# if the item is your wallet, then...
			elif isinstance(item, items.Wallet):
				# print an error message stating you can't/shouldn't sell your wallet
				print("{}You're going to need your gold wallet...{}".format(BgColors.FAIL, BgColors.ENDC))
			# if there is no cost associated with the item, then it can't be sold for anything
			elif item.cost == 0:
				# print error message stating you can't sell that item
				print("{}There is no defined value for {}, you can't sell it!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			# else, allow the player to sell the item
			else:
				print("{}You sold the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
				# remove the item from the player's inventory
				player.inventory.remove(item)
				# append the item to the merchant's inventory
				merchant[0].inventory.append(item)
				
				cls.reindex_inventory(merchant[0])
				# add the item cost in credits to the player's wallet to get paid for the item
				player.wallet.add_credits(item.cost)
		# apparently the item selected is not a valid item in the merchant's inventory...
		else:
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
	
	
	@classmethod
	def list(cls, merchant, **kwargs):
		player = kwargs['player']
		
		cls.reindex_inventory(merchant)
		
		print("""Hey there, take a look at my spectacular selection of items for sale.  You
won't find better deals anywhere else in the realm!
""")
		
		# print the box headers and frame
		print("┌{}┐".format("─"*111))
		print("|", "{:<3}|".format('#'), "{:<20}|".format('Name'), "{:<7}|".format('Value'), "{:<5}|".format("HP"), "{:<5}|".format("DEF"), "{:<5}|".format("DMG"), "{:<53}|".format("Description")) #{:<20}
		print("|{}|".format("─"*111))

		for index,item in enumerate(merchant[0].inventory):			
			# First, get the HP of the item if it exists
			try :
				hp = item.kwargs['hp'] 
			except KeyError:
				try :
					hp = item.hp
				except AttributeError:
					hp = ''
			
			try :
				defense = item.block
			except AttributeError:
				defense = ''
				
			# Next, get the damage points of an item, if exists
			try :
				damage = item.damage
			except AttributeError:
				damage = ''
			
			print("|", "{:<3}|".format(index+1), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<5}|".format(hp), "{:<5}|".format(defense), "{:<5}|".format(damage), "{}{:<53}{}|".format(BgColors.WARNING, item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}

		# print the box footer
		print("└{}┘".format("─"*111))
		
	
	
	
	@classmethod
	def reindex_inventory(cls, merchant=None):
		i = 1
		def get_name(b) :
			return b.name
		
		def get_index(b) :
			return b.index 
			
		inv = sorted(merchant.inventory, key=get_name)
		
		# provide index numbers, and sort, usable items first
		for index, item in enumerate(inv):
			if issubclass(item.__class__, items.Usable) and not issubclass(item.__class__, serums.Serum):
				i += 1
				inv[index].index = i
	
		# provide index numbers, and sort, weapons next
		for index, item in enumerate(inv):
			if issubclass(item.__class__, weapons.Weapon):
				i += 1
				inv[index].index = i
		
		# provide index numbers, and sort, armor next
		for index, item in enumerate(inv):
			if issubclass(item.__class__, armor.Armor):
				i += 1
				inv[index].index = i
		
		# provide index numbers, and sort, serums next
		for index, item in enumerate(inv):
			if issubclass(item.__class__, serums.Serum):
				i += 1
				inv[index].index = i

		inv = sorted(inv, key=get_index)
		# override inventory with the newly indexed and sorted inventory list
		merchant.inventory = inv
