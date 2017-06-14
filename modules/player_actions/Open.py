#!/usr/local/bin/python3

import textwrap, re
from modules.bgcolors import BgColors
from modules import items
from modules import armor
from modules import weapons

class aOpen(object):
	
	@classmethod
	def __act__(cls, item=None, **kwargs):
		player = kwargs['player']
	
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = player.select_item(item, player.room.get_items())
		# if the user did not pass an item to interact with, then...
		else:
			# get the items within the room that can be interacted in this way
			item = player.room.get_items()
		# if there are multiple "open-able" items within the room, then...
		if len([x for x in [item] if isinstance(x,items.Container)]) > 1: #issubclass(x.__class__,items.Chest)]) > 1:
			# provide error message stating user must select an item to interact with
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in the room. Use the [search] command to view items within the room.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
		# if the items within the room are not open-able, but the user wants to try an open it, then...
		elif len([x for x in [item] if not isinstance(x,items.Container)]) > 1 : #issubclass(x.__class__,items.Chest)]:
			# provide an error message stating you canot do that
			print("{}You cannot open this item! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif not list(filter(None.__ne__, item)):
			print("{}That is not a valid item in the area! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0]
			# set the item taken status to true so we know we can't take it again
			if hasattr(item, 'opened') and not item.opened :
				# set the open status to true
				item.opened = True
				# if the item is instance of gold, then get the amount of gold in order to add to wallet
				if isinstance(item, items.Money):
					print("{}You opened the {} and found {} credits!{}".format(BgColors.OKGREEN, item.name, item.cost, BgColors.ENDC))
					# add the gold amount to your wallet
					player.wallet.add_credits(item.cost)
					# set cost to 0 so it can't be unintentionally opened again and added to wallet somehow
					item.cost = 0
				
				# if the item is a readable item, and you opened the terminal or enclosure in order to read it, then print note to screen
				elif isinstance(item.objects[0], items.Readable):
					# print the name of the narrative
					print(item.objects[0].name + "\n")
					# print the narrative text
					print( textwrap.fill("{}".format(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', item.objects[0].narrative, flags=re.M)),70) )
					
					# add the narrative to inventory if not already present
					if not item.objects[0].read :
						# add the item to the player inventory
						player.journal.append(item.objects[0])
				
				# if the item is anything other than money within the object you opened, then print this
				else :
					item_article = 'an' if item.name[:1].lower() in ['a','e','i','o','u'] else 'the' if item.name[-1:].lower() == 's' else 'a'
					obj_article = 'an' if item.objects[0].name[:1].lower() in ['a','e','i','o','u'] else 'the' if item.objects[0].name[-1:].lower() == 's' else 'a'

					print("{}You opened {} {} and found {} {}!{}".format(BgColors.OKGREEN, item_article, item.name, obj_article, item.objects[0].name, BgColors.ENDC))
					# add the item to your inventory
					player.inventory.append(item.objects[0])
					if isinstance(item.objects[0],armor.Armor) or isinstance(item.objects[0],weapons.Weapon):
						print("{}Equip the {} with the [equip] [#] command.{}".format(BgColors.WARNING, item.objects[0].name, BgColors.ENDC))
					else :
						# provide a message about remembering to check your inventory for more stats about the item
						print("{}Check your inventory with the [i] command.{}".format(BgColors.WARNING, BgColors.ENDC))
			
			elif not hasattr(item, 'opened') :
				print("{}You can't open the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
					
			else :
				print("{}The {} is already opened!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
				
				
