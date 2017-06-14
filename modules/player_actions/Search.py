#!/usr/local/bin/python3

from modules.bgcolors import BgColors

class aSearch(object):
	
	@classmethod
	def __act__(cls, **kwargs):
		# search for objects within the room that are not taken
		player = kwargs['player']
		
		objects = [i for i in player.room.get_items()]
		# if objects within the room exist, then print them
		if objects:
			print("A quick search around the room and you find the following item(s):\n")
			# iterate over all items within the room that can be interacted with
			[print("{}.{} {}{}".format(index+1, BgColors.WARNING, item, BgColors.ENDC)) for index, item in enumerate(objects)]
		# if there are not items within the room that are interactable
		else:
			print("{}No items available to interact with!{}".format(BgColors.FAIL, BgColors.ENDC))
