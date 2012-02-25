import sys, email, xbmcgui, xbmc
import string, time, mimetypes, re, os
import shutil
import xbmcaddon

AUTOEXEC_LINE = "xbmc.executescript('special://home/addons/script.resumelast/observer.py')\nxbmc.executescript('special://home/addons/script.resumelast/default.py')"
DATADIR = xbmc.translatePath( "special://profile/addon_data/script.resumelast/" )
AUTOEXEC_DIR = xbmc.translatePath( "special://profile" )
DATAFILE = os.path.join( DATADIR, "ResumeSaverA.xml" )
DATAFILE2 = os.path.join( DATADIR, "ResumeSaverB.xml" )

Addon = xbmcaddon.Addon(id=os.path.basename(os.getcwd()))

class resumePlayer:
        rewind_before_play = {}
        rewind_before_play['0'] = 0.0
        rewind_before_play['1'] = 5.0
        rewind_before_play['2'] = 15.0
        rewind_before_play['3'] = 60.0
        rewind_before_play['4'] = 180.0
        rewind_before_play['5'] = 300.0
        
        rewind_s = rewind_before_play[Addon.getSetting('rewind_before_play')]
        
        def main(self):
                if os.path.exists(DATAFILE):
                        self.opendata()
                else:
                        return "no datafile"
                time.sleep(0.5)
                if self.plsize == False: #there is no playlist
                        xbmc.Player().play(self.playing)
                        try:
                                xbmc.Player().seekTime(self.time)
                        except:pass
                #there must be a playlist present from now on
                self.testme()
                count = 0
                if self.media == "audio":
                        self.plist = xbmc.PlayList(0)
                elif self.media == "video":
                        self.plist = xbmc.PlayList(1)
                else:
                       self.plist = xbmc.PlayList(0) 
                self.plist.clear()
                if self.playing == False: #there is playlist but no media is playing
                        for count in range (0, self.plsize):
                             self.plist.add(self.playlist[count])
                             count = count + 1               
                if self.bingo == 1:#there is a playlist and the current playing song is in this playlist
                        for count in range (0, self.plsize):
                             self.plist.add(self.playlist[count])
                             count = count + 1
                        xbmc.Player().play(self.plist)
                        xbmc.Player().playselected(self.place)
                        try:
                                xbmc.Player().seekTime(self.time)
                        except:pass
                else:#there is a playlist that is loaded but a different file is playing over the top (need to make this so the file doesnt need to be added)
                        for count in range (0, self.place+1):
                             self.plist.add(self.playlist[count])
                             count = count + 1
                        self.plist.add(self.playing)
                        count = self.place
                        for count in range (self.place, self.plsize):
                             self.plist.add(self.playlist[count])
                             count = count + 1                        
                        xbmc.Player().play(self.plist)
                        xbmc.Player().playselected(self.place+1)
                        try:
                                xbmc.Player().seekTime(self.time)
                        except:pass
                        self.plist.remove(self.playing)
        def testme(self):
                fh = open(DATAFILE)
                count = 0
                try:
                        temp1 = self.playing
                except:
                        temp1 = "-"
                for count in range (0, self.plsize):
                        for line in fh.readlines():
                                theLine = line.strip()
                                temp3 = "<plistfile"+str(count)+">"
                                if theLine.startswith(temp3):
                                        temp4 = theLine[len(temp3):-1*len(temp3)-1]
                                        if temp4 == temp1:
                                                self.bingo = 1
                                                fh.close()
                                                return
                                        else:
                                                count = count + 1
                fh.close()
                self.bingo = 0
                return
        def opendata(self):
                firstFile = DATAFILE
                secondFile = DATAFILE2
                
                if ( os.access(firstFile, os.F_OK) and os.access(secondFile, os.F_OK) ):
                    xbmc.log('Both files exisitng. checking which is newer')
                    if ( os.path.getctime( secondFile ) > os.path.getctime( firstFile ) ):
                        firstFile = DATAFILE2
                        secondFile = DATAFILE
                        xbmc.log('swapping files')
                        
                try:
                        self.opendataex(firstFile)
                except:
                        self.opendataex(secondFile)
        def opendataex(self,datafile):
                self.playlist = []
                tag = ["<window>", "<volume>", "<time>", "<plspos>", "<plsize>","<playing>","<media>"]
                fh = open(datafile)
                count = 0
                for line in fh.readlines():
                        theLine = line.strip()
                        if theLine.count(tag[0]) > 0:
                              self.window = theLine[8:-9]
                        if theLine.count(tag[1]) > 0:
                              self.volume = theLine[8:-9]
                        if theLine.count(tag[2]) > 0:
                              self.time = theLine[6:-7]
                              if self.time == "-":
                                      self.time = False
                              else:
                                      self.time = float(self.time)
                              self.time = max( 0.0, self.time - self.rewind_s )
                        if theLine.count(tag[3]) > 0:
                              self.place = theLine[8:-9]
                              if self.place == "-":
                                      self.place = False
                              else:
                                      self.place = int(self.place)
                        if theLine.count(tag[4]) > 0:
                              self.plsize = theLine[8:-9]
                              if self.plsize == "-":
                                      self.plsize = False
                              else:  
                                      self.plsize = int(self.plsize)
                        if theLine.count(tag[5]) > 0:
                              self.playing = theLine[9:-10]
                              if self.playing == "-":
                                      self.playing = False
                        if theLine.count(tag[6]) > 0:
                              self.media = theLine[7:-8]
                              if self.media == "-":
                                      self.media = False
                fh.close()
                fh = open(DATAFILE)
                if self.plsize != 0:
                        for line in fh.readlines():
                                theLine = line.strip()
                                for count in range(0, self.plsize):
                                        temp = "<plistfile"+str(count)+">"
                                        if theLine.startswith(temp):
                                                temp = theLine[len(temp):-1*len(temp)-1]
                                                self.playlist.append(temp)
                                                count = count + 1
                else:pass
                fh.close()
                return
        def checkme(self):
                self.plist = xbmc.PlayList(0)
                self.plsize = self.plist.size()
                if self.plsize !=0:
                        self.media = "audio"
                        for i in range (0 , self.plsize):
                                temp = self.plist[i]
                                self.playlist.append(xbmc.PlayListItem.getfilename(temp))
                        return
                else:pass
                self.plist = xbmc.PlayList(1)
                self.plsize = self.plist.size()                
                if self.plsize !=0:
                        self.media = "video"
                        for i in range (0 , self.plsize):
                                temp = self.plist[i]
                                self.playlist.append(xbmc.PlayListItem.getfilename(temp))
                        return
                else:
                        self.media = "-"
                        self.plsize = "-"
                        self.playlist = "-"
                        return
        def addauto(self):
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
                    lines.append(AUTOEXEC_LINE+"\n")
                    f = open(autoexecfile, "w")
                    f.writelines(lines)
                    f.close()
                    return
            else:
                    f = open(autoexecfile, "w")
                    f.write("import xbmc\n")
                    f.write(AUTOEXEC_LINE)
                    f.close()
                    return
m = resumePlayer()
m.addauto()
m.main()
del m
