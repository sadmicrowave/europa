#!/usr/local/bin/python3

from modules.bgcolors import BgColors
from modules import items

class aJournal (object):	
	
	@classmethod
	def __act__(cls, item=None, **kwargs):
		player = kwargs['player']
			
		i = 1
		print(BgColors.NORMAL + """
The following is a list of the narratives you have read through the realm and possess in 
your journal.  Each narrative has an associated number, name, and narrative summary. The
narrative index is sorted in ascending chronological order by date discovered. You can 
read narratives within your journal with the [read] [#] command.
		""")

		if len([x for x in player.journal if issubclass(x.__class__, items.Readable)]) > 0:
		
			for index, item in enumerate(player.journal):
				if item.index :
					i += 1
				else :
					player.journal[index].index = i
					
			print("{}┌{}┐".format(BgColors.NORMAL,"─"*111))
			print("|", "{:<3}|".format('#'), "{:<20}|".format('Name'), "{:<83}|".format("Narrative")) #{:<20}
			print("| {} |".format("─"*109))
	
			for index, item in enumerate(player.journal):
				if issubclass(item.__class__, items.Readable) :
					print("{}| {:<3}|".format(BgColors.NORMAL, item.index), "{:<20}|".format(item.name if len(item.name) <= 20 else item.name[0:17]+'...'), "{:<83}{}|".format(item.narrative if len(item.narrative) <= 83 else item.narrative[0:80]+'...', BgColors.ENDC)) #{:<20}
						
			print("{}└{}┘".format(BgColors.NORMAL, "─"*111))
		
		else :
			print("{}There are no entries in your journal.{}".format(BgColors.FAIL, BgColors.ENDC))
	
