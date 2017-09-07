#!/usr/local/bin/python3

from modules.bgcolors import BgColors
from modules.helpers.skills import aSkills
from modules.helpers.health import Health

class Stats(object):
	@classmethod
	def check_stats(cls, **kwargs):
		player = kwargs['player']
		print("{}Stats:{}".format(BgColors.CADETBLUE, BgColors.ENDC))
		# print the player health
		Health.check_hp(**kwargs)
		# compile total sum of armor defense from equipped armor
		print("{}Current Armor Level: {}{}".format(BgColors.OKGREEN, sum([x.block for x in player.inventory if isinstance(x, armor.Armor) and x.is_equipped()]), BgColors.ENDC))
		# compile total sum of weapon damage from equipped weapons
		print("{}Current Damage Level: {}{}".format(BgColors.OKGREEN, sum([x.damage for x in player.inventory if isinstance(x, weapons.Weapon) and x.is_equipped()]), BgColors.ENDC))
																				
		# print each item of armor that is equipped
		if len([x for x in player.inventory if isinstance(x, armor.Armor)]) > 0:
			print("\n{}Equipped Armor:{}".format(BgColors.CADETBLUE, BgColors.ENDC))
			[print(x) for x in player.inventory if isinstance(x, armor.Armor) and x.is_equipped()]
																				
		# print each item of weapons that is equipped
		if len([x for x in player.inventory if isinstance(x, weapons.Weapon)]) > 0:
			print("\n{}Equipped Weapons:{}".format(BgColors.CADETBLUE, BgColors.ENDC))
			[print(x) for x in player.inventory if isinstance(x, weapons.Weapon) and x.is_equipped()]

		print("")
		# print the skills stats
		#cls.check_skills(**kwargs)
		aSkills.check_skills(**kwargs)
