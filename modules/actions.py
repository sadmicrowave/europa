#!/usr/local/bin/python3

from modules.player import Player
from modules.helpers.state import State
from modules.helpers.skills import aSkills
from modules.helpers.stats import Stats
from modules.helpers.help import aHelp
from modules.helpers.health import Health

from modules.player_actions.Move   import aMove
from modules.player_actions.PickUp import aPickUp
from modules.player_actions.Equip import aEquip
from modules.player_actions.UnEquip import aUnEquip
from modules.player_actions.Inventory import aInventory
from modules.player_actions.Read import aRead
from modules.player_actions.Drop import aDrop
from modules.player_actions.Open import aOpen
from modules.player_actions.Use import aUse
from modules.player_actions.Repair import aRepair
from modules.player_actions.Merchant import Merchant
from modules.player_actions.Fight import Fight
from modules.player_actions.Map import aMap
from modules.player_actions.Loot import aLoot
from modules.player_actions.Search import aSearch
from modules.player_actions.Journal import aJournal



# We now have behavior defined for certain actions. But within the game, 
# we need some additional information. First, we need to bind keyboard keys 
# to these actions. It would also be nice if we had a pretty name for each 
# action that could be displayed to the player. Because of this additional 
# meta information, we are going to wrap these behavior methods inside of classes. 
 
class Action():

	# For starters, the Action class will have a method assigned to it. This method will correspond directly 
	# to one of the action methods in the player class, which you will see shortly. Additionally, each Action 
	# will have a hotkey, the pretty name, and a slot for additional parameters. These additional parameters 
	# are specified by the special ** operator and are named kwargs by convention. Using **kwargs allows us to
	# make the Action class extremely flexible.	
	def __init__(self, method, name, hotkey, **kwargs):
		self.method = method
		self.hotkey = hotkey
		self.name = name
		self.kwargs = kwargs

	def __str__(self):
		m = '['
		for i,k in enumerate(self.hotkey):
			m += '|' if i > 0 else ''
			m += k
		m += ']'

		return "{:<15}:{}".format(m, self.name) # format with x number of spaces after text to standardize the string length


	@classmethod
	def get_actions(cls):
		return [ Attack()
				,Buy()
				,CheckHp()
				,CheckStats()
				,Drop()
				,Equip()
				,Inventory()
				,Journal()
				,List()
				,Loot()
				,Map()
				,MoveEast()
				,MoveNorth()
				,MoveSouth()
				,MoveWest()
				,Open()
				,PickUp()
				,Quit()
				,Read()
				,Repair()
				,Save()
				,Sell()
				,Search()
				,Skills()
				,UnEquip()
				,Use()
				]

	        
#################################################################################################################################
# DEFINE ACTIONS
class ItemAction(Action):
    pass
    #def __str__(self):
	 #   return "{} [name|index]: {}".format(self.hotkey, self.name)

class HiddenAction(Action):
	pass
	
class MerchantAction(Action):
	pass

class MoveNorth(Action):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.move_north, name='Move north', hotkey=['n','north'])
		super().__init__(method=aMove.move_north, name='Move north', hotkey=['n','north'], **kwargs)
 
class MoveSouth(Action):
	def __init__(self, **kwargs):
		super().__init__(method=aMove.move_south, name='Move south', hotkey=['s','south'], **kwargs)
 
class MoveEast(Action):
	def __init__(self, **kwargs):
		super().__init__(method=aMove.move_east, name='Move east', hotkey=['e','east'], **kwargs)
 
class MoveWest(Action):
	def __init__(self, **kwargs):
		super().__init__(method=aMove.move_west, name='Move west', hotkey=['w','west'], **kwargs)
 
#class Exit(Action):
#	def __init__(self, **kwargs):
#		super().__init__(method=Player.exit, name='Exit', hotkey=['exit'])
 
class Inventory(Action):
	def __init__(self, **kwargs):
		super().__init__(method=aInventory.__act__, name='View inventory', hotkey=['i'], **kwargs)

class Journal(HiddenAction):
	def __init__(self, **kwargs):
		super().__init__(method=aJournal.__act__, name='View journal', hotkey=['j'], **kwargs)

class Help(Action):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.extended_help, name='Help menu', hotkey=['?'], **kwargs)
                super().__init__(method=aHelp.extended_help, name='Help menu', hotkey=['?'], **kwargs)

class CheckHp(HiddenAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.check_hp, name='Check HP', hotkey=['hp'], **kwargs)
                super().__init__(method=Health.check_hp, name='Check HP', hotkey=['hp'], **kwargs)

class CheckStats(HiddenAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.check_stats, name='Check stats', hotkey=['cs','stats'])
                super().__init__(method=Stats.check_stats, name='Check stats', hotkey=['cs','stats'], **kwargs)

class Skills(HiddenAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.check_skills, name='Skills', hotkey=['sk','skills'], **kwargs)
                super().__init__(method=aSkills.check_skills, name='Skills', hotkey=['sk','skills'], **kwargs)

class Map(HiddenAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.map, name='Show map', hotkey=['m','map'])
		super().__init__(method=aMap.__act__, name='Show map', hotkey=['m','map'], **kwargs)

