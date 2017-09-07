#!/usr/local/bin/python3

from modules.bgcolors import BgColors

class aHelp(object):

	@classmethod
	def extended_help(cls, **kwargs):
		player = kwargs['player']

		#available_actions = player.room.available_actions(player)
		available_actions = kwargs['actions_list'] #actions.Action.get_actions()
		#actions = __import__('actions')
		print(textwrap.fill("You can use the following commands within the game to interact with the world around you.  Not all actions will be available for use at all times.  The available actions are contextual and will depend on your current status and state in the game, including where you are, what items you possess, and what objects are around you.",70))
		print("")
		for action in available_actions:
			print("{}{}{}".format(BgColors.CADETBLUE, action, BgColors.ENDC))

	@classmethod
	def help(cls, **kwargs):
		"""print the available actions"""		
		print( BgColors.HEADER + "\nChoose an action:" + BgColors.ENDC )
		available_actions = kwargs['available_actions'] #self.room.available_actions(self)
		#actions = __import__('actions')
		for action in available_actions:
			if not isinstance(action, getattr(kwargs['actions'], 'ItemAction')) and not isinstance(action, getattr(kwargs['actions'], 'HiddenAction')):
				print("{}{}{}".format(BgColors.CADETBLUE, action, BgColors.ENDC))
