#!/usr/local/bin/python3

from player import Player

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
    def __init__(self):
        super().__init__(method=Player.move_north, name='Move north', hotkey=['n','north'])
 
class MoveSouth(Action):
    def __init__(self):
        super().__init__(method=Player.move_south, name='Move south', hotkey=['s','south'])
 
class MoveEast(Action):
    def __init__(self):
        super().__init__(method=Player.move_east, name='Move east', hotkey=['e','east'])
 
class MoveWest(Action):
    def __init__(self):
        super().__init__(method=Player.move_west, name='Move west', hotkey=['w','west'])
 
class Exit(Action):
    def __init__(self):
        super().__init__(method=Player.exit, name='Exit', hotkey=['exit'])
 
class ViewInventory(Action):
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View inventory', hotkey=['i'])

class Help(Action):
    def __init__(self):
        super().__init__(method=Player.extended_help, name='Help menu', hotkey=['?'])

class CheckHp(HiddenAction):
	def __init__(self):
		super().__init__(method=Player.check_hp, name='Check HP', hotkey=['hp'])

class CheckStats(HiddenAction):
	def __init__(self):
		super().__init__(method=Player.check_stats, name='Check stats', hotkey=['cs','stats'])

class Map(HiddenAction):
	def __init__(self):
		super().__init__(method=Player.map, name='Show map', hotkey=['m','map'])

class Equip(ItemAction):
	def __init__(self):
		super().__init__(method=Player.equip, name='Equip item [Name|Item #]', hotkey=['eq','equip'])

class UnEquip(ItemAction):
	def __init__(self):
		super().__init__(method=Player.unequip, name='Unequip item [Name|Item #]', hotkey=['un','unequip'])
	
class Use(ItemAction):
	def __init__(self):
		super().__init__(method=Player.use, name='Use item [Name|Item Number]', hotkey=['u','use'])

class Search(HiddenAction):
	def __init__(self):
		super().__init__(method=Player.search, name='Search the room for items', hotkey=['se','search'])

class PickUp(Action):
	def __init__(self):
		super().__init__(method=Player.pick_up, name='Pick up item [Name|Item #]', hotkey=['p'])

class Repair(Action):
	def __init__(self, vendor):
		super().__init__(method=Player.repair, name='Repair an item [Name|Item #]', hotkey=['re','repair'], vendor=vendor)

class Open(Action):
	def __init__(self):
		super().__init__(method=Player.open, name='Open item [Name|Item #]', hotkey=['o','open'])
		
class Drop(ItemAction):
	def __init__(self):
		super().__init__(method=Player.drop, name='Drop item [Name|Item #]', hotkey=['d','drop'])

class Read(Action):
	def __init__(self):
		super().__init__(method=Player.read, name='Read item [Name|Item #]', hotkey=['r','read'])
		
class Buy(MerchantAction):
    def __init__(self, merchant):
	    super().__init__(method=Player.buy, name='Buy from merchant [Name|Item #]', hotkey=['buy'], merchant=merchant)

class Sell(MerchantAction):
    def __init__(self, merchant):
	    super().__init__(method=Player.sell, name='Sell to merchant [Name|Item #]', hotkey=['sell'], merchant=merchant)

class List(Action):
    def __init__(self, merchant):
	    super().__init__(method=Player.list, name='List merchant items for sale', hotkey=['l','list'], merchant=merchant)
   
class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name='Attack', hotkey=['a','attack'], enemy=enemy)

class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name='Flee', hotkey=['f','flee'], tile=tile)

class Loot(Action):
	def __init__(self, enemy):
		super().__init__(method=Player.loot, name='Loot', hotkey=['l','loot'], enemy=enemy)

class Skills(HiddenAction):
	def __init__(self):
		super().__init__(method=Player.check_skills, name='Skills', hotkey=['sk','skills'])
		
class Save(HiddenAction):
	def __init__(self):
		super().__init__(method=Player.save, name='Save Game', hotkey=['sa','save'])

class Quit(HiddenAction):
	def __init__(self):
		super().__init__(method=Player.quit, name='Quit Game', hotkey=['q','quit'])




