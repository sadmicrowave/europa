#!/usr/local/bin/python3

# Note: in most game programming the x-y coordinate plane is different 
# from the one you learned in algebra. In the game world, (0,0) is in 
# the top left corner, x increases to the right, and y increases to the bottom.

import random, inspect, math
from modules.bgcolors import BgColors
from modules import actions
from modules import items
from modules import armor
from modules import weapons
from modules import world

# The MapTile class is going to provide a template for all of the tiles in our world, 
# which means we need to define the methods that all tiles will need.
class MapTile:
	# MapTile is actually a specific flavor of a base class.  We call it an abstract 
	# base class because we don’t want to create any instances of it.
	item = None
	def __init__(self, name, description, visited_description=None, item=[], interaction_item=[], isBlocked=False, floor=1):
		self.name = name
		self.x = None
		self.y = None
		self.description 			= description
		self.visited_description 	= (visited_description or "This appears to be an unremarkable area.") + "  You've been here before."
		self.objects 				= item
		self.isBlocked 				= isBlocked
		self.interaction_item 		= interaction_item
		self.visited 				= False
		self.floor 					= int(floor)
       
	# We will never create a MapTile directly, instead we will create subclasses. 
	# The code raise NotImplementedError() will warn us if we accidentally create a MapTile directly.
	#def intro_text(self):
	#	return self.description
	
	#def intro_text(self):
	#	return self.description
	
	def intro_text(self):
		message = None
		#for item in self.objects:
		#	if isinstance(item, items.Movable):
		#		message = self.description if not item.unblocked else "You see a moved {} in the room.  You've been here before.".format(item.name)
				
		if not message:
			message = self.description if not self.visited else self.visited_description
		return message	
 
	def modify_player(self, player):
		pass
	
	def modify_player(self, player):
		pass
	
	def add_item(self, item):
		self.objects.append( item )
	
	def remove_item(self, item):
		self.objects.remove( item )
	
	def get_items(self):
		return self.objects
		
	def reindex_items(self):
		i = 0		
		for index, item in enumerate(self.objects):	
			i += 1
			self.objects[index].index = i
	
	def is_visited(self):
		return self.visited == True
	
	# These methods provide some default behavior for a tile. The default actions that a player should have are: 
	# move to any adjacent tile and view inventory. The method adjacent_moves determines which moves are possible in the map. 
	# For each available action, we append an instance of one of our wrapper classes to the list. Since we used the wrapper 
	# classes, we will later have easy access to the names and hotkeys of the actions.
	def adjacent_moves(self, player=None):
		"""Returns all move actions for adjacent tiles."""
			
		moves = []
		if not self.isBlocked :		
			if player.world.__dict__.get('(%s, %s)' % (self.x + 1, self.y) ):
				moves.append(actions.MoveEast())
			if player.world.__dict__.get('(%s, %s)' % (self.x - 1, self.y)):
				moves.append(actions.MoveWest())
			if player.world.__dict__.get('(%s, %s)' % (self.x, self.y - 1)):
				moves.append(actions.MoveNorth())
			if player.world.__dict__.get('(%s, %s)' % (self.x, self.y + 1)):
				moves.append(actions.MoveSouth())
		
		else :
			# get the moves to go back to the previous location
			if self.x < player.prev_location_x :
				moves.append(actions.MoveEast())
			if self.x > player.prev_location_x :
				moves.append(actions.MoveWest())
			if self.y < player.prev_location_y :
				moves.append(actions.MoveSouth())
			if self.y > player.prev_location_y :
				moves.append(actions.MoveNorth())
			
		return moves

	def available_actions(self, player=None):
		"""Returns all of the available actions in this room."""
		buf = []
		
		moves = self.adjacent_moves(player)
		
		if self.objects:
			for item in self.objects:
				if isinstance(item, items.Container) and item.unblocked and not item.opened:
					buf.append( actions.Open() )
				elif isinstance(item, items.Readable) : #and not item.is_read():
					buf.append( actions.Read() )
				elif ( isinstance(item, items.Movable) and not item.unblocked ) or ( isinstance(item, items.Container) and not item.unblocked and not item.opened ):
					buf.append( actions.UseAction() )
				elif not isinstance(item, items.Container) and not isinstance(item, items.Readable) and not isinstance(item, items.Movable):
					buf.append( actions.PickUp() )
				
				
		
		# append a unique list of the available action objects (from buf) to moves.  This converts the list to
		# a dict, then removes duplicates, then converts the dict back to a list in order to append
		moves += list({type(k): k for k in buf}.values())
		
		moves += [actions.ViewInventory()
				,actions.Drop()
				,actions.CheckHp()
				,actions.CheckStats()
				,actions.Use()
				,actions.Equip()
				,actions.UnEquip()
				,actions.Search()
				,actions.Skills()
				,actions.Save()
				,actions.Quit()
				,actions.Map()
				,actions.ReadHidden()
				,actions.ViewJournal()
				]
				
		if self.name == 'LeaveCaveRoom' and not self.isBlocked:
			moves += [actions.Exit()]
		
		moves += [actions.Help()]
		
		return moves



