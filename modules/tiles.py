#!/usr/local/bin/python3

# Note: in most game programming the x-y coordinate plane is different 
# from the one you learned in algebra. In the game world, (0,0) is in 
# the top left corner, x increases to the right, and y increases to the bottom.

import random, inspect, math
from res.bgcolors import BgColors
from modules import actions
from modules import items
from modules import gold
from modules import armor
from modules import weapons
import world

# The MapTile class is going to provide a template for all of the tiles in our world, 
# which means we need to define the methods that all tiles will need.
class MapTile:
	# MapTile is actually a specific flavor of a base class.  We call it an abstract 
	# base class because we don’t want to create any instances of it.
	item = None
	def __init__(self, name, description, item=[], interaction_item=[], isBlocked=False):
		self.name = name
		self.x = None
		self.y = None
		self.description = description
		self.objects = item
		self.isBlocked = isBlocked
		self.interaction_item = interaction_item
       
	# We will never create a MapTile directly, instead we will create subclasses. 
	# The code raise NotImplementedError() will warn us if we accidentally create a MapTile directly.
	#def intro_text(self):
	#	return self.description
	
	#def intro_text(self):
	#	return self.description
	
	def intro_text(self):
		message = None
		for item in self.objects:
			if isinstance(item, items.Movable):
				message = self.description if item.moved == False else "You see a moved {} in the room.  You've been here before.".format(item.name)
		
		if not message:
			message = self.description
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

	
	# These methods provide some default behavior for a tile. The default actions that a player should have are: 
	# move to any adjacent tile and view inventory. The method adjacent_moves determines which moves are possible in the map. 
	# For each available action, we append an instance of one of our wrapper classes to the list. Since we used the wrapper 
	# classes, we will later have easy access to the names and hotkeys of the actions.
	def adjacent_moves(self, player=None):
		"""Returns all move actions for adjacent tiles."""
			
		moves = []
		if not self.isBlocked :		
			if player.world.__dict__.get( (self.x + 1, self.y) ):
				moves.append(actions.MoveEast())
			if player.world.__dict__.get((self.x - 1, self.y)):
				moves.append(actions.MoveWest())
			if player.world.__dict__.get((self.x, self.y - 1)):
				moves.append(actions.MoveNorth())
			if player.world.__dict__.get((self.x, self.y + 1)):
				moves.append(actions.MoveSouth())

		
		
# 			if world.World._world.get((self.x + 1, self.y)):
# 				moves.append(actions.MoveEast())
# 			if world.World._world.get((self.x - 1, self.y)):
# 				moves.append(actions.MoveWest())
# 			if world.World._world.get((self.x, self.y - 1)):
# 				moves.append(actions.MoveNorth())
# 			if world.World._world.get((self.x, self.y + 1)):
# 				moves.append(actions.MoveSouth())
		
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
				if issubclass(item.__class__, items.Chest) and item.is_moved() and not item.is_taken():
					buf.append( actions.Open() )
				elif issubclass(item.__class__, items.Readable) : #and not item.is_read():
					buf.append( actions.Read() )
				elif not issubclass(item.__class__, items.Chest) and not issubclass(item.__class__, items.Readable) and not item.is_taken() and not isinstance(item, items.Movable):
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
				]
				
		if self.name == 'LeaveCaveRoom' and not self.isBlocked:
			moves += [actions.Exit()]
		
		moves += [actions.Help()]
		
		return moves



#################################################################################################################################
# DEFINE TILES OF THE WORLD

class StartingRoom(MapTile):
	def __init__(self, name, description, item=[], interaction_item=None, isBlocked=False):
		super().__init__(name, description, item, interaction_item, isBlocked)
	
	def intro_text(self):
		torch_exists = False
		message = ''
		for item in self.objects:
			if item.name == 'Torch':
				torch_exists = True
				message = self.description
		
		if not torch_exists:
			message += "You see an empty holder for a torch on the wall.\nThis seems to be where you started...\n"
		return message + "\nYou can make out four paths, each equally as dark and foreboding."		
 
	def modify_player(self, player):
		pass

class LeaveCaveRoom(MapTile):
	def __init__(self, name, description, item=[], interaction_item=None, isBlocked=False):
		super().__init__(name, description, item, interaction_item, isBlocked)
	
	
class LootRoom(MapTile):
	def __init__(self, name, description, item=[], interaction_item=None, isBlocked=False):
		super().__init__(name, description, item, interaction_item, isBlocked)

	def intro_text(self):
		if self.objects:
			return self.description
		else:
			return "Another unremarkable part of the cave. You must forge onwards."

	def modify_player(self, player):
		pass

class ChestRoom(LootRoom):
	def __init__(self, name, description, item=[], interaction_item=None, isBlocked=False):
		super().__init__(name, description, item, interaction_item, isBlocked)
		
	def intro_text(self):
		if self.objects:
			return self.description
		else:
			return "An open and empty wooden chest resides in the room.  You've been here before."
	
	def modify_player(self, player):
		pass

class GoldRoom(ChestRoom):
	def __init__(self, name, description, item=[], interaction_item=None, isBlocked=False):		
		super().__init__(name, description, item, interaction_item, isBlocked)


