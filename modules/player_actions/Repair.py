#!/usr/local/bin/python3

import textwrap

from modules.bgcolors import BgColors
from modules import items
from modules import armor
from modules import weapons


class aRepair(object):
	
	@classmethod
	def __act__(cls, vendor, **kwargs):
		player = kwargs['player']
		item = kwargs['item']
	
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item :
			# attempt to find the item the user wants to interact with in the container/room
			item = player.select_item(item, player.inventory)
		# if the user did not pass an item to interact with, then...
		else:
			# print an error message stating an item reference must be passed
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return		
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the vendor variable from the passed vendor found within the tile object
			vendor = vendor[0]
			# set the correct item variable for interactions
			item = item[0]
			# ensure we are attempting to repair a weapon or armor, nothing else can be repaired, as nothing else in the game gets damaged
			if isinstance(item, weapons.Weapon) or isinstance(item, armor.Armor):
				if item.hp == item.orig_hp :
					print("{}This item does not need repair. HP:{}/{}{}".format(BgColors.FAIL, item.hp, item.orig_hp, BgColors.ENDC))
				# using the vendor method can_repair, we check to see if the level of item being requested to repair is acceptable by the vendor (vendor level >= item level)
				elif not vendor.can_repair(item) :
					print( textwrap.fill("{}This item can not be repaired at this station. Find a repair station with a higher level. Item Level:{} / Repair Level:{}{}".format(BgColors.FAIL, item.level, vendor.level, BgColors.ENDC),70) )
				else :
					# get the cost of repairing the item in reference
					cost = vendor.repair_cost(item)
					# ensure the player has enough in his wallet to cover the cost of repair
					if player.wallet.value >= cost :
						# repair the item, set the item health back to it's original value
						item.hp = item.orig_hp
						print("{}The {} have been successfully repaired!  HP:{}/{}{}".format(BgColors.OKGREEN, item.name, item.hp, item.orig_hp, BgColors.ENDC))
						# deduct the player wallet to remove the cost of repair
						player.wallet.remove_credits(cost)
					# if the player does not have enough in his wallet to repair the item then error message
					else :
						print("{}You don't have enough credits to repair the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))											
			# error if the user is attempting to repair an item other than armor or weapons
			else :
				print("{}You can't repair the {} because it is not armor or a weapon.{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
		
				