#################################################################################################################################
# DEFINE TILES OF THE WORLD

class LeaveCaveRoom(MapTile):
	def __init__(self, name, description, visited_description, item=[], interaction_item=None, isBlocked=False, floor=1):
		super().__init__(name, description, visited_description, item, interaction_item, isBlocked, floor)
	
	
#class LootRoom(MapTile):
#	def __init__(self, name, description, visited_description, item=[], interaction_item=None, isBlocked=False, floor=None):
#		super().__init__(name, description, visited_description, item, interaction_item, isBlocked, floor)
#
#	def intro_text(self):
#		return self.description if self.objects and not self.visited else self.visited_description
#	
#	def modify_player(self, player):
#		pass


# A tile to encounter an new enemy
class EnemyRoom(MapTile):
	def __init__(self, x, y, enemy, interaction_item=None, isBlocked=False, floor=1):
		self.enemy = enemy[0]
		super().__init__(x, y)
	
	def modify_player(self, player):
		# We didn’t want enemies to respawn. So if the player already visited 
		# this room and killed the enemy, they should not engage battle again.
		# So we check if enemy is still alive...
		if self.enemy.is_alive():
			# give a 65% chance the enemy hits you with an attack
			if random.random() > (player.skills['evade']['value']/100): 
			
				armor_level = sum( [x.block for x in player.inventory if issubclass(x.__class__, armor.Armor) and x.is_equipped()] )
				#damage = (self.enemy.damage-armor_level) #if self.enemy.damage > armor_level else 0
				damage = self.enemy.damage
				
				# get the list of all inventory armor items that are equipped, in order to calculate the armor/block level
				equipped = [x for x in player.inventory if issubclass(x.__class__, armor.Armor) and x.is_equipped()]
				
				damage_inflicted = damage*(1-(player.skills['block']['value']/100)) #/ len(equipped)
				damage = damage_inflicted
				for i in equipped :
					# enemy_damage * [inverse of blocking skill points] / [number of equipped armor items]
					#armor_damage = damage*(1-(player.skills['block']['value']/100)) / len(equipped)
					
					i.hp = max(round(i.hp - (damage_inflicted/len(equipped)),2) if i.level <= self.enemy.level else i.hp,0)
					if i.hp <= 0 :
						i.equip = False
						print("{}The {} has broken! You must equip different armor!{}".format(BgColors.FAIL, i.name, BgColors.ENDC))
					
					damage = max(damage - (armor_level/len(equipped)),0)
				
				armor_quote = ". Your armor blocks {}!".format(min(damage_inflicted,armor_level)) if armor_level else '!'
				print("{}Enemy attacks with {} damage{}{}".format(BgColors.FAIL, round(damage_inflicted,2), armor_quote, BgColors.ENDC))
				
				# adjust player health based on remaining damage after armor blocks
				player.hp = max(int(player.hp - damage),0)
			
			else:
				print("{}Enemy missed!{}".format(BgColors.FAIL, BgColors.ENDC))
			
			print("{}Enemy HP: {}{}".format(BgColors.FAIL, self.enemy.hp, BgColors.ENDC))
			print("{}Your HP: {}{}".format(BgColors.OKGREEN, player.hp, BgColors.ENDC))
	
	
	# Add the attack and flee action options to any enemy room
	def available_actions(self, player=None):
		# If the enemy is still alive then the player’s only options are attack or flee. 
		# If the enemy is dead, then this room works like all other rooms.
		if self.enemy.is_alive():
			return [actions.Flee(tile=self)
				,actions.Attack(enemy=self.enemy)
				,actions.Equip()
				,actions.UnEquip()
				,actions.ViewInventory()
				,actions.Help()
				,actions.Use()
				,actions.CheckHp()
				,actions.CheckStats()
				,actions.Skills()
				,actions.Quit()
				]
		elif not self.enemy.is_alive() and not self.enemy.been_looted():
			# create some objects on the enemy to loot if they don't already exist
			if not self.enemy.objects:
				r = random.random()
				s = player.skills['loot']['value']/100
				if r <= s:
					loot = []
					# get a full list of all the lootable objects from the items master list
					for k, v in player.world._objects.items():
						if issubclass(v.__class__, items.Lootable) and v.level == self.enemy.level:
							loot.append( v )
										
					# calculate number of objects to be looted, based on threshold defined from player looting skill
					ran = min(math.floor(s/r), math.floor(100*(s/5)))
					# iterate for as many times as "ran" variable says there should be items lootable on the enemy
					for x in range( ran ):
						# randomly select one of the lootable items inside the master loot container
						loot_index = random.randint(1, len(loot))-1
						try:
							obj = loot[ loot_index ]
							item_name = obj.name.replace(' ','')
														
							if issubclass(obj.__class__, weapons.Weapon):
								# define an __init__ constructor method to be used when dynamically creating the object class
								def __constructor__(self, n, cl, d, c, da, h, l):
									# initialize super of class type
									super(self.__class__, self).__init__(name=n, classtype=cl, description=d, cost=c, damage=da, hp=h, level=l)
								
								# create the object class dynamically, utilizing __constructor__ for __init__ method
								item = type(obj.name, (eval("{}.{}".format("weapons",obj.classtype.replace(' ',''))),), {'__init__':__constructor__})
								# add new object to the global _objects object to be used throughout the world
								item = item(obj.name, obj.classtype, obj.description, obj.cost, obj.damage, obj.orig_hp, obj.level)
				
							if issubclass(obj.__class__, armor.Armor):
								def __constructor__(self, n, cl, d, c, b, h, l):
									# initialize super of class type
									super(self.__class__, self).__init__(name=n, classtype=cl, description=d, cost=c, block=b, hp=h, level=l)
							
								# create the object class dynamically, utilizing __constructor__ for __init__ method
								item = type(obj.name, (eval("{}.{}".format("armor",obj.classtype.replace(' ',''))),), {'__init__':__constructor__})
								# add new object to the global _objects object to be used throughout the world
								item = item(obj.name, obj.classtype, obj.description, obj.cost, obj.block, obj.hp, obj.level)
							
							if issubclass(obj.__class__,money.Money):
								def __constructor__(self, n, cl, d, a):
									# initialize super of class type
									super(self.__class__, self).__init__(name=n, classtype=cl, description=d, amt=a)
								
								# create the object class dynamically, utilizing __constructor__ for __init__ method
								item = type(obj.name, (eval("{}.{}".format("money",obj.classtype.replace(' ',''))),), {'__init__':__constructor__})
								# add new object to the global _objects object to be used throughout the world
								amt = math.floor(random.randint(math.floor(100*(s/5)), math.floor(100*s)))
								
								item = item(obj.name, obj.classtype, obj.description, amt)
							
							# remove the item from master lootable index so we can't select it again
							del loot[ loot_index ]
						
							#amt = ""
							#
							#	amt = math.floor(random.randint(math.floor(100*(s/5)), math.floor(100*s)))
							
							# place the item/object onto the enemy
							self.enemy.objects.append( item )
							
						except IndexError:
							pass
				
		action_list = super().available_actions(player)
		if self.enemy.objects:
			action_list += [actions.Loot(enemy=self.enemy)]
            
		return action_list
    
	def intro_text(self):
		if self.enemy.is_alive():
			message = self.description if not self.visited else self.visited_description
			
			message += "\n\n┌{}┐".format("─"*50)
			message += "\n|" + " {:<25}|".format('Name','') + " {:<4}|".format("HP") + " {:<16}|".format("Damage")
			message += "\n|{}|".format("─"*50)
			message += "\n|{}".format(BgColors.FAIL) + " {:<25}|".format(self.enemy.name) + " {:<4}|".format(self.enemy.hp) + " {:<16}{}|".format(self.enemy.damage, BgColors.ENDC)
			message += "\n└{}┘".format("─"*50)
			message += "\nCheck your current stats with the [cs] command."
			
			return message
		else:
			return self.enemy.dead_message