# A tile to encounter an new enemy
class EnemyRoom(MapTile):
	def __init__(self, x, y, enemy, interaction_item=None, isBlocked=False):
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
							
							if issubclass(obj.__class__,gold.Gold):
								def __constructor__(self, n, cl, d, a):
									# initialize super of class type
									super(self.__class__, self).__init__(name=n, classtype=cl, description=d, amt=a)
								
								# create the object class dynamically, utilizing __constructor__ for __init__ method
								item = type(obj.name, (eval("{}.{}".format("gold",obj.classtype.replace(' ',''))),), {'__init__':__constructor__})
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
			message = self.description
			
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
	def __init__(self, x, y, merchant, interaction_item=None, isBlocked=False):
		# items is a dict of items to sell and buy
		self.merchant = merchant
		#self.objects =  merchant
		
		#self.merchant = eval("merchants.Merchant{}()".format(merchant))
		super().__init__(x, y)

	# Add the buy, sell, and list action options to any enemy room
	def available_actions(self, player=None):        
		available_actions = super().available_actions(player)
		available_actions += [actions.Buy(merchant=self.merchant)
							,actions.Sell(merchant=self.merchant)
							,actions.List(merchant=self.merchant)
							]
		return available_actions

	def modify_player(self, player):
		pass

	def get_items(self):
		return self.merchant

	def intro_text(self):
		return self.description
		


class RepairVendorRoom(MapTile):
	def __init__(self, x, y, vendor, interaction_item=None, isBlocked=False):
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
		return self.description
		




# class EmptyCavePath(MapTile):
# 	def __init__(self, name, description, item=None):
# 		pass
# 		
# 	def intro_text(self):
# 		return self.description
# 
# 	def modify_player(self, player):
# 		pass

# class EmptyCavePath(MapTile):
# 	def __init__(self, name, description, item=None):
# 		pass
# 	#	super().__init__(name, description, item)
# 	
# 	def intro_text(self):
# 		return self.description
# 
# 	def modify_player(self, player):
# 		pass

            
# class MerchantRoom(MapTile):
#     def __init__(self, x, y, merchant):
# 	    # items is a dict of items to sell and buy
#         self.merchant = eval("merchants.Merchant{}()".format(merchant))
#         super().__init__(x, y)
#  
#  	# Add the buy, sell, and list action options to any enemy room
#     def available_actions(self):        
#         available_actions = super().available_actions()
#         available_actions += [actions.Buy(merchant=self.merchant)
#         					 ,actions.Sell(merchant=self.merchant)
# 							 ,actions.List(merchant=self.merchant)
# 							 ]
#         return available_actions
#  
#     def modify_player(self, player):
#     	 pass
#     
#     def intro_text(self):
#         return self.merchant.intro_text()
# 
# class NoteRoom(MapTile):
#     def __init__(self, x, y, item):
#         self.item = eval("items.Note{}()".format(item))
#         # make the note taken so it doesn't trigger the 'pickup' action
#         self.item.taken = True
#         super().__init__(x, y, [self.item])
#  
#     def available_actions(self):        
#         available_actions = super().available_actions()
#         available_actions.append(actions.Read())
#         return available_actions
#  
#     def modify_player(self, player):
#     	 pass
#     
#     def intro_text(self):
#         return self.item.intro_text()
# 
# class KeyRoom(MapTile):
#     def __init__(self, x, y, item):
#         self.item = item
#         self.item.taken = True 
#         super().__init__(x, y, [item])
#   
#     def modify_player(self, player):
#     	 pass


# class LootRoom(MapTile):
#     def __init__(self, x, y, item):
#         if type(item) == str:
#             block = item.split('>',1)
#             self.message = block[1]
#             loot = [x for x in block[0].split('|')]
#             item = []
#                             
#             for i in loot:
#                 z = None
#                 if hasattr(weapons, i):
#                     z = getattr(weapons, i)
#                 elif hasattr(armor, i):
#                     z = getattr(armor, i)
#                 elif hasattr(items, i):
#                     z = getattr(items, i)
#                 if z:
#                     item.append( eval("{}.{}()".format(z.__module__, z.__name__)) )
#         else:
#             item = [item] 
#         
#         super().__init__(x, y, item)
#     
#     def intro_text(self):
#         if self.objects:
#             return self.message
#         else:
#             return "Another unremarkable part of the cave. You must forge onwards."
#  
#     def modify_player(self, player):
#     	 pass

# class ChestRoom(LootRoom):
#     def __init__(self, x, y, item):
#         super().__init__(x, y, item)
#      
#     def available_actions(self):
#         return super().available_actions(actions.Open())
# 
#     def modify_player(self, player):
#         pass
        


