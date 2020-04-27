import urllib
import time
import os
#import pygame
uri = "http://kaizhen.us"  #url where result will be declared
source = urllib.urlopen(uri).read()
nw_source=source
cntr=0
flg=True
while nw_source==source:
    if flg:
      time.sleep(5)  #refresh every 5 seconds
    try:
      nw_source = urllib.urlopen(uri).read()
      print(nw_source)
    except IOError:
      print "Error in reading url"
      flg=False
      continue
    cntr+=1
    print cntr," times refreshed"
 
    flg=True

#while True:
#  pass