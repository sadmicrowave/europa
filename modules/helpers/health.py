#!/usr/local/bin/python3


class Health(object):
	
	@classmethod
	def set_max_health (cls) :
		return 75
	
	@classmethod
	def is_alive(cls, entity) :
		return entity.hp > 0
	
	@classmethod
	def increase_health(cls, entity, amt):
		# increase the player health by the additional hp amount, or max out at 100
		entity.hp = min(100, entity.hp+amt)
	
	@classmethod
	def get_hp(cls, entity):
		#print("{}Current HP Level: {}{}".format(BgColors.OKGREEN, entity.hp, BgColors.ENDC))
		return entity.hp
