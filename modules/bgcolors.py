#!/usr/local/bin/python3


# class BgColors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'
    

class BgColors:
	
	HEADER = '[!HEADER!]'
	OKBLUE = '[!OKBLUE!]'
	SKYBLUE = '[!SKYBLUE!]'
	CADETBLUE = '[!CADETBLUE!]'
	OKGREEN = '[!OKGREEN!]'
	WARNING = '[!WARNING!]'
	NORMAL = '[!NORMAL!]'
	FAIL = '[!FAIL!]'
	ENDC = '[!ENDC!]'
	#BOLD = '\033[1m'
	#UNDERLINE = '\033[4m'

	def __init__(self, t):
		# HEADER = PINK
		t.tag_add('HEADER','1.0','1.0')
		t.tag_config('HEADER', foreground='pale violet red')

		#OKBLUE = BLUE
		t.tag_add('OKBLUE','1.0','1.0')
		t.tag_config('OKBLUE', foreground='dodger blue')
	
		#SKYBLUE = BLUE
		t.tag_add('SKYBLUE','1.0','1.0')
		t.tag_config('SKYBLUE', foreground='sky blue')
		
		#CADETBLUE = BLUE
		t.tag_add('CADETBLUE','1.0','1.0')
		t.tag_config('CADETBLUE', foreground='cadet blue')
		
		#OKGREEN = GREEN
		t.tag_add('OKGREEN','1.0','1.0')
		t.tag_config('OKGREEN', foreground='green')
		
		#WARNING = YELLOW
		t.tag_add('WARNING','1.0','1.0')
		t.tag_config('WARNING', foreground='yellow')
		
		#FAIL = RED
		t.tag_add('FAIL','1.0','1.0')
		t.tag_config('FAIL', foreground='tomato')
		
		#NORMAL = WHITE
		t.tag_add('NORMAL','1.0','1.0')
		t.tag_config('NORMAL', foreground='white')
