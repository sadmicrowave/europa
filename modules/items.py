#!/usr/local/bin/python3

from modules.bgcolors import BgColors

class Item():
	def __init__(self, name, description, cost, **kwargs):
		self.name 			= name
		self.description 	= description
		self.cost 			= cost
		self.kwargs			= kwargs
		#self.taken			= False
		self.equip			= False
		self.value			= None
		self.opened			= False

	# method to determine if the item has been picked up yet
	#def is_taken(self):
	#	return self.taken == True
		
	def is_equipped(self):
		return self.equip == True
		
	def __str__(self):
		return self.description if not self.opened else self.description.replace(self.description[0:2], 'An opened ')
	


#################################################################################################################################
# MONEY FOR THE ECONOMY
class Wallet:
	def __init__(self,amt=0):
		self.name = 'Wallet Card'
		self.description = 'A digital card for storing credits.'
		self.value = amt
		self.index = 1
		self.classtype = 'Wallet'
		self.equip = True
		
	def is_equipped(self):
		return self.equip == True

	def add_credits(self, amt):
		self.value += amt
		print("{}{} credit(s) added to your wallet card.{}".format(BgColors.WARNING, amt, BgColors.ENDC))

	def remove_credits(self, amt):
		self.value -= amt
		print("{}{} credit(s) removed from your wallet card.{}".format(BgColors.FAIL, amt, BgColors.ENDC))


class Lootable(Item):
	def __init__(self, name, classtype, description, cost, hp, level):
		self.classtype = classtype
		self.level = level
		#self.orig_hp = hp
		super().__init__(name, description, cost)


class Container(Item):
	def __init__(self, name, classtype, description, item=[], interaction_item=[]):
		self.unblocked = False if interaction_item else True
		self.objects = item
		self.opened = False
		#cost = 0
		self.interaction_item = interaction_item
		super().__init__(name, description, item)	
		
	def is_unblocked(self):
		return self.unblocked == True


class Usable(Item):
	def __init__(self, name, classtype, description, cost, hp, level):
		self.hp = hp
		super().__init__(name, description, cost)

class Keypad(Usable):
	pass	

class Backpack(Lootable):
	def __init__(self, name, classtype, description, cost, hp, level):
		self.classtype = classtype
		self.level = level
		super().__init__(name, classtype, description, cost, hp, level)

class Readable(Item):
	def __init__(self, name, classtype, description, narrative=None, skill=None, value=None):
		self.read = False
		self.skill = skill
		self.index = None
		self.narrative = narrative
		self.inc_value = value
		super().__init__(name, description, None)

	def is_read(self):
		return self.read == True
	
	def __str__(self):
		return "{}{}{}".format(BgColors.WARNING, self.description, BgColors.ENDC)


class Money(Container):
	def __init__(self, name, classtype, description, amt, interaction_item=[]):
		self.amt = amt
		self.cost = amt
		hp = None
		super().__init__(name, classtype, description, amt, interaction_item)
		
		

class Movable():
	def __init__(self, name, classtype, description, moved_description, interaction_item=[], code=None):
		self.name 			= name
		self.description 	= description
		self.unblocked_description = moved_description
		self.classtype 		= classtype
		self.interaction_item = interaction_item
		self.code			= code
		self.taken			= False
		self.unblocked		= False

	def is_taken(self):
		return self.taken == True

	def is_unblocked(self):
		return self.unblocked == True

	def move(self):
		pass
	
	def key_match(self, keycode):
		return str(self.code) == str(keycode)
	
	def __str__(self):
		return self.description if not self.unblocked else self.unblocked_description
	
        
        
        
        
        