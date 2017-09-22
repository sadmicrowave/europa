#!/usr/local/bin/python3

import sys, io, os, shutil, requests, json, zipfile, subprocess, time

from distutils.dir_util import copy_tree
from win32com.client import Dispatch

from modules.bgcolors import BgColors

os.environ["REQUESTS_CA_BUNDLE"] = "cacert.pem"

class Check(object):
	#################################################################################################################################
	# CREATE METHOD FOR CHECKING THE VERSION OF THE GAME, TO SEE IF IT IS OUTDATED AND NEEDS UPDATING

	@classmethod
	def is_up_to_date(cls):
		# use github api to get latest release from repo
		r = requests.get('https://api.github.com/repos/sadmicrowave/europa/releases/latest')
		if r.ok :
			# compare tag_name from release api results to version in VERSION.txt file
			j = json.loads( r.text )
			if open("VERSION.txt", 'r').read() != j['tag_name'] :
				return (False, j['tag_name'], j['assets'][0]['browser_download_url'])
			return (True,)


class Update(object):
	#################################################################################################################################
	# CREATE METHOD FOR UPDATING THE GAME DATA, IF `version` FOUND THE GAME VERSION TO BE OUT OF DATE

	download_path = r"C:\Windows\Temp\europa.protocol" if os.name == 'nt' else r"/tmp/europa.protocol"
	installation_path = r"C:\Program Files (x86)\The Europa Protocol" if os.name == 'nt' else ''
	installation_file = "The Europa Protocol.exe" if os.name == 'nt' else ''

	@classmethod
	def get_updates(cls, version, tk, browser_download_url):
		# get the files from the download url provided by the latest release api call
		print( "Retreiving game data from remote server...", end='' )
		tk.update()
		r = requests.get(browser_download_url)
		if r.ok and r.content :
			print( "Done." )
			print( "Extracting game data to temp directory...", end='' )
			tk.update()
			z = zipfile.ZipFile(io.BytesIO(r.content))
			z.extractall(cls.download_path)
			print( "Done." )
			tk.update()
			
			# copy the game contents from the newly extracted temp dir to the installation dir
			cls.copy_contents(version, tk)
			# update the desktop shortcut path
			cls.update_desktop_shortcut(version, tk)
			
			# remove the temp dir from the system to prevent unnecessary harddrive usage
			cls.destroy_env(tk)
			print( BgColors.OKGREEN + "Update successful." + BgColors.ENDC)
			print( "Restarting game..." )
			tk.update()
			
			# wait long enough for the user to read all the log entries from the update
			time.sleep(3)
			
			# reload the game so the new version is being used
			cls.reload_game(version)
			# exit current version
			sys.exit()
				

	@classmethod
	def copy_contents(cls, version, tk):
		# copy the newly extracted update contents into the game directory
		print( "Copying game data to installation directory: %s..." % cls.installation_path, end='' )
		tk.update()
		copy_tree("%s\dist" % cls.download_path, '%s\%s' % (cls.installation_path, version))
		print( "Done." )
		tk.update()
	
	@classmethod
	def make_env(cls, version):
		# ensure the correct directory structure is in place to copy the new game contents into
		if not os.path.exists('%s\%s' % (cls.installation_path, version)):
			os.makedirs( '%s\%s' % (cls.installation_path, version) )
	
	@classmethod
	def destroy_env(cls, tk):
		# remove the directory structure that was created to download new game data
		if os.path.exists(cls.download_path):
			print( "Removing temporary extraction directory...", end='' )
			tk.update()
			shutil.rmtree(cls.download_path)
			print( "Done." )
			tk.update()
			
	@classmethod
	def reload_game(cls, version):
		# now that the game data is new within the installation directory, we need to reload the game executable
		subprocess.Popen( os.path.join(cls.installation_path, version, cls.installation_file) )
		
	@classmethod
	def update_desktop_shortcut(cls, version, tk):
		# update the desktop shortcut path, if windows and a desktop shortcut exists
		#print( os.listdir( os.path.join(os.getenv('userprofile'), 'desktop')) )
		desktop_shortcut = os.path.join(os.getenv('userprofile'), 'desktop', 'The Europa Protocol.lnk')
		if os.name == 'nt' and os.path.isfile( desktop_shortcut ) :
			print( "Updating desktop shortcut...", end='' )
			tk.update()
			# remove the desktop shortcut
			os.remove( desktop_shortcut )
			# begin creating a new shortcut to the new path
			shell = Dispatch('WScript.Shell')
			shortcut = shell.CreateShortCut(desktop_shortcut)
			shortcut.Targetpath = os.path.join(cls.installation_path, version, cls.installation_file)
			shortcut.WorkingDirectory = os.path.join(cls.installation_path, version)
			shortcut.IconLocation = os.path.join(cls.installation_path, version, 'game_icon.ico')
			shortcut.save()
			print( "Done." )
			tk.update()
			
			
			
			
			
			