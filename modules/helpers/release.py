#!/usr/local/bin/python3

import sys, io, os, shutil, requests, json, zipfile, subprocess

from distutils.dir_util import copy_tree


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
				return (False, j['assets'][0]['browser_download_url'])
			return (True,)


class Update(object):
	#################################################################################################################################
	# CREATE METHOD FOR UPDATING THE GAME DATA, IF `version` FOUND THE GAME VERSION TO BE OUT OF DATE

	download_path = r"C:\Windows\Temp\europa.protocol" if os.name == 'nt' else r"/tmp/europa.protocol"
	installation_path = r"C:\Program Files (x86)\The Europa Protocol" if os.name == 'nt' else ''
	installation_file = "The Europa Protocol.exe" if os.name == 'nt' else ''

	@classmethod
	def get_updates(cls, tk, browser_download_url):
		# get the files from the download url provided by the latest release api call
		print( "Retreiving game data from remote server...", end='' )
		tk.update()
		r = requests.get(browser_download_url)
		if r.ok:
			print( "Done." )
			print( "Extracting game data to temp directory...", end='' )
			tk.update()
			z = zipfile.ZipFile(io.BytesIO(r.content))
			z.extractall(cls.download_path)
			print( "Done." )
			tk.update()
    
	@classmethod
	def copy_contents(cls, tk):
		# copy the newly extracted update contents into the game directory
		print( "Copying game data to installation directory: %s..." % cls.installation_path, end='' )
		tk.update()
		copy_tree("%s\dist" % cls.download_path, cls.installation_path)
		print( "Done." )
		tk.update()
		
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
	def reload_game(cls):
		# now that the game data is new within the installation directory, we need to reload the game executable
		subprocess.Popen("%s\%s" % (cls.installation_path, cls.installation_file) )
		
		