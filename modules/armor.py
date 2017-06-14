#!/usr/local/bin/python3

from modules import items

class Armor(items.Lootable):	
	def __init__(self, name, classtype, description, cost, block, hp, level):
		self.hp = hp
		self.orig_hp = hp
		self.level = level
		self.block = block
		self.classtype = classtype
		super().__init__(name, classtype, description, cost, hp, level)
		
	#def __str__(self):
	#	status_str = ''
	#	if self.is_equipped() and self.hp > 0:
	#		status_str = '{} (equipped){}'.format(BgColors.HEADER, BgColors.ENDC)
	#	elif self.hp <= 0:
	#		status_str = '{} (broken){}'.format(BgColors.FAIL, BgColors.ENDC)
	#	
	#	#return "{}{} | Value:{}, HP:{}, Blocks:{}\n{}{}{}".format(self.name, status_str, (self.cost if self.hp > 0 else 0), self.hp, self.block, BgColors.WARNING, self.description, BgColors.ENDC)
	#	#return "{}{} | Value:{}, HP:{}, Defense:{} | {}{}{}".format(self.name, status_str, (self.cost if self.hp > 0 else 0), self.hp, self.block, BgColors.WARNING, self.description, BgColors.ENDC)


# ------------------------------------------------------------------------------------------------------------------------------- #
class Shield(Armor):
	def __init__(self, name, classtype, description, cost, block, hp, level):
		super().__init__(name, classtype, description, cost, block, hp, level)

# ------------------------------------------------------------------------------------------------------------------------------- #
class Gloves(Armor):
	def __init__(self, name, classtype, description, cost, block, hp, level):
		super().__init__(name, classtype, description, cost, block, hp, level)

# ------------------------------------------------------------------------------------------------------------------------------- #
class Boots(Armor):
	def __init__(self, name, classtype, description, cost, block, hp, level):
		super().__init__(name, classtype, description, cost, block, hp, level)

# ------------------------------------------------------------------------------------------------------------------------------- #
class ChestPlate(Armor):
	def __init__(self, name, classtype, description, cost, block, hp, level):
		super().__init__(name, classtype, description, cost, block, hp, level)

# ------------------------------------------------------------------------------------------------------------------------------- #
class Leggings(Armor):
	def __init__(self, name, classtype, description, cost, block, hp, level):
		super().__init__(name, classtype, description, cost, block, hp, level)

# ------------------------------------------------------------------------------------------------------------------------------- #
class Helmet(Armor):
	def __init__(self, name, classtype, description, cost, block, hp, level):
		super().__init__(name, classtype, description, cost, block, hp, level)
       
