#!/usr/local/bin/python3

import textwrap

from modules.bgcolors import BgColors
#from modules import actions
from modules import items
from modules import armor
from modules import weapons
from modules import serums


class aInventory(object):
	
	@classmethod
	def __act__(cls, item=None, **kwargs):
		player = kwargs['player']
		
		print("{}Other available actions:".format(BgColors.HEADER))
		print("{}Usage: action paired with either the item index number or the item full name.\n".format(BgColors.NORMAL))
		available_actions = kwargs['available_actions'] #player.room.available_actions(player)
		for action in available_actions:
			if isinstance(action, getattr(kwargs['actions'], 'ItemAction')):
				print("{}{}{}".format(BgColors.CADETBLUE, action, BgColors.ENDC))
		i = 1
		
		print("")
		print( textwrap.fill("{}The following is a list of the items you may have equipped, or that you possess in your backpack. Discover, or buy, larger backpacks to carry more items.  The items in the inventory list are categorized by equipment type.  Each item has an associated number, name, description, and statistics. You can interact with your inventory items by using one of the available action commands paired with the item number, or the short name of the item.{}".format(BgColors.NORMAL, BgColors.ENDC),70) )
		print("")
		print("{}pink = equipped{}".format(BgColors.HEADER, BgColors.ENDC))
		print("{}red = broken{}".format(BgColors.FAIL, BgColors.ENDC))
		print('')
		
		cls.reindex_inventory(player)

		print("{}Backpack Capacity: %s/%s{}".format(BgColors.NORMAL, BgColors.ENDC) % (player.get_inventory_size(), player.backpack.level))		
				
		print("{}┌{}┐".format(BgColors.NORMAL,"─"*111))
		print("|", "{:<3}|".format('#'), "{:<20}|".format('Name'), "{:<7}|".format('Value'), "{:<5}|".format("HP"), "{:<5}|".format("DEF"), "{:<5}|".format("DMG"), "{:<53}|".format("Description")) #{:<20}
		print("{}| {} |{}".format(BgColors.NORMAL, "─"*109, BgColors.ENDC))
			
		# print the wallet text
		print("{}| {:<3}|".format(BgColors.HEADER, player.wallet.index), "{:<20}|".format(player.wallet.name), "{:<7}|".format(player.wallet.value), "{:<5}|".format(''), "{:<5}|".format(''), "{:<5}|".format(''), "{:<53}{}|".format(player.wallet.description, BgColors.ENDC)) #{:<20}
		
		if len([x for x in player.inventory if issubclass(x.__class__, items.Usable) and not issubclass(x.__class__, serums.Serum)]) > 0:
			for index, item in enumerate(player.inventory):
				if issubclass(item.__class__, items.Usable) and not issubclass(item.__class__, serums.Serum):
					color_ = BgColors.HEADER if item.is_equipped() else BgColors.NORMAL
					print("{}| {:<3}|".format(color_,item.index), "{:<20}|".format(item.name if len(item.name) <= 20 else item.name[0:17]+'...'), "{:<7}|".format(item.cost), "{:<5}|".format(''), "{:<5}|".format(''), "{:<5}|".format(''), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
	
		
		if len([x for x in player.inventory if issubclass(x.__class__, weapons.Weapon)]) > 0:
			print("{}| {} |{}".format(BgColors.NORMAL, "─"*109, BgColors.ENDC))
			for index, item in enumerate(player.inventory):
				if issubclass(item.__class__, weapons.Weapon) :
					color_ = BgColors.HEADER if item.is_equipped() and item.hp > 0 else BgColors.FAIL if item.hp <= 0 else BgColors.NORMAL
					print("{}| {:<3}|".format(color_, item.index), "{:<20}|".format(item.name if len(item.name) <= 20 else item.name[0:17]+'...'), "{:<7}|".format(item.cost), "{:<5}|".format(item.hp), "{:<5}|".format(''), "{:<5}|".format(item.damage), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
					
		if len([x for x in player.inventory if issubclass(x.__class__, armor.Armor)]) > 0:
			print("{}| {} |{}".format(BgColors.NORMAL, "─"*109, BgColors.ENDC))
			for index, item in enumerate(player.inventory):
				if issubclass(item.__class__, armor.Armor) :
					color_ = BgColors.HEADER if item.is_equipped() and item.hp > 0 else BgColors.FAIL if item.hp <= 0 else BgColors.NORMAL
					print("{}| {:<3}|".format(color_, item.index), "{:<20}|".format(item.name if len(item.name) <= 20 else item.name[0:17]+'...'), "{:<7}|".format(item.cost), "{:<5}|".format(item.hp), "{:<5}|".format(item.block), "{:<5}|".format(''), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
									
		if len([x for x in player.inventory if issubclass(x.__class__, serums.Serum)]) > 0:
			print("{}| {} |{}".format(BgColors.NORMAL, "─"*109, BgColors.ENDC))
			for index, item in enumerate(player.inventory):
				if issubclass(item.__class__, serums.Serum) :
					print("{}| {:<3}|".format(BgColors.NORMAL, item.index), "{:<20}|".format(item.name if len(item.name) <= 20 else item.name[0:17]+'...'), "{:<7}|".format(item.cost), "{:<5}|".format(item.hp), "{:<5}|".format(''), "{:<5}|".format(''), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
		
									
		print("{}└{}┘".format(BgColors.NORMAL, "─"*111))




	@classmethod
	def reindex_inventory(cls, player=None):
		i = 1
		def get_name(b) :
			return b.name
		
		def get_index(b) :
			return b.index 
			
		inv = sorted(player.inventory, key=get_name)
		
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
		player.inventory = inv
