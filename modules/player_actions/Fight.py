#!/usr/local/bin/python3

import math, random, re

from modules.bgcolors import BgColors
from modules import items
from modules import armor
from modules import weapons
#from modules import actions
from modules.helpers.health import Health
	
#################################################################################################################################
# SETUP THE ATTACH METHOD FOR THE PLAYER TO ATTACH ENEMIES

class Fight(object):
	
	@classmethod	
	def attack(cls, enemy, **kwargs):
		player = kwargs['player']
	
		# get the weapon that is equipped from the player's inventory
		weapon = [item for item in player.inventory if isinstance(item, weapons.Weapon) and item.is_equipped()]
		
		# check if the initial weapon find within the container was successful and weapon is a list with a valid element within the list
		if list(filter(None.__ne__, weapon)):
			# set the correct weapon variable for interactions
			weapon = weapon[0]
			# give a percentage chance of hitting the enemy with an attack based on the skill attach value
			if random.random() <= (player.skills['attack']['value']/100): 
				#print("{}You use the {} against {} for {} HP!{}\n".format(BgColors.WARNING, weapon.name, enemy.name, weapon.damage, BgColors.ENDC))
				# new enemy hp = the original enemy hp minus whatever the weapon damage does, or 0 is as low as the enemy health will go
				enemy.hp = max(enemy.hp-weapon.damage,0)
				# decrease the hp of the weapon after each use based on the wield skill value
				# 1. take wield skill and divide by 100 to get a decimal. 70/100 = .70
				# 2. take the decimal and subtract 1 to inverse the number so we only degrade by the opposite of 'avoid degradation' skill. 1-.70 = .30
				# 3. take this inversion (.30) and multiply by the weapon's original health.  .30*40 = 12
				# 4. take this new number (12) and subtract from current weapon health.  40-12 = 28
				# 5. get the max between new health number and 0 to prevent negative numbers. max(28,0) = 28
				weapon.hp = max(weapon.hp - math.floor(weapon.orig_hp * (1-(player.skills['wield']['value']/100))), 0)
				
				print("{}You attacked the {}:{}".format(BgColors.NORMAL, enemy.name, BgColors.ENDC))
				print("{}┌{}┐".format(BgColors.WARNING,"─"*50))
				print("|", "{:<24}|".format('Attack'), "{:<23}|".format( "%s DMG" % weapon.damage) )
				print("|", "{:<24}|".format('Weapon HP (%s)' % weapon.name), "{:<23}|".format( "%s/%s" % (weapon.hp, weapon.orig_hp) ) )
				print("|", "{:<24}|".format('Your HP'), "{:<23}|".format(player.hp) ) 
				print("{}└{}┘".format(BgColors.WARNING, "─"*50))
				
				# if new weapon health is less than or equal to 0, then the weapon is now broken
				if weapon.hp <= 0:
					# unequip the weapon automatically
					weapon.equip = False
					# print warning to player that weapon is broken and a new weapon must be equipped
					print("{}The {} has insufficient HP! You must equip a different weapon!{}".format(BgColors.FAIL, weapon.name, BgColors.ENDC))
				# if the enemy is dead after your attack, then print a successfully killed message
				if not Health.is_alive(enemy):
					print("\n{}You defeated the {}!{}".format(BgColors.OKGREEN, enemy.name, BgColors.ENDC))
					#print("{}Check your HP with the hp command.{}".format(BgColors.NORMAL, BgColors.ENDC))
			# if the random number is outside of the attack skill percentage, then you missed
			else:
				print("{}You missed!{}".format(BgColors.WARNING, BgColors.ENDC))
		# if you attack without a weapon equipped, then print error
		else:
			print("{}You don't have a weapon equipped!{}\n".format(BgColors.FAIL, BgColors.ENDC))
	
	
# 	@classmethod	
# 	def flee(player, tile, **kwargs):
# 		"""Moves the player randomly to an adjacent tile"""
# 		player = kwargs['player']
# 		
# 		# if last location x is greater than current location x, then we must have moved west to get here, move east would be reverse
# 		if tile.x < player.prev_location_x :
# 			a = actions.MoveEast()
# 		# if last location x is less than current location x, then we must hav emoved east to get here, move west would be reverse
# 		if tile.x > player.prev_location_x :
# 			a = actions.MoveWest()
# 		# if last location y is greater than current location y, then we must of have moved north to get here, move south would be reverse
# 		if tile.y < player.prev_location_y :
# 			a = actions.MoveSouth()
# 		# if last location y is less than current location y, then we must have moved south to get here, move north would be reverse
# 		if tile.y > player.prev_location_y :
# 			a = actions.MoveNorth()		
# 		
# 		print ("{}You fled to the {}! This is the way you came from.{}".format(BgColors.WARNING, a.name.split(' ')[1], BgColors.ENDC ))
# 		# call the do_action method to actually perform the move
# 		#player.do_action( a )

