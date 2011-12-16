#!D:\pylons\mydevenv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pastescript==1.7.3','console_scripts','paster'


__requires__ = 'pastescript'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('pastescript', 'console_scripts', 'paster')()
)


#from paste.script.serve import ServeCommand

#ServeCommand("serve").run(["development.ini"])
