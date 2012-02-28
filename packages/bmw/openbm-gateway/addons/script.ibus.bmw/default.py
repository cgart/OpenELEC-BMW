import os
import xbmc
import xbmcgui
import sys
import subprocess
import xbmcaddon
import signal

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
process = os.path.join( BASE_RESOURCE_PATH , "ibus.pid")
bmwLogoSmallImg = os.path.join ( BASE_RESOURCE_PATH, "bmw_logo_small.png")
AUTOEXEC_LINE = "xbmc.executescript('special://home/addons/script.ibus.bmw/bmwdaemon.py')"
AUTOEXEC_DIR = xbmc.translatePath( "special://profile" )

# check whenever we have to add autoexec line
def checkAutostart():
	autoexecfile = os.path.join( AUTOEXEC_DIR, 'autoexec.py' )                     
	if os.path.exists(autoexecfile):
	    fh = open(autoexecfile)
	    lines = []
	    for line in fh.readlines():
		 theLine = line.strip()
		 if theLine.startswith(AUTOEXEC_LINE):  
		         return
		 lines.append(str(line))
	    fh.close()
	    lines.append("\n" + AUTOEXEC_LINE + "\n")
	    f = open(autoexecfile, "w")
	    f.writelines(lines)
	    f.close()
	    return
	else:
	    f = open(autoexecfile, "w")
	    f.write("import xbmc\n")
	    f.write(AUTOEXEC_LINE + "\n")
	    f.close()
	    return

checkAutostart()

# if no parameters specified, then open settings
if (len(sys.argv) <= 1):
	__settings__ = xbmcaddon.Addon(id='script.ibus.bmw')
	__language__ = __settings__.getLocalizedString
	__settings__.openSettings()
        
        # write values from settings to the system config files
	f = open('/var/config/openbm-gateway.conf', 'w')
	f.write('DEV=%s\n' % __settings__.getSetting("ibus.device"))
	f.write('EVENT_FILE=%s\n' % __settings__.getSetting("ibus.eventfile"))
	f.write('LOG_FILE=%s\n' % __settings__.getSetting("ibus.logfile"))
	f.close()
			
	# try to restart openbm-gateway process
	proc = subprocess.Popen(["pidof", "openbm-gateway"], stdout=subprocess.PIPE) 

	# Kill process.
	for pid in proc.stdout:
		os.kill(int(pid), signal.SIGINT)
		xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)"%("Restarting", "BMW I-Bus restarting...", bmwLogoSmallImg))		
		try: 
			xbmc.sleep(500)
			os.kill(int(pid), 0)
			
			dialog = xbmcgui.Dialog()
			dialog.ok("Cannot restart ibus...", "IBus gateway could not be restarted, this is :(")
			
		except OSError as ex:
			continue
	
	# Save old logging file and create a new one.
	os.system("/usr/bin/openbm-gateway-run")
	
	#dialog = xbmcgui.Dialog()
	#dialog.ok("Please restart", "Settings are only applied after reboot.")

	#xbmc.executebuiltin('XBMC.RunScript(%s)' % os.path.join( os.getcwd(), "startobc.py" ))

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
		
		