class Equip(ItemAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.equip, name='Equip item [Name|Item #]', hotkey=['eq','equip'])
		super().__init__(method=aEquip.__act__, name='Equip item [Name|Item #]', hotkey=['eq','equip'], **kwargs)

class UnEquip(ItemAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.unequip, name='Unequip item [Name|Item #]', hotkey=['un','unequip'])
		super().__init__(method=aUnEquip.__act__, name='Unequip item [Name|Item #]', hotkey=['un','unequip'], **kwargs)
	
class Use(ItemAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.use, name='Use item [Name|Item #]', hotkey=['u','use'])
		super().__init__(method=aUse.__act__, name='Use item [Name|Item #]', hotkey=['u','use'], **kwargs)

class UseAction(Action):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.use, name='Use item [Name|Item #]', hotkey=['u','use'])
		super().__init__(method=aUse.__act__, name='Use item [Name|Item #]', hotkey=['u','use'], **kwargs)

class Search(HiddenAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.search, name='Search the room for items', hotkey=['se','search'])
		super().__init__(method=aSearch.__act__, name='Search the room for items', hotkey=['se','search'], **kwargs)

class PickUp(Action):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.pick_up, name='Pick up item [Name|Item #]', hotkey=['p'])
		super().__init__(method=aPickUp.__act__, name='Pick up item [Name|Item #]', hotkey=['p'], **kwargs)

class Repair(Action):
	def __init__(self, vendor=None, **kwargs):
		#super().__init__(method=Player.repair, name='Repair an item [Name|Item #]', hotkey=['re','repair'], vendor=vendor)
		super().__init__(method=aRepair.__act__, name='Repair item [Name|Item #]', hotkey=['re','repair'], vendor=vendor, **kwargs)

class Open(Action):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.open, name='Open item [Name|Item #]', hotkey=['o','open'])
		super().__init__(method=aOpen.__act__, name='Open item [Name|Item #]', hotkey=['o','open'], **kwargs)
		
class Drop(ItemAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.drop, name='Drop item [Name|Item #]', hotkey=['d','drop'])
		super().__init__(method=aDrop.__act__, name='Drop item [Name|Item #]', hotkey=['d','drop'], **kwargs)

class Read(Action):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.read, name='Read item [Name|Item #]', hotkey=['r','read'])
		super().__init__(method=aRead.__act__, name='Read item [Name|Item #]', hotkey=['r','read'], **kwargs)

class ReadHidden(HiddenAction):
	def __init__(self, **kwargs):
		#super().__init__(method=Player.read, name='Read item [Name|Item #]', hotkey=['r','read'])
		super().__init__(method=aRead.__act__, name='Read item [Name|Item #]', hotkey=['r','read'], **kwargs)

class Buy(MerchantAction):
    def __init__(self, merchant=None, **kwargs):
	    #super().__init__(method=Player.buy, name='Buy from merchant [Name|Item #]', hotkey=['buy'], merchant=merchant)
	    super().__init__(method=Merchant.buy, name='Buy from merchant [Name|Item #]', hotkey=['buy'], merchant=merchant, **kwargs)

class Sell(MerchantAction):
    def __init__(self, merchant=None, **kwargs):
	    #super().__init__(method=Player.sell, name='Sell to merchant [Name|Item #]', hotkey=['sell'], merchant=merchant)
	    super().__init__(method=Merchant.sell, name='Sell to merchant [Name|Item #]', hotkey=['sell'], merchant=merchant, **kwargs)

class List(Action):
    def __init__(self, merchant=None, **kwargs):
	    #super().__init__(method=Player.list, name='List merchant items for sale', hotkey=['l','list'], merchant=merchant)
	    super().__init__(method=Merchant.list, name='List merchant items for sale', hotkey=['l','list'], merchant=merchant, **kwargs)
   
class Attack(Action):
    def __init__(self, enemy=None, **kwargs):
        #super().__init__(method=Player.attack, name='Attack', hotkey=['a','attack'], enemy=enemy)
        super().__init__(method=Fight.attack, name='Attack', hotkey=['a','attack'], enemy=enemy, **kwargs)

#class Flee(Action):
#    def __init__(self, tile, **kwargs):
#        #super().__init__(method=Player.flee, name='Flee', hotkey=['f','flee'], tile=tile)
#        super().__init__(method=Fight.flee, name='Flee', hotkey=['f','flee'], tile=tile, **kwargs)

class Loot(Action):
	def __init__(self, enemy=None, **kwargs):
		#super().__init__(method=Player.loot, name='Loot', hotkey=['l','loot'], enemy=enemy)
		super().__init__(method=aLoot.__act__, name='Loot', hotkey=['l','loot'], enemy=enemy, **kwargs)

class Save(HiddenAction):
	def __init__(self, **kwargs):
		super().__init__(method=State.save, name='Save Game', hotkey=['sa','save'], **kwargs)

class Quit(HiddenAction):
	def __init__(self, **kwargs):
		super().__init__(method=State.quit, name='Quit Game', hotkey=['q','quit'], **kwargs)


