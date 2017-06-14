#!/usr/local/bin/python3

import textwrap
from modules.bgcolors import BgColors
from modules import items
from modules import armor
from modules import weapons

class aEquip(object):
	
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
			# check if the item is already equipped, provide error message if so
			if item.is_equipped():
				print("{}The {} is already equipped!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
				return
			# check if item is a weapon, and can be equipped
			if isinstance(item, weapons.Weapon): #item.__class__.__bases__[0] == 'Weapon':
				# check if item health is greater than 0, proving it is not broken and can be equipped
				if item.hp <= 0:
					# print an error message if the item is broken and health is 0
					print("{}You can not equip {}, it is broken{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
					return
				# else, the item can be equipped
				else :
					# ensure only one weapon is equipped at any time, so iterate through all other weapons and unequip them if they are equipped
					for i in player.inventory:
						if isinstance(i, weapons.Weapon):
						#if item.classtype == 'Weapon':
							i.equip = False
					# set this item equipped status to true
					item.equip = True
					print("{}You equipped the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
			# check if the item is armor, and can be equipped
			elif isinstance(item, armor.Armor) or item.name == 'Flashlight':
				# ensure only one armor item that is the same baseclass (for example boots, or shield) is equipped at one time.  unequip the other armor item of same baseclass if so
				for i in player.inventory:
					if isinstance(i, armor.Armor):
						# ensure the same type of armor isn't already equipped (i.e. two boot types, etc.)
						if i.__class__ == item.__class__ and i.is_equipped() :
							i.equip = False
				# set this item equipped status to true
				item.equip = True
				print("{}You equipped the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
			
			# if the item is not armor or weapons, then it can not be equipped, print an error message
			else:
				print("{}You can't equip the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			
