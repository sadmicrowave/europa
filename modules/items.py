#!/usr/local/bin/python3

from res.bgcolors import BgColors



class Item():
	def __init__(self, name, description, cost, **kwargs):
		self.name 			= name
		self.description 	= description
		self.cost 			= cost
		self.kwargs			= kwargs
		self.taken			= False
		self.equip			= False
		self.value			= None

	# method to determine if the item has been picked up yet
	def is_taken(self):
		return self.taken == True

	def is_equipped(self):
		return self.equip == True

	#def __str__(self):
	#	return "{:<15} v{:<5} - {}{}{}".format(self.name, self.cost, BgColors.WARNING, self.description, BgColors.ENDC)


#class Item():
# 	def __init__(self, name=None, classtype=None, baseclass=None, description=None, cost=None, block=None, damage=None, hp=None, level=None, interaction_item=None, narrative=None, skill=None, value=None, items=None ): #**kwargs):
# 		self.name 			= name
# 		#self.classtype		= classtype
# 		self.baseclass		= baseclass
# 		self.description 	= description
# 		self.cost 			= cost
# 		#self.kwargs			= kwargs
# 		self.block 			= block
# 		self.damage 		= damage
# 		self.hp				= hp
# 		self.level 			= level
# 		self.interaction_item = interaction_item
# 		self.narrative 		= narrative
# 		self.skill 			= skill
# 		self.value			= value
# 		self.items 			= items
# 		
# 		self.index 			= 0
# 		
# 		self.taken			= False
# 		self.equip			= False
# 		self.moved			= False
# 		
# 
# 	# method to determine if the item has been picked up yet
# 	def is_taken(self):
# 		return self.taken == True
# 
# 	def is_equipped(self):
# 		return self.equip == True
# 
# 	def is_moved(self):
# 		return self.moved == True
# 
# 	def is_read(self):
# 		return self.read == True


#################################################################################################################################
# MONEY FOR THE ECONOMY
class Purse:
	def __init__(self,amt=0):
		self.name = 'Purse'
		self.description = 'A pouch for holding gold coins.'
		self.value = amt
		self.index = 1
		self.classtype = 'Purse'
		#self.baseclass = None

	def add_coins(self, amt):
		self.value += amt
		print("{}{} coin(s) has been added to your purse.{}".format(BgColors.WARNING, amt, BgColors.ENDC))

	def remove_coins(self, amt):
		self.value -= amt
		print("{}{} coin(s) has been removed from your purse.{}".format(BgColors.FAIL, amt, BgColors.ENDC))

	def __str__(self):
		#return "{} | Value:{}\n{}{}{}".format(self.name, self.value, BgColors.WARNING, self.description, BgColors.ENDC)
		return "{} | Value:{} | {}{}{}".format(self.name, self.value, BgColors.WARNING, self.description, BgColors.ENDC)


class Lootable(Item):
	def __init__(self, name, classtype, description, cost, hp, level):
		self.classtype = classtype
		self.level = level
		self.orig_hp = hp
		super().__init__(name, description, cost)


class Chest(Item):
	def __init__(self, name, classtype, description, cost, hp, interaction_item=[]):
		self.moved = False
		self.interaction_item = interaction_item
		super().__init__(name, description, cost)	
		
	def is_moved(self):
		return self.moved == True


class Usable(Item):
	def __init__(self, name, classtype, description, cost, hp, level):
		self.hp = hp
		super().__init__(name, description, cost)

	def __str__(self):
		cost_str = " | Value:{}".format(self.cost) if self.cost != 0 else ""
		hp_str 	 = " HP:{}".format(self.hp) if self.hp != 0 else ""
	#	#return "{}{}{}\n{}{}{}".format(self.name, cost_str, hp_str, BgColors.WARNING, self.description, BgColors.ENDC)
		return "{}{}{} | {}{}{}".format(self.name, cost_str, hp_str, BgColors.WARNING, self.description, BgColors.ENDC)

class Backpack(Lootable):
	def __init__(self, name, classtype, description, cost, hp, level):		
		self.classtype = classtype
		self.level = level
		super().__init__(name, classtype, description, cost, hp, level)

class Readable(Item):
	def __init__(self, name, classtype, description, narrative=None, skill=None, value=None):
		self.read = False
		self.skill = skill
		self.narrative = narrative
		self.inc_value = value
		super().__init__(name, description, None)

	def is_read(self):
		return self.read == True
	
	def __str__(self):
		return "{}{}{}".format(BgColors.WARNING, self.description, BgColors.ENDC)


class Movable():
	def __init__(self, name, classtype, description, items):
		self.name 			= name
		self.description 	= description
		self.classtype 		= classtype
		self.items			= items
		self.taken			= False
		self.moved			= False
		#super().__init__(name, description, cost)

	def is_taken(self):
		return self.taken == True

	def is_moved(self):
		return self.moved == True

	def __str__(self):
		#return "{} | Value:{}\n{}{}{}".format(self.name, self.value, BgColors.WARNING, self.description, BgColors.ENDC)
		return "{} | {}{}{}".format(self.name, BgColors.WARNING, self.description, BgColors.ENDC)

	def move(self):
		pass
	


# class Torch(Usable):
#     def __init__(self):
#         super().__init__(name="Torch", description="A flickering torch to light the way.", cost=0, hp=0) 
#         
# class Shovel(Usable):
#     def __init__(self):
#         super().__init__(name="Shovel", description="A long handled shovel for digging.", cost=0, hp=0)
# 
# class Rope(Usable):
#     def __init__(self):
#         super().__init__(name="Rope", description="A long rope suitable to hold your weight.", cost=0, hp=0)


# ------------------------------------------------------------------------------------------------------------------------------- #

# class Potion(Lootable):
#     def __init__(self, name, description, cost, hp):
#         self.hp = hp
#         super().__init__(name, description, cost, hp)
#  
#     def __str__(self):
#         return "{}{} | value {}\n{}{}{}\nHP: {}{}".format(BgColors.FAIL, self.name, self.cost, BgColors.ENDC, BgColors.WARNING, self.description, self.hp, BgColors.ENDC)

# class SmallHealthPotion(Potion):
#     def __init__(self):
#         super().__init__(name="Small Health Potion", description="A small healing potion.", cost=10, hp=5)
# 
# class MediumHealthPotion(Potion):
#     def __init__(self):
#         super().__init__(name="Medium Health Potion", description="A medium healing potion.", cost=20, hp=25)
# 
# class LargeHealthPotion(Potion):
#     def __init__(self):
#         super().__init__(name="Large Health Potion", description="A large healing potion.", cost=50, hp=50)

# ------------------------------------------------------------------------------------------------------------------------------- #


#################################################################################################################################
# TYPES OF NOTES
# class Note(Item):
# 	def __init__(self, description):
# 		super().__init__(None, description, None)
# 
# 	def __str__(self):
# 		return "{}{}{}".format(BgColors.WARNING, self.description, BgColors.ENDC)
    
# class Note1(Note):
#     def __init__(self):
#         message = """
# 		They're close...
# 		I don't know what they'll do if they find me, or the key for that matter!
# 		So I hid it. I buried it the cave to the west.
#         """
#         super().__init__(description=message)
#     
#     def intro_text(self):
#         return """
#         A crumpled piece of paper lies on the ground...
#         """  
        
        
        
        
        
        