# class GoldRoom(ChestRoom):
#     def __init__(self, x, y, amount):
#         if amount.isdigit():
#             self.item = items.Gold(int(amount))
#         
#         else:
#             block = amount.split('>',1)
#             self.item = items.Gold(int(block[0]))
#             self.message = block[1]
#                         
#             #setattr(self.__class__, 'intro_text', intro_text)
#         
#         super().__init__(x, y, self.item)
#     
#     def intro_text(self):
#         if not self.item.is_taken():
#             return self.message
#         else:
#             return "Another unremarkable part of the cave. You must forge onwards."

 
#     def intro_text(self):
#         if self.item.is_taken():
#             return """
#             An empty treasure chest resides in the corner. You must forge onwards.
#             """
#         else:
#             return """
#             A very small treasure chest resides in the corner of the room.
#             """ 
    
#     def modify_player(self, player):
#         pass

# class EnemyRoom(MapTile):
#     def __init__(self, x, y, enemy):
#         #if '>' in enemy:
#         #    block = enemy.split('>',1)
#         #    self.message = block[1]
#         #    self.enemy = eval("enemies.{}()".format(block[0]))
#         #else:
#         #    self.enemy = eval("enemies.{}()".format(enemy))
#         #
#         #self.enemy.objects = []
#         super().__init__(x, y)        
#  
#     def modify_player(self, player):
# 	    # We didn’t want enemies to respawn. So if the player already visited 
# 	    # this room and killed the enemy, they should not engage battle again.
# 	    # So we check if enemy is still alive...
#         if self.enemy.is_alive():
#             armor_level = sum([x.hp for x in player.inventory if isinstance(x, items.Armor) and x.is_equipped()])
#             damage = (self.enemy.damage-armor_level) if self.enemy.damage > armor_level else 0
#             player.hp = player.hp - damage
#             print("\n{}Enemy HP is {}{}".format(BgColors.WARNING, self.enemy.hp, BgColors.ENDC))
#             armor_quote = "{}Damage reduced by {} from armor.{}".format(BgColors.FAIL, armor_level, BgColors.ENDC) if armor_level else ""
#             print("{}Enemy does {} damage.\nYou have {} HP remaining.{}\n{}".format(BgColors.FAIL, self.enemy.damage, player.hp, BgColors.ENDC, armor_quote))
# 
# 	# Add the attack and flee action options to any enemy room
#     def available_actions(self):
#         # If the enemy is still alive then the player’s only options are attack or flee. 
#         # If the enemy is dead, then this room works like all other rooms.
#         if self.enemy.is_alive():
#             return [actions.Flee(tile=self)
#             	   ,actions.Attack(enemy=self.enemy)
#             	   ,actions.Equip()
#             	   ,actions.UnEquip()
#             	   ,actions.ViewInventory()
#             	   ,actions.Help()
#             	   ,actions.Use()
#             	   ,actions.CheckHp()
#             	   ]
#         elif not self.enemy.is_alive() and not self.enemy.been_looted():
#             if not self.enemy.objects:
#                 number = random.randint(0, 3)
#                 if number > 0:
#                     loot = []
#                     def classloop(container, loot):
#                         for item in container:
#                             if item.__subclasses__():
#                                 classloop(item.__subclasses__(), loot)
#                             else:
#                                 loot.append( item )
#             
#                     classloop(items.Lootable.__subclasses__(), loot)
#                     
#                     for x in range(number):
#                         item = loot[ random.randint(1, len(loot))-1 ]
#                         amt = ""
#                         if isinstance(item, items.Gold):
#                             amt = random.randint(3,25)
#                         self.enemy.objects.append( eval("{}.{}({})".format(item.__module__, item.__name__, amt)) )
#                 
#         action_list = super().available_actions()
#         if self.enemy.objects:
#             action_list += [actions.Loot(enemy=self.enemy)]
#             
#         return action_list
#     
#     def intro_text(self):
#         if self.enemy.is_alive():
#             return self.message
#         else:
#             return "The remains of a defeated {} lay rotting on the ground.".format(self.enemy.name.lower())
#         #return self.enemy.intro_text()





#################################################################################################################################
# Now that we have some basic types of tiles defined, we can make some even more specific versions.



# class StartingRoom(MapTile):
#     def __init__(self, x, y):
#         super().__init__(x, y, [items.Torch()])
#     
#     def intro_text(self):
#         torch_exists = False
#         message = ""
#         for item in self.objects:
#             if isinstance(item, items.Torch):
#                 torch_exists = True
#                 message = """You awaken, dizzy and confused.  You find yourself on the dirty 
#                 ground in a cave with a flickering torch on the wall.  How did you get here?\n"""
#             
#         if not torch_exists:
#             message += "You see an empty holder for a torch on the wall.\nThis seems to be where you started...\n"
#         
#         return message + "\nYou can make out four paths, each equally as dark and foreboding."
#  
#     def modify_player(self, player):
#         #Room has no action on player
#         pass
# 
# class EmptyCavePath(MapTile):
#     def intro_text(self):
#         return "Another unremarkable part of the cave. You must forge onwards."
#  
#     def modify_player(self, player):
#         #Room has no action on player
#         pass

# class LeaveCaveRoom(MapTile):
#     def intro_text(self):
#         return """
#         You see a bright light in the distance...
#         ... it grows as you get closer! It's sunlight!
#  
#  
#         Victory is yours!
#         """
#  
#     def modify_player(self, player):
#         player.victory = True


         
        
        
        
        
        
        
        