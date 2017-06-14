#!/usr/local/bin/python3

from modules.bgcolors import BgColors
from modules import items
from modules.player_actions.Inventory import aInventory


class aLoot(object):
	
	@classmethod
	def __act__(cls, enemy, **kwargs):
		player = kwargs['player']
	
		# get the objects on the enemy that can be looted and that are not already taken
		objects = [i for i in enemy.get_items()]
		# if there are objects to be lootted
		if objects:
			# iterate over the items to be looted
			for item in objects:
				if isinstance(item, items.Money):
					#print("{}You picked up {} {}!{}".format(BgColors.WARNING, item.amt, item.name, BgColors.ENDC))
					print( item )
					# add the gold amount to your wallet
					player.wallet.add_credits(item.cost)
				else:
					print("{}You picked up the {}!{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
				# remove the item from the enemy
				enemy.objects.remove(item)
				# add the item to your player inventory
				player.inventory.append(item)
				# reindex the player inventory based on our categorization rules
				#player.reindex_inventory()
				aInventory.reindex_inventory(player)

		# set the enemy (passed variable) looted property to true
		enemy.looted = True
