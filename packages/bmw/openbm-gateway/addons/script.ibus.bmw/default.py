import os
import xbmc
import xbmcgui
import sys

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
process = os.path.join( BASE_RESOURCE_PATH , "ibus.pid")

if (len(sys.argv) <= 1):
#	dialog = xbmcgui.Dialog()
#	dialog.ok("Cannot run directly", "This program cannot be executed directly, start it from the home screen", "i.e. 'radio' - to start radio, etc")
	xbmc.executebuiltin('XBMC.RunScript(%s)' % os.path.join( os.getcwd(), "startobc.py" ))
else:
	if not os.path.exists(process):
		dialog = xbmcgui.Dialog()
		dialog.ok("No connection to I-Bus daemon", "Make sure that bmwdaemon.py is running", "and that the connection is established")
	else:
		# check what we would like to start
		if (sys.argv[1] == "radio"):
			xbmc.executebuiltin('XBMC.RunScript(%s)' % os.path.join( os.getcwd(), "startradio.py" ))
		elif (sys.argv[1] == "obc"):
			xbmc.executebuiltin('XBMC.RunScript(%s)' % os.path.join( os.getcwd(), "startobc.py" ))
		
		
