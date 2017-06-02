#!/usr/local/bin/python3

import sys, random, re, inspect, math, pickle, textwrap, jsonpickle

from modules.bgcolors import BgColors
from modules import actions
from modules import items
from modules import armor
from modules import weapons
from modules import serums
from modules import tiles


class Player:
	hp 						= 100
	victory 				= False
	world					= None
 
	def __init__(self, world):
		self.location_x, self.location_y = (world.start_point[0], world.start_point[1])
		self.prev_location_x = None
		self.prev_location_y = None
		self.world = world
		
		self.wallet	= self.world._objects['Wallet']
			
		self.inventory  = [self.wallet]
		self.journal 	= []
		
		self.backpack	= self.world._objects['SmallBackpack']
		#self.wallet.add_credits(10)
				
		self.skills	= {	'attack':
							{'name':'Attacking'
							 ,'desc':'Ability to land an attack on an enemy.'
							 ,'value':70
							 }
						,'evade':
							{'name':'Evasion'
							 ,'desc':'Ability to evade an enemy attack.'
							 ,'value':10
							 }
						,'loot':
							{'name':'Looting'
							 ,'desc':'Ability to find loot on deceased enemies.'
							 ,'value':20
							 }
						,'wield':
							{'name':'Wielding'
							 ,'desc':'Rate at which wielded weapons resist degradation from usage.'
							 ,'value':70
							 }
						,'block':
							{'name':'Blocking'
							 ,'desc':'Rate at which equipped armor resist degradation from attacks.'
							 ,'value':20
							 }
						}		

	def is_alive(self):
		return self.hp > 0

	def print_inventory(self, item=None):
		print("{}Other available actions:".format(BgColors.HEADER))
		print("{}Usage: action paired with either the item index number or the item full name.\n".format(BgColors.NORMAL))
		available_actions = self.room.available_actions(self)
		for action in available_actions:
			if isinstance(action, getattr(actions, 'ItemAction')):
				print("{}{}{}".format(BgColors.OKBLUE, action, BgColors.ENDC))
		i = 1
		print(BgColors.NORMAL + """
The following is a list of the items you possess in your backpack.  Discover, or buy, 
larger backpacks to carry more items.  The items in the inventory list are categorized 
by equipment type.  Each item has an associated number, name, description, and item statistics.  
You can interact with your inventory items by using one of the available action commands
paired with the item number, or the short name of the item.
		""")
		
		print("{}pink = equipped{}".format(BgColors.HEADER, BgColors.ENDC))
		print("{}red = broken{}".format(BgColors.FAIL, BgColors.ENDC))
		print('')
		
		self.reindex_inventory()


		print("{}Backpack Capacity: %s/%s{}".format(BgColors.NORMAL, BgColors.ENDC) % (self.get_inventory_size(), self.backpack.level))		
				
		print("{}┌{}┐".format(BgColors.NORMAL,"─"*111))
		print("|", "{:<3}|".format('#'), "{:<20}|".format('Name'), "{:<7}|".format('Value'), "{:<5}|".format("HP"), "{:<5}|".format("DEF"), "{:<5}|".format("DMG"), "{:<53}|".format("Description")) #{:<20}
		print("| {} |".format("─"*109))
			
		# print the wallet text
		print("{}| {:<3}|".format(BgColors.HEADER, self.wallet.index), "{:<20}|".format(self.wallet.name), "{:<7}|".format(self.wallet.value), "{:<5}|".format(''), "{:<5}|".format(''), "{:<5}|".format(''), "{:<53}{}|".format(self.wallet.description, BgColors.ENDC)) #{:<20}
		
		if len([x for x in self.inventory if issubclass(x.__class__, items.Usable) and not issubclass(x.__class__, serums.Serum)]) > 0:
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, items.Usable) and not issubclass(item.__class__, serums.Serum):
					color_ = BgColors.HEADER if item.is_equipped() else BgColors.NORMAL
					print("{}| {:<3}|".format(color_,item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<5}|".format(''), "{:<5}|".format(''), "{:<5}|".format(''), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
	
		
		if len([x for x in self.inventory if issubclass(x.__class__, weapons.Weapon)]) > 0:
			print("| {} |".format("─"*109))
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, weapons.Weapon) :
					color_ = BgColors.HEADER if item.is_equipped() and item.hp > 0 else BgColors.FAIL if item.hp <= 0 else BgColors.NORMAL
					print("{}| {:<3}|".format(color_, item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<5}|".format(item.hp), "{:<5}|".format(''), "{:<5}|".format(item.damage), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
					
		if len([x for x in self.inventory if issubclass(x.__class__, armor.Armor)]) > 0:
			print("| {} |".format("─"*109))
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, armor.Armor) :
					color_ = BgColors.HEADER if item.is_equipped() and item.hp > 0 else BgColors.FAIL if item.hp <= 0 else BgColors.NORMAL
					print("{}| {:<3}|".format(color_, item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<5}|".format(item.hp), "{:<5}|".format(item.block), "{:<5}|".format(''), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
									
		if len([x for x in self.inventory if issubclass(x.__class__, serums.Serum)]) > 0:
			print("| {} |".format("─"*109))
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, serums.Serum) :
					print("{}| {:<3}|".format(BgColors.NORMAL, item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<5}|".format(item.hp), "{:<5}|".format(''), "{:<5}|".format(''), "{:<53}{}|".format(item.description if len(item.description) <= 53 else item.description[0:50]+'...', BgColors.ENDC)) #{:<20}
		
									
		print("{}└{}┘".format(BgColors.NORMAL, "─"*111))

		

	def reindex_inventory(self):
		i = 1
		def get_name(b) :
			return b.name
		
		def get_index(b) :
			return b.index 
			
		inv = sorted(self.inventory, key=get_name)
		
		for index, item in enumerate(inv):
			if issubclass(item.__class__, items.Usable) and not issubclass(item.__class__, serums.Serum):
				i += 1
				inv[index].index = i
	
		for index, item in enumerate(inv):
			if issubclass(item.__class__, weapons.Weapon):
				i += 1
				inv[index].index = i
	
		for index, item in enumerate(inv):
			if issubclass(item.__class__, armor.Armor):
				i += 1
				inv[index].index = i
			
		for index, item in enumerate(inv):
			if issubclass(item.__class__, serums.Serum):
				i += 1
				inv[index].index = i


		inv = sorted(inv, key=get_index)
		# override inventory with the newly indexed and sorted inventory list
		self.inventory = inv
	
	
	def print_journal(self, item=None):
		
		i = 1
		print(BgColors.NORMAL + """
The following is a list of the narratives you have read through the realm and possess in 
your journal.  Each narrative has an associated number, name, and narrative summary. The
narrative index is sorted in ascending chronological order by date discovered. You can 
read narratives within your journal with the [read] [#] command.
		""")

		if len([x for x in self.journal if issubclass(x.__class__, items.Readable)]) > 0:
		
			for index, item in enumerate(self.journal):
				if item.index :
					i += 1
				else :
					self.journal[index].index = i
					
					

			print("{}┌{}┐".format(BgColors.NORMAL,"─"*111))
			print("|", "{:<3}|".format('#'), "{:<20}|".format('Name'), "{:<83}|".format("Narrative")) #{:<20}
			print("| {} |".format("─"*109))
	
			for index, item in enumerate(self.journal):
				if issubclass(item.__class__, items.Readable) :
					print("{}| {:<3}|".format(BgColors.NORMAL, item.index), "{:<20}|".format(item.name if len(item.name) <= 20 else item.name[0:17]+'...'), "{:<83}{}|".format(item.narrative if len(item.narrative) <= 83 else item.narrative[0:80]+'...', BgColors.ENDC)) #{:<20}
						
			print("{}└{}┘".format(BgColors.NORMAL, "─"*111))
		
		else :
			print("{}There are no entries in your journal.{}".format(BgColors.FAIL, BgColors.ENDC))
	

	# Now we need to allow the Player class to take an Action and run the action`s internally-bound method. 
	def do_action(self, action, *args, **kwargs):
		action_method = getattr(self, action.method.__name__)
		if action_method:
			action_method(*args, **kwargs)

	def help(self):
		"""print the available actions"""
		print( BgColors.HEADER + "\nChoose an action:" + BgColors.ENDC )
		available_actions = self.room.available_actions(self)
		#actions = __import__('actions')
		for action in available_actions:
			if not isinstance(action, getattr(actions, 'ItemAction')) and not isinstance(action, getattr(actions, 'HiddenAction')):
				print("{}{}{}".format(BgColors.OKBLUE, action, BgColors.ENDC))

	def extended_help(self):
		available_actions = self.room.available_actions(self)
		#actions = __import__('actions')
		print("""
You can use the following commands within the game to interact with
the world around you.  Not all actions will be available for use at
all times.  The available actions are contextual and will depend on 
your current status and state in the game, including where you are, 
what items you possess, and what objects are around you.
			""")
		for action in available_actions:
			print("{}{}{}".format(BgColors.OKBLUE, action, BgColors.ENDC))


	#################################################################################################################################
	# METHODS TO ALLOW THE PLAYER TO MOVE AROUND - THESE ARE PART OF THE PLAYER CLASS
	def select_item(self, ref, container=None):
		try:
			# set item variable
			item = [None]
			# check if the ref code is an integeter, or a character/string
			if ref.isdigit():
				# iterate over every item within the passed container (if container was passed), to find the item with the matching ref
				for i in container:
					# check the index attribute first
					if hasattr(i, 'index'):
						# if the item index attribute matches the passed ref integer, then...
						if i.index == int(ref):
							# return the matched item object in a list format
							return [i] #if i.index == int(ref) else [None]
				
				# if nothing was found matching within the loop, then attempt to get the matching item from the container with the list index matching ref (-1 for zero basing)
				item = [container[int(ref)-1]]
			# if ref is not an integer/digit
			else:
				# find the item name within the container that matches the string ref (lower), after removing all spaces from item name and ref to ensure a straight match
				item = [x for x in container if x.name.upper().replace(' ','') == ref.upper().replace(' ','')]
		except (IndexError, AttributeError):
			# otherwise, item is none and there will be no match
			item = [None]
		# return item to the calling function
		return item

	
	def move(self, dx, dy):
		if not self.has_light():
			print( BgColors.NORMAL + textwrap.fill("It is too dark to see.  You must discover how to light the way before continuing.  Use the [search] command to view items within the room, or the [i] command to view items within your inventory.\n",70) )
		else:
			# set the previous location x,y to the current location x,y before we change rooms/tiles so we know where we were at the last move
			self.prev_location_x = self.location_x
			self.prev_location_y = self.location_y
			# set the new coordinates x and y for moving
			self.location_x += dx
			self.location_y += dy
			
			intro_text = self.world.tile_exists(self.location_x, self.location_y).intro_text()
			if intro_text :
				print(BgColors.NORMAL + "\n" + textwrap.fill( intro_text, 70)  + BgColors.ENDC)
				#print( re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', BgColors.NORMAL + self.world.tile_exists(self.location_x, self.location_y).intro_text().replace(r'\n','\n'), flags=re.M) )
			
			# set the bool for knowing if we have visited this room/tile before
			self.world.tile_exists(self.location_x, self.location_y).visited = True

		
			
	def move_north(self, **kargs):
		self.move(dx=0, dy=-1)
	
	def move_south(self, **kargs):
		self.move(dx=0, dy=1)
	
	def move_east(self, **kargs):
		self.move(dx=1, dy=0)
	
	def move_west(self, **kargs):
		self.move(dx=-1, dy=0)
	
	def check_hp(self, **kargs):
		print("{}Current HP Level: {}{}".format(BgColors.OKGREEN, self.hp, BgColors.ENDC))

	def check_skills(self, **kwargs):
		print("{}Skills:{}".format(BgColors.OKBLUE, BgColors.ENDC))
		for k, v in self.skills.items():
			print("{}{:<10}:{}% - {}{}".format(BgColors.OKGREEN, v['name'], v['value'], v['desc'], BgColors.ENDC))
	
	def check_stats(self, **kwargs):
		print("{}Stats:{}".format(BgColors.OKBLUE, BgColors.ENDC))
		# print the player health
		self.check_hp()
		# compile total sum of armor defense from equipped armor
		print("{}Current Armor Level: {}{}".format(BgColors.OKGREEN, sum([x.block for x in self.inventory if isinstance(x, armor.Armor) and x.is_equipped()]), BgColors.ENDC))
		# compile total sum of weapon damage from equipped weapons
		print("{}Current Damage Level: {}{}".format(BgColors.OKGREEN, sum([x.damage for x in self.inventory if isinstance(x, weapons.Weapon) and x.is_equipped()]), BgColors.ENDC))
		
		# print each item of armor that is equipped
		if len([x for x in self.inventory if isinstance(x, armor.Armor)]) > 0:
			print("\n{}Equipped Armor:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			[print(x) for x in self.inventory if isinstance(x, armor.Armor) and x.is_equipped()]
		
		# print each item of weapons that is equipped
		if len([x for x in self.inventory if isinstance(x, weapons.Weapon)]) > 0:
			print("\n{}Equipped Weapons:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			[print(x) for x in self.inventory if isinstance(x, weapons.Weapon) and x.is_equipped()]

		print("")
		# print the skills stats
		self.check_skills()
		
	
	def get_inventory_size(self):
		# get the full size of your inventory, excluding items that are equipped since those are being worn and not in your backpack
		return len([x for x in self.inventory if hasattr(x, 'equip') and not x.equip or not hasattr(x, 'equip') ])
	
	def increase_health(self, amt):
		# increase the player health by the additional hp amount, or max out at 100
		self.hp = min(100, self.hp+amt)
	
	def has_light(self):
		return any( item for item in self.inventory if item.name == 'Flashlight' and item.is_equipped() )		
		
	def loot(self, enemy):
		# get the objects on the enemy that can be looted and that are not already taken
		#objects = [i for i in enemy.get_items() if not i.is_taken()]
		objects = [i for i in enemy.get_items()]
		# if there are objects to be lootted
		if objects:
			# iterate over the items to be looted
			for item in objects:
				if isinstance(item, items.Money):
					#print("{}You picked up {} {}!{}".format(BgColors.WARNING, item.amt, item.name, BgColors.ENDC))
					print( item )
					# add the gold amount to your wallet
					self.wallet.add_credits(item.cost)
				else:
					print("{}You picked up the {}!{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
				# remove the item from the enemy
				enemy.objects.remove(item)
				# add the item to your player inventory
				#self.inventory.append(item)
				# add the item to the player inventory
				self.inventory.append(item)
				# reindex the player inventory based on our categorization rules
				self.reindex_inventory()

		# set the enemy (passed variable) looted property to true
		enemy.looted = True


	def search(self):
		# search for objects within the room that are not taken
		objects = [i for i in self.room.get_items()]
		# if objects within the room exist, then print them
		if objects:
			print("A quick search around the room and you find the following item(s):\n")
			# iterate over all items within the room that can be interacted with
			[print("{}.{} {}{}".format(index+1, BgColors.WARNING, item, BgColors.ENDC)) for index, item in enumerate(objects)]
		# if there are not items within the room that are interactable
		else:
			print("{}No items available to interact with!{}".format(BgColors.FAIL, BgColors.ENDC))
			
			
	def read(self, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = [i for i in self.select_item(item, self.room.get_items()) if isinstance(i, items.Readable)] or self.select_item(item, self.journal)
		# if the user did not pass an item to interact with, then...
		else:
			# attempt to autmatically get the readaable item from the room, if it exists
			item = [i for i in self.room.get_items() if isinstance(i, items.Readable)]
			#item = [i for i in self.room.get_items() if i.classtype == 'Readable']
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
			if not item.read :
				# add the item to the player inventory
				self.journal.append(item)
			
			# check if the readable item also has a skill that can be incremented, and that it has not already been read (we don't want to re-increment the skill value again if it has been read before)
			if item.skill and item.inc_value and not item.is_read():
				# set the read status to true, so we know if it has been read before
				item.read = True
				# increment the skill by the amount to be incremented
				self.skills[item.skill.lower()]['value'] += item.inc_value
				print("\n{}You gained +{} {} experience!{}".format(BgColors.OKGREEN, item.inc_value, item.skill, BgColors.ENDC))
				

	def pick_up(self, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.room.get_items())
		# if the user did not pass an item to interact with, then...
		else: 
			item = [x for x in self.room.get_items() if issubclass(x.__class__,(items.Lootable,items.Usable))]
			# if there are multiple items within the room that can be picked up, then return error stating the user must define an item to interact with
			if len(item) > 1:
				print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in the room. Use the [search] command to view items within the room.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
				return
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in the room! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return
		# if item is subclass of chest, then provide error message that you can not pick it up
		elif [x for x in [item] if issubclass(x.__class__,items.Container)]:
			print("{}You cannot pick this item up! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		# ensure that we have enough room in our backpack before we can pick up the item
		if self.get_inventory_size()+1 > self.backpack.level:
			# if the backpack does not have enough room, then provide error message back
			print("""
{}You don't have enough room in your backpack items.  
Find a larger backpack or drop items from your inventory.{}"""
.format(BgColors.FAIL, BgColors.ENDC))
			return
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)):
			# set the correct item variable for interactions
			item = item[0] # if not isinstance(item, list) else item[0]
			# set the item's taken status to false
			#item.taken = True
			# remove the item from the room's list of items
			self.room.remove_item(item)
			# reindex the room index list
			self.room.reindex_items()
			# if the item is gold, then add the amount to your wallet
			if isinstance(item, items.Money):
				print( item )
				# add the gold amount to your wallet
				self.wallet.add_credits(item.cost)
			# if the item is an item
			elif isinstance(item, items.Item):
				# print message that the player picked up the message
				print("{}You picked up the {}!{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
				# if the item is an instance of the armor or weapons class, then provide a message about remembering to equip your item
				if isinstance(item,armor.Armor) or isinstance(item,weapons.Weapon):
					print("{}Equip the {} with the [equip] command.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
				else :
					# provide a message about remembering to check your inventory for more stats about the item
					print("{}Check your inventory with the [i] command.{}".format(BgColors.WARNING, BgColors.ENDC))

				# add the item to the player inventory
				self.inventory.append(item)
				# reindex the player inventory based on our categorization rules
				self.reindex_inventory()
				
				
	def drop(self, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.inventory)
		# if the user did not pass an item to interact with, then...
		else:
			# print an error message stating an item reference must be passed
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return  
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		if not list(filter(None.__ne__, item)):
			print("{}That is not a valid item in your inventory!{}".format(BgColors.FAIL, BgColors.ENDC))
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		elif list(filter(None.__ne__, item)) :
			# set the correct item variable for interactions
			item = item[0]
			# if the item is instance of wallet, then provide error that we can't/shouldn't drop the wallet
			if isinstance(item, items.Wallet):
				print("{}You're going to need your wallet...{}".format(BgColors.FAIL, BgColors.ENDC))
				return
			# otherwise, provide message that you dropped the item
			print("{}You dropped the {}.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			# remove the item from inventory
			self.inventory.remove(item)
			# set the item's equipped status to false
			item.equip = False
			# set the item's taken status to false
			#item.taken = False
			# add the item to the room object so it is now part of the room
			self.room.add_item(item)
			# re-index the order of the indexing of the room items for interactions
			self.room.reindex_items()
				
	
	def open(self, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.room.get_items())
		# if the user did not pass an item to interact with, then...
		else:
			# get the items within the room that can be interacted in this way
			item = self.room.get_items()
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
			if not item.opened :
				# set the open status to true
				item.opened = True
				# remove the item from the room
				#self.room.remove_item(item)
				
				# if the item is instance of gold, then get the amount of gold in order to add to wallet
				if isinstance(item, items.Money):
					print("{}You opened the {} and found {} credits!{}".format(BgColors.OKGREEN, item.name, item.cost, BgColors.ENDC))
					# add the gold amount to your wallet
					self.wallet.add_credits(item.cost)
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
						self.journal.append(item.objects[0])
				
				# if the item is anything other than money within the object you opened, then print this
				else :
					print("{}You opened the {} and found {}!{}".format(BgColors.OKGREEN, item.name, item.objects[0].name, BgColors.ENDC))
					# add the item to your inventory
					self.inventory.append(item.objects[0])
					# provide a message about remembering to check your inventory for more stats about the item
					print("{}Check your inventory with the [i] command.{}".format(BgColors.WARNING, BgColors.ENDC))
					
			else :
				print("{}The {} is already opened!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
				
				
	
	def use(self, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.inventory)
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
			room_items = self.room.get_items()
			# get the first item within the room, if there are items within the room
			room_item = room_items[0] if list(filter(None.__ne__, room_items)) else None
			
			# ensure that the item we want to use is usable
			if issubclass(item.__class__, items.Usable):
				# check if the item is a serum
				#print( room_item )
				if issubclass(item.__class__, serums.Serum):
				#if item.classtype == 'serum':
					# if it is a serum, then increase the player health by the hp points of the serum
					self.increase_health( item.hp )
					print("{}You used the {}. Health increased by {}.{}".format(BgColors.OKGREEN, item.name, item.hp, BgColors.ENDC))
					# remove the serum from the inventory, since it is not used and not re-usable
					self.inventory.remove(item)
				
				# check if the used item class matches the desired class of the usable item class specified in the room item details
				# this is for items within the room that have an interaction item, like Gold Chest needing a Key
				#elif list(filter(None.__ne__, self.room.interaction_item)) and item.__class__ == self.room.interaction_item[0].__class__ :
				elif list(filter(None.__ne__, self.room.interaction_item)) and item.__class__ == self.room.interaction_item[0].__class__ and item.name == self.room.interaction_item[0].name:
				#elif list(filter(None.__ne__, self.room.interaction_item)) and item.classtype == self.room.interaction_item[0].classtype :
					# if it matches, then move the barrier item
					self.room.get_items()[0].unblocked = True
					# set the room status to not blocked, since we just moved the object
					self.room.isBlocked = False
					print("{}You used the {} on the {}.{}".format(BgColors.OKGREEN, item.name, self.room.get_items()[0].name, BgColors.ENDC))

				# check if the used item class matches the desired class of the usable item class specified in the room item details 
				# this is for rooms with barrier items that have an interaction item, like a room with rock pile as movable
				elif list(filter(None.__ne__, room_item.interaction_item)) and room_item and hasattr(room_item, 'interaction_item') and item.__class__ == room_item.interaction_item[0].__class__ and item.name == room_item.interaction_item[0].name :				
				#elif room_item and hasattr(room_item, 'interaction_item') and item.classtype == room_item.interaction_item[0].classtype :
					# set the item as moved
					room_item.unblocked = True
					print("{}You used the {} on the {}.{}".format(BgColors.OKGREEN, item.name, room_item.name, BgColors.ENDC))
				# finally, if none of the above conditions are true, then the item must not be usable on the movable item in that way
				else :
					print("{}Using the {} doesn't do anything here.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			# the item is not usable, print an error message
			else:
				print("{}The item you selected is not usable in that way. Select again...{}".format(BgColors.FAIL, BgColors.ENDC))			
	
	
	
	def equip(self, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.inventory)
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
			#if item.classtype == 'Weapon': #item.__class__.__bases__[0] == 'Weapon':
				# check if item health is greater than 0, proving it is not broken and can be equipped
				if item.hp <= 0:
					# print an error message if the item is broken and health is 0
					print("{}You can not equip the {}, it is broken{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
					return
				# else, the item can be equipped
				else :
					# ensure only one weapon is equipped at any time, so iterate through all other weapons and unequip them if they are equipped
					for i in self.inventory:
						if isinstance(i, weapons.Weapon):
						#if item.classtype == 'Weapon':
							i.equip = False
					# set this item equipped status to true
					item.equip = True
					print("{}You equipped the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
			# check if the item is armor, and can be equipped
			elif isinstance(item, armor.Armor) or item.name == 'Flashlight':
			#elif item.baseclass == 'Armor':
				# ensure only one armor item that is the same baseclass (for example boots, or shield) is equipped at one time.  unequip the other armor item of same baseclass if so
				for i in self.inventory:
					if isinstance(i, armor.Armor):
					#if item.baseclass == 'Armor':
						# ensure the same type of armor isn't already equipped (i.e. two boot types, etc.)
						if i.__class__ == item.__class__ and i.is_equipped() :
						#if i.classtype == item.classtype and i.is_equipped():
							i.equip = False
				# set this item equipped status to true
				item.equip = True
				print("{}You equipped the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
			
			# if the item is not armor or weapons, then it can not be equipped, print an error message
			else:
				print("{}You can't equip the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			
	
	def unequip(self, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.inventory)
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
			if isinstance(item, items.Wallet):
			#if item.classtype == 'wallet':
				print("{}You're going to need your wallet...{}".format(BgColors.FAIL, BgColors.ENDC))
				return
			# check if the item is equipped
			if item.is_equipped():
				# set the equipped status to false
				item.equip = False
				print("{}You unequiped the {}.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			# if the item is not equipped, then error
			else: 
				print("{}You don't have the {} equipped!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))			
	
	
	
	
	def repair(self, vendor, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item :
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.inventory)
		# if the user did not pass an item to interact with, then...
		else:
			# print an error message stating an item reference must be passed
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		# check if the initial item find within the container was successful and item is a list with a valid element within the list
		if list(filter(None.__ne__, item)):
			# set the vendor variable from the passed vendor found within the tile object
			vendor = vendor[0]
			# set the correct item variable for interactions
			item = item[0]
			# ensure we are attempting to repair a weapon or armor, nothing else can be repaired, as nothing else in the game gets damaged
			if isinstance(item, weapons.Weapon) or isinstance(item, armor.Armor):
			#if item.classtype == 'Weapon' or item.baseclass == 'Armor':
				if item.hp == item.orig_hp :
					print("{}This item does not need repair. HP:{}/{}{}".format(BgColors.FAIL, item.hp, item.orig_hp, BgColors.ENDC))
				# using the vendor method can_repair, we check to see if the level of item being requested to repair is acceptable by the vendor (vendor level >= item level)
				elif not vendor.can_repair(item) :
					print("{}This item can not be repaired by this vendor. Find a vendor with a higher repair level. Item Level:{}, Vendor Repair Level:{}{}".format(BgColors.FAIL, item.level, vendor.level, BgColors.ENDC))
				else :
					# get the cost of repairing the item in reference
					cost = vendor.repair_cost(item)
					# ask the user if they are sure they want to repair the item given the cost of this repair action
					action_input = input( BgColors.HEADER + 'Would you like to repair the {} for {} credits? [y/n]: '.format(item.name,cost) + BgColors.ENDC).lower()
					print("\n")
					# if the user inputted 'y' for yes
					if action_input.lower() == 'y' :
						# ensure the player has enough in his wallet to cover the cost of repair
						if self.wallet.value >= cost :
							# repair the item, set the item health back to it's original value
							item.hp = item.orig_hp
							print("{}The {} have been successfully repaired to full health!  HP:{}/{}{}".format(BgColors.OKGREEN, item.name, item.hp, item.orig_hp, BgColors.ENDC))
							# deduct the player wallet to remove the cost of repair
							self.wallet.remove_credits(cost)
						# if the player does not have enough in his wallet to repair the item then error message
						else :
							print("{}You don't have enough credits to repair the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))						
					
					# enseure the user selected either a yes or no option, if not, then error
					if action_input.lower() not in ['y','n'] :
						print("{}You must provide a [y/n] answer!{}".format(BgColors.FAIL, BgColors.ENDC))
			# error if the user is attempting to repair an item other than armor or weapons
			else :
				print("{}You can't repair the {} because it is not armor or a weapon.{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
				
					
	def map(self):
		"""Show the map of where the player has been."""
		
		print(textwrap.fill("{}Printing map of where you have been.  Tiles are displayed with x,y coordinates for easy location reference.{}\n".format(BgColors.WARNING, BgColors.ENDC),70))
		
		print("\n{}{} = Current Location".format(BgColors.WARNING, u"\u2588"*2))
		print("{}{} = 1st level".format(BgColors.SKYBLUE, u"\u2588"*2))
		print("{}{} = 2nd level".format(BgColors.CADETBLUE, u"\u2588"*2))
		
		
		# set grid to view.  Grid will present visited tiles/rooms within a x,y range of current location
		# set positive x,y grid ranges in tuple form
		axis_x = 10
		axis_y = 10
		
		normalized_grid_origin = (axis_x/2, axis_y/2)
		
		# create an empty list to hold the tiles where we have been
		buf = []
		# print the grid based on current coordinate view
		for key,tile in self.world.__dict__.items() :
			if isinstance(tile,tiles.MapTile) and tile.is_visited() :
				
				# ensure the x,y axis position is within our range (set above) from center-tile (current location)
				if ( abs( tile.x - self.room.x ) <= normalized_grid_origin[0] ) and ( abs( tile.y - self.room.y ) <= normalized_grid_origin[1] ):
					# if the position logic is true, then add the tile to the buffer list for next iteration set
					buf.append( tile )
				
		buf = sorted(buf, key=lambda b:(b.y, b.x))
		
		line_text = ""
		# iterate over y axis grid range, each line will print a new position tile
		#for y in range(0,axis_y) :
		y_min = int(0 if self.room.y - normalized_grid_origin[1] < 0 else self.room.y - normalized_grid_origin[1])
		y_max =	int(axis_y if self.room.y + normalized_grid_origin[1] < axis_y else self.room.y + normalized_grid_origin[1])
		
		x_min = int(0 if self.room.x - normalized_grid_origin[0] < 0 else self.room.x - normalized_grid_origin[0])
		x_max = int(axis_x if self.room.x + normalized_grid_origin[0] < axis_x else self.room.x + normalized_grid_origin[0])

		for y in range(y_min,y_max) :
			# break to a new line and add the prefixing grid pipe
			#line_text += "\n{:<3}   | ".format(y)
			print("\n{}{}   | ".format(BgColors.NORMAL, y), end='' )
			# # iterate over y axis grid range, each line will print a new position tile
			#for x in range(0,axis_x) :
			for x in range(x_min,x_max) :
				found_x = False
				# iterate over the tiles in buf to get the x and y coordinate, to see if something exists on the x,y coordinate plane we are on currently
				for tile in buf :
					# if the tile x position matches the current iterated x range, and the y position matches the current iterated y range, then provide a square
					if tile.x == x and tile.y == y :
						found_x = True
						color_ = None
						if tile.floor == 1 :
							color_ = BgColors.SKYBLUE
						elif tile.floor == 2 :
							color_ = BgColors.CADETBLUE
						elif tile.floor == 3 :
							color_ = BgColors.WARNING
						else :
							color_ = BgColors.FAIL
						
						#line_text += "{} ".format(u"\u2588"*2) if tile.x == self.room.x and tile.y == self.room.y else "{} ".format(u"\u2591"*2)
						s = "{}{} ".format(BgColors.WARNING, u"\u2588"*2) if tile.x == self.room.x and tile.y == self.room.y else "{}{} ".format(color_, u"\u2588"*2)
						#s = "{}{} ".format(color_, "  ") if tile.x == self.room.x and tile.y == self.room.y else "{}{} ".format(BgColors.NORMAL, "  ")
						print(s, end='')
					
				# if we didn't find an x coordinate tile during our x axis loop, then provide empty spaces
				if not found_x :
					#line_text += "   "
					print("   ", end='' )

		#print( line_text )
		print('')
		
		# print bottom x axis grid
		print("      {}{}".format(BgColors.NORMAL, "―― "*axis_x)) # 2 underscores = 2 x axis spaces per tile
		# print the x coordinate integers
		x_axis_int = ''
		print( '    ',''.join([x_axis_int + " {}{} ".format(BgColors.NORMAL, x) for x in range(x_min,x_max)]) )
		
		
			
		

#################################################################################################################################
# SETUP THE ACTIONABLE ACTIONS FOR INTERACTING WITH A MERCHANT 

	def buy(self, merchant, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, merchant[0].inventory)
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
			if not isinstance(item, items.Backpack) and self.get_inventory_size()+1 > self.backpack.level:
			#if not item.classtype == 'Backpack' and self.get_inventory_size()+1 > self.backpack.level:
				print("""
{}You don't have enough room in your backpack items.  
Find a larger backpack or drop items from your inventory.{}""".format(BgColors.FAIL, BgColors.ENDC))

			# check to see if the player has enough money to purchase the item
			elif item.cost > self.wallet.value :
				# print error message stating there is not enough money to purchase item
				print("{}You don't have enough in your wallet to purchase the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			# otherwise, there is enough money, and there is enough room in the backpack to purchase, so...
			else:
				print("{}You bought the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
				# remove the cost of the item from the wallet			
				self.wallet.remove_credits(item.cost)
				# print a conditional message notifying the user that they should equip the item if it is of type weapon or armor
				if isinstance(item,armor.Armor) or isinstance(item,weapons.Weapon):
					print("{}Equip the {} with the [equip] command.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
				# if you bought a backpack, then set the backpack object of player to the new backpack
				if isinstance(item, items.Backpack):
				#if item.classtype == 'Backpack' :
					self.backpack = item			
				else:
					# otherwise, append the inventory item to the player's inventory
					self.inventory.append(item)
				# remove the item from the merchant's inventory
				merchant[0].inventory.remove(item)
	
	
	def sell(self, merchant, item=None):
		# check if an item has been passed to the method. This function does not work without an item to interact with
		if item:
			# attempt to find the item the user wants to interact with in the container/room
			item = self.select_item(item, self.inventory)
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
				self.inventory.remove(item)
				# append the item to the merchant's inventory
				merchant[0].inventory.append(item)
				# add the item cost in credits to the player's wallet to get paid for the item
				self.wallet.add_credits(item.cost)
		# apparently the item selected is not a valid item in the merchant's inventory...
		else:
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
    
    
	def list(self, merchant):
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

	
	
	
#################################################################################################################################
# SETUP THE ATTACH METHOD FOR THE PLAYER TO ATTACH ENEMIES
	def attack(self, enemy):
		# get the weapon that is equipped from the player's inventory
		weapon = [item for item in self.inventory if isinstance(item, weapons.Weapon) and item.is_equipped()]
		
		# check if the initial weapon find within the container was successful and weapon is a list with a valid element within the list
		if list(filter(None.__ne__, weapon)):
			# set the correct weapon variable for interactions
			weapon = weapon[0]
			# give a percentage chance of hitting the enemy with an attack based on the skill attach value
			if random.random() <= (self.skills['attack']['value']/100): 
				print("{}You use the {} against {} for {} HP!{}\n".format(BgColors.WARNING, weapon.name, enemy.name, weapon.damage, BgColors.ENDC))
				# new enemy hp = the original enemy hp minus whatever the weapon damage does, or 0 is as low as the enemy health will go
				enemy.hp = max(enemy.hp-weapon.damage,0)
				# decrease the hp of the weapon after each use based on the wield skill value
				# 1. take wield skill and divide by 100 to get a decimal. 70/100 = .70
				# 2. take the decimal and subtract 1 to inverse the number so we only degrade by the opposite of 'avoid degradation' skill. 1-.70 = .30
				# 3. take this inversion (.30) and multiply by the weapon's original health.  .30*40 = 12
				# 4. take this new number (12) and subtract from current weapon health.  40-12 = 28
				# 5. get the max between new health number and 0 to prevent negative numbers. max(28,0) = 28
				weapon.hp = max(weapon.hp - math.floor(weapon.orig_hp * (1-(self.skills['wield']['value']/100))), 0)
				# if new weapon health is less than or equal to 0, then the weapon is now broken
				if weapon.hp <= 0:
					# unequip the weapon automatically
					weapon.equip = False
					# print warning to player that weapon is broken and a new weapon must be equipped
					print("{}The {} has broken! You must equip a different weapon!{}".format(BgColors.FAIL, weapon.name, BgColors.ENDC))
				# if the enemy is dead after your attack, then print a successfully killed message
				if not enemy.is_alive():
					print("{}You killed the {}!{}\n".format(BgColors.OKGREEN, enemy.name, BgColors.ENDC))
					print("Check your HP with the hp command!")
			# if the random number is outside of the attack skill percentage, then you missed
			else:
				print("{}You missed!{}\n".format(BgColors.WARNING, BgColors.ENDC))
		# if you attack without a weapon equipped, then print error
		else:
			print("{}You don't have a weapon equipped!{}\n".format(BgColors.FAIL, BgColors.ENDC))
	
	def flee(self, tile):
		"""Moves the player randomly to an adjacent tile"""
		# if last location x is greater than current location x, then we must have moved west to get here, move east would be reverse
		if tile.x < self.prev_location_x :
			a = actions.MoveEast()
		# if last location x is less than current location x, then we must hav emoved east to get here, move west would be reverse
		if tile.x > self.prev_location_x :
			a = actions.MoveWest()
		# if last location y is greater than current location y, then we must of have moved north to get here, move south would be reverse
		if tile.y < self.prev_location_y :
			a = actions.MoveSouth()
		# if last location y is less than current location y, then we must have moved south to get here, move north would be reverse
		if tile.y > self.prev_location_y :
			a = actions.MoveNorth()		
		
		print ("{}You fled to the {}! This is the way you came from.{}".format(BgColors.WARNING, a.name.split(' ')[1], BgColors.ENDC ))
		# call the do_action method to actually perform the move
		self.do_action( a )
		
		
		
#################################################################################################################################
# SETUP WAYS TO LEAVE THE GAME
		
	def exit(self):
		"""Exit the game rooms to win."""
		# set victory variable within the player object to true, for the next while iteration within Game.py to detect victory
		self.victory = True
		# print exit text
		print( textwrap.fill("Being lost in this cavern was terrible. but as you emerge, you find yourself on a mountain ridge, overlooking a lively city in the distance.  It's over.  You are safe.\n\n Thank you for playing.\n\n",70))
				
	
	def save(self):
		"""Save the current state of the game."""
		try :
			# open the file to use for saving the game state, as writable
			with open('res/gsave.pkl', 'w') as output:
				# write the output of jsonpickling the Player object to the file
				output.write( jsonpickle.encode(self) )
			# print successful game save message
			print("{}Game state successfully saved.{}".format(BgColors.OKGREEN, BgColors.ENDC))
		except Exception:
			# if there was an error saving the game, then provide an error message
			print("{}There was an error saving the game.  Sorry.{}".format(BgColors.FAIL, BgColors.ENDC))
	
	
	def quit(self):
		"""Quick the current game, and save."""
		self.save()
		sys.exit()