class MerchantRoom(MapTile):
	def __init__(self, x, y, merchant, interaction_item=None, isBlocked=False, floor=None):
		# items is a dict of items to sell and buy
		self.merchant = merchant
		
		#self.merchant = eval("merchants.Merchant{}()".format(merchant))
		super().__init__(x, y)

	# Add the buy, sell, and list action options to any enemy room
	def available_actions(self, player=None):        
		available_actions = [actions.Buy(merchant=self.merchant)
							,actions.Sell(merchant=self.merchant)
							,actions.List(merchant=self.merchant)
							]
		available_actions += super().available_actions(player)

		return available_actions

	def modify_player(self, player):
		pass

	def get_items(self):
		return self.merchant

	def intro_text(self):
		return self.description if not self.visited else self.visited_description
		


class RepairVendorRoom(MapTile):
	def __init__(self, x, y, vendor, interaction_item=None, isBlocked=False, floor=None):
		self.vendor = vendor
		super().__init__(x, y)

	# Add the buy, sell, and list action options to any enemy room
	def available_actions(self, player=None):        
		available_actions = super().available_actions(player)
		available_actions += [actions.Repair(vendor=self.vendor)]
		return available_actions

	def modify_player(self, player):
		pass

	def intro_text(self):
		return self.description if not self.visited else self.visited_description
		


        
        
        
        
        
        
        