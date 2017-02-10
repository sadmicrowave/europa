#!/usr/local/bin/python3

from modules import items

class Weapon(items.Lootable):	
	def __init__(self, name, classtype, description, cost, damage, hp, level):
		self.hp = hp
		self.level = level
		self.orig_hp = hp
		self.damage = damage
		super().__init__(name, classtype, description, cost, hp, level)

#	def __str__(self):
#		status_str = ''
#		if self.is_equipped() and self.hp > 0:
#			status_str = '{} (equipped){}'.format(BgColors.HEADER, BgColors.ENDC)
#		elif self.hp <= 0:
#			status_str = '{} (broken){}'.format(BgColors.FAIL, BgColors.ENDC)
#
#		hp_str = str(self.hp)
#		if self.hp < self.orig_hp:
#			hp_str += ' {}(-{}){}'.format(BgColors.FAIL, (self.orig_hp - self.hp), BgColors.ENDC)
#
#		#return "{}{} | Value:{}, HP:{}, Damage:{} \n{}{}{}".format(self.name, status_str, (self.cost if self.hp > 0 else 0), self.hp, self.damage, BgColors.WARNING, self.description, BgColors.ENDC)
#		return "{}{} | Value:{}, HP:{}, Damage:{} | {}{}{}".format(self.name, status_str, (self.cost if self.hp > 0 else 0), self.hp, self.damage, BgColors.WARNING, self.description, BgColors.ENDC)
