#!/bin/bash


# INSTALL NODE JS AND DEPENDENCIES
display_help() {
    echo "Usage: $( basename $0 ) [option...] " >&2
    echo
    echo "   -h | --help           Display this help menu"
    echo "   -v | --verbose	       Increase logging/printing level"
#    echo "   --with-db-create      Execute with database [re]creation"
    echo
    exit 1
}

OPTS=`getopt -o vh --long verbose,help -n 'test' -- "$@"`
if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi

eval set -- "$OPTS"

VERBOSE=true

while true; do
	case "$1" in
    -v | --verbose)
	    VERBOSE=true
	    shift;;
    -h | --help)
    	display_help
    	exit 0
    	;;
    -- ) shift; break;;
    * ) break;;

	esac
done


if [ ! $(which python3) ]; then
	if $VERBOSE; then echo -e '\033[0;33m[+] Installing python3 ...\t\033[0m'; fi
	
	# Install homebrew for easy installation of python 3 if homebrew does not exist
	if [ ! $(which brew) ]; then
		if $VERBOSE; then echo -e '\033[0;33m[++] Installing homebrew packages and drivers...\t\033[0m'; fi
		ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"
		
		# update homebrew installation and paths
		brew update
		
		if $VERBOSE; then echo -e '\033[0;33m[++] Installing homebrew python3 package...\t\033[0m'; fi
		# install python tree
		brew install python3
		
		
		if $VERBOSE; then echo -e '\033[0;33m[++] Checking success of python3 installation...\t\033[0m'; fi
		python3 --version
		if [ $? -eq 0 ]; then 
			if $VERBOSE; then echo -e '\033[0;32m[++] Python3 installation succeeded!\t\033[0m'; fi 
		else 
			if $VERBOSE; then echo -e '\033[0;31m[++] Python3 installation failed!\t\033[0m'; fi
		fi
		
		if $VERBOSE; then echo -e '\033[0;33m[++] Installing python3 modules for program compilation...\t\033[0m'; fi
		pip3 install jsonpickle openpyxl
		
		
	fi
	
else

	if $VERBOSE; then echo -e '\033[0;33m[+] Python3 already installed...\t\033[0m'; fi
	
fi

echo -e '\033[0;33m[+] Finished. \033[0m\n'
