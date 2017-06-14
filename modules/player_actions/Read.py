#!/usr/local/bin/python3

import textwrap, re

from modules.bgcolors import BgColors
from modules import items

class aRead(object):
	
	@classmethod
	def __act__(cls, item=None, **kwargs):
		player = kwargs['player']
	
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = [i for i in player.select_item(item, player.room.get_items()) if isinstance(i, items.Readable)] or player.select_item(item, player.journal)
		# if the user did not pass an item to interact with, then...
		else:
			# attempt to autmatically get the readaable item from the room, if it exists
			item = [i for i in player.room.get_items() if isinstance(i, items.Readable)]
			#item = [i for i in player.room.get_items() if i.classtype == 'Readable']
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in the room! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0]
			# print the name of the narrative
			print(item.name + "\n")
			# print the narrative text
			print( textwrap.fill("{}".format(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', item.narrative, flags=re.M)),70) )
			# add the narrative to inventory if not already present
			#if not item.read :
			if item not in player.journal :
				# add the item to the player inventory
				player.journal.append(item)
			# check if the readable item also has a skill that can be incremented, and that it has not already been read (we don't want to re-increment the skill value again if it has been read before)
			if item.skill and item.inc_value and not item.is_read():
				# set the read status to true, so we know if it has been read before
				item.read = True
				# increment the skill by the amount to be incremented
				player.skills[item.skill.lower()]['value'] += item.inc_value
				print("\n{}You gained +{} {} experience!{}".format(BgColors.OKGREEN, item.inc_value, item.skill, BgColors.ENDC))
