#!/usr/local/bin/python3

import random, re, inspect, math, pickle, textwrap, jsonpickle

from res.bgcolors import BgColors
from modules import actions
from modules import items
from modules import armor
from modules import weapons
from modules import gold
from modules import potions
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
		
		shield = self.world._objects['WoodenShield']
		shield.equip = True
		boots = self.world._objects['LeatherBoots']
		boots.equip = True
		self.purse	= self.world._objects['Purse']
			
		self.inventory  = [self.purse, boots, self.world._objects['LargeRope'], self.world._objects['SmallKey'] ]		
		
		self.backpack	= self.world._objects['SmallBackpack']
		self.purse.add_coins(10)
				
		self.skills	= {	'attack':
							{'name':'Attacking'
							 ,'desc':'Ability to land an attack on an enemy.'
							 ,'value':30
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
	
# 	def print_inventory(self):
# 		print("\n{}Other available actions:{}\nUsage: action paired with either the item index number or the item full name.\n".format(BgColors.HEADER, BgColors.ENDC))
# 		available_actions = self.room.available_actions(self)
# 		for action in available_actions:
# 			if isinstance(action, getattr(actions, 'ItemAction')):
# 				print("{}{}{}".format(BgColors.OKBLUE, action, BgColors.ENDC))
# 		i = 1
# 		print("""
# The following is a list of the items you possess in your backback.  Discover, or buy, 
# larger backpacks to carry more items.  The items in the inventory list are categorized 
# by equipment type.  Each item has an associated number, name, description, and item statistics.  
# You can interact with your inventory items by using one of the available action commands
# paired with the item number, or the short name of the item.
# 		""")
# 		print("{}Backpack Capacity: %s/%s{}\n".format(BgColors.OKGREEN, BgColors.ENDC) % (self.get_inventory_size(), self.backpack.size))
# 		
# 		print("{}. {}".format(i,self.purse))
# 		
# 		self.reindex_inventory()
# 		
# 		if len([x for x in self.inventory if issubclass(x.__class__, items.Usable) and not issubclass(x.__class__, potions.Potion)]) > 0:
# 			print("\n{}Usables:{}".format(BgColors.OKBLUE, BgColors.ENDC))
# 			for index, item in enumerate(self.inventory):
# 				if issubclass(item.__class__, items.Usable) and not issubclass(item.__class__, potions.Potion):
# 					print("{}. {}".format(item.index,item))
# 		
# 		if len([x for x in self.inventory if issubclass(x.__class__, weapons.Weapon)]) > 0:
# 			print("\n{}Weapons:{}".format(BgColors.OKBLUE, BgColors.ENDC))
# 			for index, item in enumerate(self.inventory):
# 				if issubclass(item.__class__, weapons.Weapon):
# 					print("{}. {}".format(item.index,item))
# 		
# 		if len([x for x in self.inventory if issubclass(x.__class__, armor.Armor)]) > 0:
# 			print("\n{}Armor:{}".format(BgColors.OKBLUE, BgColors.ENDC))
# 			for index, item in enumerate(self.inventory):
# 				if issubclass(item.__class__, armor.Armor):
# 					print("{}. {}".format(item.index,item))
# 				
# 		if len([x for x in self.inventory if issubclass(x.__class__, potions.Potion)]) > 0:
# 			print("\n{}Potions:{}".format(BgColors.OKBLUE, BgColors.ENDC))
# 			for index, item in enumerate(self.inventory):
# 				if issubclass(item.__class__, potions.Potion):
# 					print("{}. {}".format(item.index,item))

	
	def print_inventory(self):
		print("\n{}Other available actions:{}\nUsage: action paired with either the item index number or the item full name.\n".format(BgColors.HEADER, BgColors.ENDC))
		available_actions = self.room.available_actions(self)
		for action in available_actions:
			if isinstance(action, getattr(actions, 'ItemAction')):
				print("{}{}{}".format(BgColors.OKBLUE, action, BgColors.ENDC))
		i = 1
		print("""
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


		print("{}Backpack Capacity: %s/%s{}".format(BgColors.OKGREEN, BgColors.ENDC) % (self.get_inventory_size(), self.backpack.level))		
				
		print("┌{}┐".format("─"*132))
		print("|", "{:<3}|".format('#'), "{}{:<16}|".format('Name',''), "{}{:<7}|".format('Value',''), "{:<6}|".format("HP"), "{} |".format("Defense"), "{} |".format("Damage"), "{:<68}|".format("Description")) #{:<20}
		print("|{}|".format("─"*132))
			
		# print the purse text
		print("|", "{:<3}|".format(self.purse.index), "{:<20}|".format(self.purse.name), "{:<7}|".format(self.purse.value), "{:<6}|".format(''), "{:<8}|".format(''), "{:<7}|".format(''), "{}{:<68}{}|".format(BgColors.WARNING, self.purse.description, BgColors.ENDC)) #{:<20}
		
		if len([x for x in self.inventory if issubclass(x.__class__, items.Usable) and not issubclass(x.__class__, potions.Potion)]) > 0:
		#if len([x for x in self.inventory if x.classtype == 'Usable' and not x.classtype == 'Potion']) > 0:
			#print("\n{}Usables:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, items.Usable) and not issubclass(item.__class__, potions.Potion):
				#if item.classtype == 'Usable' and not item.classtype == 'Potion' :
					#print(item, item.index, item.name, item.cost)
					print("|", "{:<3}|".format(item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<6}|".format(''), "{:<8}|".format(''), "{:<7}|".format(''), "{}{:<68}{}|".format(BgColors.WARNING, item.description, BgColors.ENDC)) #{:<20}
	
		
		if len([x for x in self.inventory if issubclass(x.__class__, weapons.Weapon)]) > 0:
		#if len([x for x in self.inventory if x.classtype == 'Weapon']) > 0:
			print("|{}|".format("─"*132))
			#print("\n{}Weapons:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, weapons.Weapon) :
				#if item.classtype == 'Weapon' :
					color_ = BgColors.HEADER if item.is_equipped() and item.hp > 0 else BgColors.FAIL if item.hp <= 0 else ''
					print("|", "{}{:<3}|".format(color_, item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<6}|".format(item.hp), "{:<8}|".format(''), "{:<7}|".format(item.damage), "{}{:<68}{}|".format(color_ if color_ else BgColors.WARNING, item.description, BgColors.ENDC)) #{:<20}
					
		if len([x for x in self.inventory if issubclass(x.__class__, armor.Armor)]) > 0:
		#if len([x for x in self.inventory if x.baseclass == 'Armor']) > 0:
			print("|{}|".format("─"*132))
			#print("\n{}Armor:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, armor.Armor) :
				#if item.baseclass == 'Armor' :
					color_ = BgColors.HEADER if item.is_equipped() and item.hp > 0 else BgColors.FAIL if item.hp <= 0 else ''
					print("|", "{}{:<3}|".format(color_, item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<6}|".format(item.hp), "{:<8}|".format(item.block), "{:<7}|".format(''), "{}{:<68}{}|".format(color_ if color_ else BgColors.WARNING, item.description, BgColors.ENDC)) #{:<20}
									
		if len([x for x in self.inventory if issubclass(x.__class__, potions.Potion)]) > 0:
		#if len([x for x in self.inventory if x.classtype == 'Potion']) > 0:
			print("|{}|".format("─"*132))
			#print("\n{}Potions:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			for index, item in enumerate(self.inventory):
				if issubclass(item.__class__, potions.Potion) :
				#if item.classtype == 'Potion' :
					print("|", "{:<3}|".format(item.index), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<6}|".format(item.hp), "{:<8}|".format(''), "{:<7}|".format(''), "{}{:<68}{}|".format(BgColors.WARNING, item.description, BgColors.ENDC)) #{:<20}
							
		print("└{}┘".format("─"*132))

		

	def reindex_inventory(self):
		i = 1
		def get_name(b) :
			return b.name
		
		def get_index(b) :
			return b.index 
			
		inv = sorted(self.inventory, key=get_name)
		
		for index, item in enumerate(inv):
			if issubclass(item.__class__, items.Usable) and not issubclass(item.__class__, potions.Potion):
			#if item.classtype == 'Usable' and not item.classtype == 'Potion' :
				i += 1
				inv[index].index = i
	
		for index, item in enumerate(inv):
			if issubclass(item.__class__, weapons.Weapon):
			#if item.classtype == 'Weapon' :
				i += 1
				inv[index].index = i
	
		for index, item in enumerate(inv):
			if issubclass(item.__class__, armor.Armor):
			#if item.baseclass == 'Armor' :
				i += 1
				inv[index].index = i
			
		for index, item in enumerate(inv):
			if issubclass(item.__class__, potions.Potion):
			#if item.classtype == 'Potion' :
				i += 1
				inv[index].index = i


		inv = sorted(inv, key=get_index)
		#for index, item in enumerate(inv):
		#	print( index, item.name )

		# override inventory with the newly indexed and sorted inventory list
		self.inventory = inv
		

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
all times.  The available actions will depend on your current status
and state in the game, including where you are, what items you possess,
and what objects are around you.  Try them out, you will be notified if
you can't use a certain command at this point in time.
			""")
		for action in available_actions:
			print("{}{}{}".format(BgColors.OKBLUE, action, BgColors.ENDC))


	#################################################################################################################################
	# METHODS TO ALLOW THE PLAYER TO MOVE AROUND - THESE ARE PART OF THE PLAYER CLASS
	def select_item(self, ref, container):
		try:
			item = [None]
			if ref.isdigit():
				#print( ref, container )
				for i in container:
					if hasattr(i, 'index'):
						if i.index == int(ref):
							return [i] #if i.index == int(ref) else [None]
				
				item = [container[int(ref)-1]]
			else:
				item = [x for x in container if x.name.upper().replace(' ','') == ref.upper().replace(' ','')]
		except (IndexError, AttributeError):
			item = [None]
		return item

	
	def move(self, dx, dy):
		if not self.has_torch():
			print( textwrap.fill("It is too dark to see.  You must discover how to light the way before continuing.  Use the [search] command to view items within the room.\n",70) )
		else:
			self.prev_location_x = self.location_x
			self.prev_location_y = self.location_y
			self.location_x += dx
			self.location_y += dy
				
			print( re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', self.world.tile_exists(self.location_x, self.location_y).intro_text().replace(r'\n','\n'), flags=re.M) )
		
			
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
		self.check_hp()
		print("{}Current Armor Level: {}{}".format(BgColors.OKGREEN, sum([x.block for x in self.inventory if isinstance(x, armor.Armor) and x.is_equipped()]), BgColors.ENDC))
		print("{}Current Damage Level: {}{}".format(BgColors.OKGREEN, sum([x.damage for x in self.inventory if isinstance(x, weapons.Weapon) and x.is_equipped()]), BgColors.ENDC))
		
		#if len([x for x in self.inventory if x.baseclass == 'Armor']) > 0:
		if len([x for x in self.inventory if isinstance(x, armor.Armor)]) > 0:
			print("\n{}Equipped Armor:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			#[print(x) for x in self.inventory if x.baseclass == 'Armor' and x.is_equipped()]
			[print(x) for x in self.inventory if isinstance(x, armor.Armor) and x.is_equipped()]
		
		#if len([x for x in self.inventory if x.classtype == 'Weapon']) > 0:
		if len([x for x in self.inventory if isinstance(x, weapons.Weapon)]) > 0:
			print("\n{}Equipped Weapons:{}".format(BgColors.OKBLUE, BgColors.ENDC))
			#[print(x) for x in self.inventory if x.classtype == 'Weapon' and x.is_equipped()]
			[print(x) for x in self.inventory if isinstance(x, weapons.Weapon) and x.is_equipped()]

		print("")
		self.check_skills()
		
	
	def get_inventory_size(self):
		return len([x for x in self.inventory if hasattr(x, 'equip') and not x.equip or not hasattr(x, 'equip')])
	
	def increase_health(self, amt):
		self.hp = min(100, self.hp+amt)
	
	def has_torch(self):
		#return any( item.name == 'Torch' for item in self.inventory )
		return any( isinstance(item, self.world._objects['Torch'].__class__) for item in self.inventory )
		
		
	def loot(self, enemy):
		objects = [i for i in enemy.get_items() if not i.is_taken()]
		if objects:
			for item in objects:
				if hasattr(item, 'amt'):
					print("{}You picked up {} {}!{}".format(BgColors.WARNING, item.amt, item.name, BgColors.ENDC))
				else:
					print("{}You picked up a {}!{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
				enemy.objects.remove(item)
				self.inventory.append(item)
		enemy.looted = True

	def search(self):
		objects = [i for i in self.room.get_items() if not i.is_taken()]
		if objects:
			print("A quick search around the room and you find the following item(s):\n")
			for index, item in enumerate(objects):
				print("{}.{} {}{}".format(index+1, BgColors.WARNING, item.description, BgColors.ENDC))
		else:
			print("{}No items available to interact with!{}".format(BgColors.FAIL, BgColors.ENDC))
			
	def read(self, item=None):
		if item:
			item = self.select_item(item, self.room.get_items())	
		else :
			item = [i for i in self.room.get_items() if isinstance(i, items.Readable)]
			#item = [i for i in self.room.get_items() if i.classtype == 'Readable']
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in the room! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		elif item:
			item = item[0]
			print(item.name) #print title of narrative
			print( textwrap.fill("{}".format(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', item.narrative, flags=re.M)),70) )
			
			if item.skill and item.inc_value and not item.is_read():
				item.read = True
				self.skills[item.skill.lower()]['value'] += item.inc_value
				print("\n{}You gained +{} {} experience!{}".format(BgColors.OKGREEN, item.inc_value, item.skill, BgColors.ENDC))
				

	def pick_up(self, item=None):
		if item:
			item = self.select_item(item, self.room.get_items())
		else: 
			item = [x for x in self.room.get_items() if issubclass(x.__class__,(items.Lootable,items.Usable))]
			#item = [x for x in self.room.get_items() if x.classtype in ['Lootable','Usable']]

			if len(item) > 1:
				print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in the room. Use the [search] command to view items within the room.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
				return
		
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in the room! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		elif [x for x in [item] if issubclass(x.__class__,items.Chest)]:
			print("{}You cannot pick this item up! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		if self.get_inventory_size()+1 > self.backpack.level:
			print("""
{}You don't have enough room in your backpack items.  
Find a larger backpack or drop items from your inventory.{}"""
.format(BgColors.FAIL, BgColors.ENDC))
		elif list(filter(None.__ne__, item)):
			item = item[0] # if not isinstance(item, list) else item[0]
			item.taken = True
			self.room.remove_item(item)
			self.room.reindex_items()
			if isinstance(item, gold.Gold):
				print( item )
				self.purse.add_coins(item.cost)
			elif isinstance(item, items.Item):
				print("{}You picked up the {}!{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
				self.inventory.append(item)
				self.reindex_inventory()
				
				
	def drop(self, item=None):
		if item:
			item = self.select_item(item, self.inventory)
		else:
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return  
		
		if not list(filter(None.__ne__, item)):
			print("{}That is not a valid item in your inventory!{}".format(BgColors.FAIL, BgColors.ENDC))
		elif item :
			item = item[0]
			if isinstance(item, items.Purse):
			#if item.classtype == 'Purse':
				print("{}You're going to need your gold purse...{}".format(BgColors.FAIL, BgColors.ENDC))
				return
			
			print("{}You dropped the {}.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			self.inventory.remove(item)
			item.equip = False
			item.taken = False
			self.room.add_item(item)
			self.room.reindex_items()
				
	
	def open(self, item=None):	
		if item: 
			item = self.select_item(item, self.room.get_items())
		else: 
			item = self.room.get_items()[0]
		
		if len([x for x in [item] if isinstance(x,items.Chest)]) > 1: #issubclass(x.__class__,items.Chest)]) > 1:
		#if len([x for x in [item] if x.classtype == 'Chest']) > 1:
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in the room. Use the [search] command to view items within the room.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
		elif len([x for x in [item] if not isinstance(x,items.Chest)]) > 1 : #issubclass(x.__class__,items.Chest)]:
			#print( item[0], isinstance(item[0],items.Chest) )
		#elif [x for x in [item] if x.classtype == 'Chest']:
			print("{}You cannot open this item! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		elif not list(filter(None.__ne__, item)):
			print("{}That is not an item in the room! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
			return 
		elif list(filter(None.__ne__, item)):
			item = item[0]
			item.taken = True
			self.room.remove_item(item)
			if isinstance(item, gold.Gold):
			#if item.baseclass == 'Gold':
				print("{}You opened the {} and found {} coins!{}".format(BgColors.OKGREEN, item.name, item.cost, BgColors.ENDC))
				self.purse.add_coins(item.cost)
			
	
	def use(self, item=None):
		if item:
			item = self.select_item(item, self.inventory)
		else:
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		elif item:
			item = item[0]
			room_items = self.room.get_items()
			room_item = room_items[0] if list(filter(None.__ne__, room_items)) else None
			
			if issubclass(item.__class__, items.Usable):
				if issubclass(item.__class__, potions.Potion):
				#if item.classtype == 'Potion':
					self.increase_health( item.hp )
					print("{}You used the {}. Health increased by {}.{}".format(BgColors.OKGREEN, item.name, item.hp, BgColors.ENDC))
					self.inventory.remove(item)
				
				elif list(filter(None.__ne__, self.room.interaction_item)) and item.__class__ == self.room.interaction_item[0].__class__ :
				#elif list(filter(None.__ne__, self.room.interaction_item)) and item.classtype == self.room.interaction_item[0].classtype :

					self.room.get_items()[0].moved = True
					self.room.isBlocked = False
					print("{}You used the {} on the {}.{}".format(BgColors.OKGREEN, item.name, self.room.get_items()[0].name, BgColors.ENDC))

				elif room_item and hasattr(room_item, 'interaction_item') and item.__class__ == room_item.interaction_item[0].__class__ :
				#elif room_item and hasattr(room_item, 'interaction_item') and item.classtype == room_item.interaction_item[0].classtype :
					room_item.moved = True
					print("{}You used the {} on the {}.{}".format(BgColors.OKGREEN, item.name, room_item.name, BgColors.ENDC))					
				else :
					print("{}Using the {} doesn't do anything here.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			else:
				print("{}The item you selected is not usable in that way. Select again...{}".format(BgColors.FAIL, BgColors.ENDC))			
	
	
	
	def equip(self, item=None):
		if item:
			item = self.select_item(item, self.inventory)
		else:
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		if not list(filter(None.__ne__, item)):
		 	print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		elif item:
			item = item[0]
			if isinstance(item, weapons.Weapon): #item.__class__.__bases__[0] == 'Weapon':
			#if item.classtype == 'Weapon': #item.__class__.__bases__[0] == 'Weapon':
				if item.hp <= 0:
					print("{}You can not equip the {}, it is broken{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
					return
				else :
					for i in self.inventory:
						if isinstance(i, weapons.Weapon):
						#if item.classtype == 'Weapon':
							i.equip = False
					item.equip = True
					print("{}You equipped the {}.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			elif isinstance(item, armor.Armor):
			#elif item.baseclass == 'Armor':
				for i in self.inventory:
					if isinstance(i, armor.Armor):
					#if item.baseclass == 'Armor':
						# ensure the same type of armor isn't already equipped (i.e. two boot types, etc.)
						if i.__class__.__bases__[0] == item.__class__.__bases__[0] and i.is_equipped():
						#if i.classtype == item.classtype and i.is_equipped():
							i.equip = False
				item.equip = True
				print("{}You equipped the {}.{}".format(BgColors.WARNING, item.name, BgColors.ENDC)) 
			else:
				print("{}You can't equip the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			
	
	def unequip(self, item=None):
		if item:
			item = self.select_item(item, self.inventory)
		else:
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		if not list(filter(None.__ne__, item)):
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
		elif item:
			item = item[0]
			if item.is_equipped():
				item.equip = False
				print("{}You unequiped the {}.{}".format(BgColors.WARNING, item.name, BgColors.ENDC))
			else: 
				print("{}You don't have the {} equipped!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))			
	
	
	def buy(self, merchant, item=None):
		if item:
			item = self.select_item(item, merchant[0].inventory)
		else:
			print( textwrap.fill("{}You must specify a value with an action! It looks like there are multiple items in the merchant's inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		if not list(filter(None.__ne__, item)):
			print( "{}That is not an item in the merchant's inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC) )
		elif item : #list(filter(None.__ne__, item)):
			item = item[0] if len(item) > 0 else None
			
			if not isinstance(item, items.Backpack) and self.get_inventory_size()+1 > self.backpack.level:
			#if not item.classtype == 'Backpack' and self.get_inventory_size()+1 > self.backpack.level:
				print("""
{}You don't have enough room in your backpack items.  
Find a larger backpack or drop items from your inventory.{}""".format(BgColors.FAIL, BgColors.ENDC))

			elif item.cost > self.purse.value :
				print("{}You don't have enough in your purse to purchase the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			else:
				print("{}You bought the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
				self.purse.remove_coins(item.cost)
				if isinstance(item, items.Backpack):
				#if item.classtype == 'Backpack' :
					self.backpack = item			
				else:
					self.inventory.append(item)
				merchant[0].inventory.remove(item)
	
	
	def sell(self, merchant, item=None):
		if item:
			item = self.select_item(item, self.inventory)
		else:
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		if list(filter(None.__ne__, item)):
			item = item[0] 
			if item.hp <= 0 and not isinstance(item, items.Usable):
			#if item.hp <= 0 and not item.classtype == 'Usable':
				print("{}You can not sell the {}, it is broken{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
				return
			if isinstance(item, items.Purse):
			#if item.classtype == 'Purse' :
				print("{}You're going to need your gold purse...{}".format(BgColors.FAIL, BgColors.ENDC))
			if item.cost == 0: #isinstance(item, items.Usable):
				print("{}There is no defined value for {}, you can't sell it!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
			else:
				print("{}You sold the {}.{}".format(BgColors.OKGREEN, item.name, BgColors.ENDC))
				self.inventory.remove(item)
				merchant[0].inventory.append(item)
				self.purse.add_coins(item.cost)
		else:
			print("{}That is not an item in your inventory! Select again...{}".format(BgColors.FAIL, BgColors.ENDC))
    
    
	def list(self, merchant):
		print("""
Hey there, take a look at my spectacular selection of items for sale.  You
won't find better deals anywhere else in the realm!
""")

		print("┌{}┐".format("─"*132))
		print("|", "{:<3}|".format('#'), "{}{:<16}|".format('Name',''), "{}{:<4}|".format('Value',''), "{}  |".format("HP"), "{} |".format("Defense"), "{} |".format("Damage"), "{:<68}|".format("Description")) #{:<20}
		print("|{}|".format("─"*132))

		for index,item in enumerate(merchant[0].inventory):			
			# First, get the HP of the item if it exists
			try :
				hp = item.kwargs['hp'] 
			except KeyError:
				try :
					hp = item.hp
				except AttributeError:
					hp = ''
			
			#stats_block += ', HP:%s' % hp if hp != 0 else ''
			
			# Next, get the block points of an item, if exists
			try :
				defense = item.block
			except AttributeError:
				defense = ''
				
			# Next, get the damage points of an item, if exists
			try :
				damage = item.damage
			except AttributeError:
				damage = ''
							
			#print("{}. {} | Value:{}, HP:{}\n{}{}{}\n".format(index+1, item.name, item.cost, hp, BgColors.WARNING, item.description, BgColors.ENDC))
			#print("{}. {} | Value:{}, HP:{} | {}{}{}\n".format(index+1, item.name, item.cost, hp, BgColors.WARNING, item.description, BgColors.ENDC))
			
			#print("{}. {} | Value:{}{} | {}{}{}".format(index+1, item.name, item.cost, stats_block, BgColors.WARNING, item.description, BgColors.ENDC))
			print("|", "{:<3}|".format(index+1), "{:<20}|".format(item.name), "{:<7}|".format(item.cost), "{:<6}|".format(hp), "{:<8}|".format(defense), "{:<7}|".format(damage), "{}{:<68}{}|".format(BgColors.WARNING, item.description, BgColors.ENDC)) #{:<20}
		print("└{}┘".format("─"*132))



	def save(self):
		"""Save the current state of the game."""
		try :
			
			
# 			class RoomHandler(jsonpickle.handlers.BaseHandler):
# 				def flatten(self,obj,data):
# 					print(obj, data)
# 					return obj
			
			#jsonpickle.handlers.registry.register(self.world.StartingRoom, RoomHandler)
			
			#print( self.room, self.room.__class__, type(self.room) )
			
#			with open('gsave.pkl', 'wb') as output:
#			dill.dump_session('gsave.pkl')
			
			#with open('gsave.pkl', 'w') as output:
				#output.write( jsonpickle.encode(self) )
				
			
# 				for item in self.world._objects :
# 					pickle.dump(item, output, pickle.DEFAULT_PROTOCOL)
# 				
# 				#for k,v in self.world.items() :
# 				pickle.dump(self.world, output, pickle.DEFAULT_PROTOCOL)
# 				
# 				pickle.dump(self.location_x, output, pickle.DEFAULT_PROTOCOL)
# 				pickle.dump(self.location_y, output, pickle.DEFAULT_PROTOCOL)
# 			
# 				
# 				pickle.dump(self.skills, output, pickle.DEFAULT_PROTOCOL)
# 				pickle.dump(self.purse, output, pickle.DEFAULT_PROTOCOL)
				
				#for item in self.inventory :
				#	pickle.dump(item, output, pickle.DEFAULT_PROTOCOL)
				
				#pickle.dump(self.backpack, output, pickle.DEFAULT_PROTOCOL)


					
			
			
				# In order to use pickle to serialize the player and world class instances
				# the entire world/tile/object model must be redesigned as pickle does not support
				# serializing dict attribute objects assigned as an attribute of a class.  The internal
				# objects must be instantiated as part of the parent class.
			
			print("{}Game state successfully saved.{}".format(BgColors.OKGREEN, BgColors.ENDC))
		except Exception:
			raise
			print("{}There was an error saving the game.  Sorry.{}".format(BgColors.FAIL, BgColors.ENDC))
	
	
	def repair(self, vendor, item=None):
		if item :
			item = self.select_item(item, self.inventory)
		else:
			print( textwrap.fill("{}You must specify a value with an action!  It looks like there are multiple items in your inventory. Use the [i] command to view items within your inventory.{}".format(BgColors.FAIL, BgColors.ENDC),70) )
			return
		if list(filter(None.__ne__, item)):
			vendor = vendor[0]
			item = item[0]
			if isinstance(item, weapons.Weapon) or isinstance(item, armor.Armor):
			#if item.classtype == 'Weapon' or item.baseclass == 'Armor':
				if item.hp == item.orig_hp :
					print("{}This item does not need repair. HP:{}/{}{}".format(BgColors.FAIL, item.hp, item.orig_hp, BgColors.ENDC))
				elif not vendor.can_repair(item) :
					print("{}This item can not be repaired by this vendor. Find a vendor with a higher repair level. Item Level:{}, Vendor Repair Level:{}{}".format(BgColors.FAIL, item.level, vendor.level, BgColors.ENDC))
				else :
					cost = vendor.repair_cost(item)
					action_found = False
					action_input = input( BgColors.HEADER + 'Would you like to repair the {} for {} coins? [y/n]: '.format(item.name,cost) + BgColors.ENDC).lower()
					print("\n")
					if action_input.lower() == 'y' :
						if self.purse.value >= cost :
							item.hp = item.orig_hp
							print("{}The {} have been successfully repaired to full health!  HP:{}/{}{}".format(BgColors.OKGREEN, item.name, item.hp, item.orig_hp, BgColors.ENDC))
							self.purse.remove_coins(cost)
						else :
							print("{}You don't have enough in your purse to repair the {}!{}".format(BgColors.FAIL, item.name, BgColors.ENDC))						
					
					if action_input.lower() not in ['y','n'] :
						print("{}You must provide a [y/n] answer!{}".format(BgColors.FAIL, BgColors.ENDC))
			else :
				print("{}You can't repair the {} because it is not armor or a weapon.{}".format(BgColors.FAIL, item.name, BgColors.ENDC))
				
				

	def exit(self):
		"""Exit the game rooms to win."""
		self.victory = True
		print( textwrap.fill("Being lost in this cavern was terrible. but as you emerge, you find yourself on a mountain ridge, overlooking a lively city in the distance.  It's over.  You are safe.\n\n Thank you for playing.\n",70))
	
	#################################################################################################################################
	# SETUP THE ATTACH METHOD FOR THE PLAYER TO ATTACH ENEMIES
	def attack(self, enemy):
		weapon = [item for item in self.inventory if isinstance(item, weapons.Weapon) and item.is_equipped()]
		#weapon = [item for item in self.inventory if item.classtype == 'Weapon' and item.is_equipped()]
		if weapon:
			weapon = weapon[0]
			# give a 65% chance of hitting the enemy with an attack
			if random.random() <= (self.skills['attack']['value']/100): #.65:
				print("{}You use the {} against {} for {} HP!{}\n".format(BgColors.WARNING, weapon.name, enemy.name, weapon.damage, BgColors.ENDC))
				enemy.hp = max(enemy.hp-weapon.damage,0)
				# decrease the hp of the weapon after each use
				weapon.hp = max(weapon.hp - math.floor(weapon.orig_hp * (1-(self.skills['wield']['value']/100))), 0)
				if weapon.hp <= 0:
					weapon.equip = False
					print("{}The {} has broken! You must equip a different weapon!{}".format(BgColors.FAIL, weapon.name, BgColors.ENDC))
				if not enemy.is_alive():
					print("{}You killed {}!{}\n".format(BgColors.OKGREEN, enemy.name, BgColors.ENDC))
					print("Check your HP with the hp command!")
			else:
				print("{}You missed!{}\n".format(BgColors.WARNING, BgColors.ENDC))
		else:
			print("{}You don't have a weapon equipped!{}\n".format(BgColors.FAIL, BgColors.ENDC))
	
	def flee(self, tile):
		"""Moves the player randomly to an adjacent tile"""
		
		if tile.x < self.prev_location_x :
			a = actions.MoveEast()
		if tile.x > self.prev_location_x :
			a = actions.MoveWest()
		if tile.y < self.prev_location_y :
			a = actions.MoveSouth()
		if tile.y > self.prev_location_y :
			a = actions.MoveNorth()		
		
		print ("{}You fled to the {}!{}".format(BgColors.WARNING, a.name.split(' ')[1], BgColors.ENDC ))
		self.do_action( a )

