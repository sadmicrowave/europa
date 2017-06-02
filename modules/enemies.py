#!/usr/local/bin/python3


class Enemy:	
	def __init__(self, name, classtype, description, hp, damage, dead_message, level, loot_type=None):
		self.name 		 = name
		self.description = description
		self.hp 		 = hp
		self.damage 	 = damage
		self.classtype	 = classtype
		self.dead_message  = dead_message
		self.level		 = level
		self.loot_type	 = loot_type.upper() or None
		self.objects 	 = []
		self.looted	 	 = False
		
	def intro_text(self):
		if self.is_alive():
			return self.alive_message
		else:
			return self.dead_message
 
	def is_alive(self):
		return self.hp > 0

	def been_looted(self):
		return self.looted
    
	def get_items(self):
		return self.objects
	
	def match_loot_type(self, obj):
		return 	obj.__class__.__name__.upper() == self.loot_type

	def __str__(self):
		return self.description if self.is_alive() else self.dead_message
