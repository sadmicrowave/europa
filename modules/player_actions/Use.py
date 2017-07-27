#!/usr/local/bin/python3

import textwrap

from modules.bgcolors import BgColors
from modules import items
from modules import armor
from modules import weapons
from modules import serums
from modules.helpers.health import Health

class aUse(object):
	
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
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0]
			# get a list of all items within the room
			room_items = player.room.get_items()
			# get the first item within the room, if there are items within the room
			room_item = room_items[0] if list(filter(None.__ne__, room_items)) else None
			
			# ensure that the item we want to use is usable
			if issubclass(item.__class__, items.Usable):
				# check if the item is a keypad type
				if issubclass(item.__class__, items.Keypad):
					if 'code' not in kwargs:
						print( textwrap.fill("{}A keycode must be specified when using this item.  Use the [use] [#] [code] command with this inventory item type.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
					elif 'code' in kwargs and room_item and hasattr(room_item, 'interaction_item') and list(filter(None.__ne__, player.room.interaction_item)) and item.__class__ == player.room.interaction_item[0].__class__ and  hasattr(room_item, 'code'):  #item.__class__ == room_item.interaction_item[0].__class__ and item.name == room_item.interaction_item[0].name :							
						if room_item.key_match(kwargs['code']) :
							room_item.unblocked = True
							player.room.isBlocked = False
							print("{}You used the {} on the {}.{}".format(BgColors.OKGREEN, item.name, room_item.name, BgColors.ENDC))
						else :
							print("{}The code: {} doesn't do anything here.{}".format(BgColors.WARNING, kwargs['code'], BgColors.ENDC))
					else :
						print("{}The code: {} doesn't do anything here.{}".format(BgColors.WARNING, kwargs['code'], BgColors.ENDC))

				# check if the item is a serum
				elif issubclass(item.__class__, serums.Serum):
					# if it is a serum, then increase the player health by the hp points of the serum
					#player.increase_health( item.hp )
					Health.increase_health(player, item.hp)
					print("{}You used the {}. Health increased by {}.{}".format(BgColors.OKGREEN, item.name, item.hp, BgColors.ENDC))
					# remove the serum from the inventory, since it is not used and not re-usable
					player.inventory.remove(item)
				
				# check if the used item class matches the desired class of the usable item class specified in the room item details
				# this is for items within the room that have an interaction item, like Gold Chest needing a Key
				#elif list(filter(None.__ne__, player.room.interaction_item)) and item.__class__ == player.room.interaction_item[0].__class__ and item.name == player.room.interaction_item[0].name:
				elif list(filter(None.__ne__, player.room.interaction_item)) and item.__class__ in [x.__class__ for x in player.room.interaction_item] and item.name in [x.name for x in player.room.interaction_item]:

					# if it matches, then move the barrier item
					player.room.get_items()[0].unblocked = True
					# set the room status to not blocked, since we just moved the object
					player.room.isBlocked = False
					article = 'an' if item.name[:1].lower() in ['a','e','i','o','u'] else 'the' if item.name[-1:].lower() == 's' else 'a'
					print("{}You used {} {} on the {}.{}".format(BgColors.OKGREEN, article, item.name, player.room.get_items()[0].name, BgColors.ENDC))

				# check if the used item class matches the desired class of the usable item class specified in the room item details 
				# this is for rooms with barrier items that have an interaction item, like a room with rock pile as movable
				#elif room_item and hasattr(room_item, 'interaction_item') and list(filter(None.__ne__, room_item.interaction_item)) and item.__class__ == room_item.interaction_item[0].__class__ and item.name == room_item.interaction_item[0].name :				
				elif room_item and hasattr(room_item, 'interaction_item') and list(filter(None.__ne__, room_item.interaction_item)) and item.__class__ in [x.__class__ for x in room_item.interaction_item] and item.name in [x.name for x in room_item.interaction_item] :				

				#elif room_item and hasattr(room_item, 'interaction_item') and item.classtype == room_item.interaction_item[0].classtype :
					# set the item as moved
					room_item.unblocked = True
					article = 'an' if item.name[:1].lower() in ['a','e','i','o','u'] else 'the' if item.name[-1:].lower() == 's' else 'a'
					print("{}You used {} {} on the {}.{}".format(BgColors.OKGREEN, article, item.name, room_item.name, BgColors.ENDC))
				# finally, if none of the above conditions are true, then the item must not be usable on the movable item in that way
				else :
					print("{}Using the {} doesn't do anything here.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			# the item is not usable, print an error message
			else:
				print("{}The item you selected is not usable in that way. Select again...{}".format(BgColors.FAIL, BgColors.ENDC))			
	
