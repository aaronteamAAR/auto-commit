from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from checker import FileChecker
from colorama import Fore, init
import time, config, os, datetime


init()


BG_GREEN = Fore.LIGHTGREEN_EX

BG_BLUE = Fore.BLUE

BLANK = Fore.RESET

BG_YELLOW = Fore.YELLOW

BG_RED = Fore.LIGHTRED_EX




eventColor = {
    "created" : BG_GREEN,
    "modified": BG_BLUE,
    "deleted": BG_RED,
    "moved": BG_YELLOW
}


def printColor(s, color=Fore.WHITE, brightness= Fore.RESET, **kwargs):
    
    print(f"{brightness}{color}{s}{Fore.RESET}", **kwargs)
    
    
class LogHandler(FileSystemEventHandler):
    
    
    def __init__(self, watchPattern, expectionPattern, doWatchDirectories) -> None:
        self.watchPattern = watchPattern
        self.expectionPattern = expectionPattern
        self.doWatchDirectories = doWatchDirectories
        self.fc = FileChecker(self.expectionPattern)
        
    def on_any_event(self, event):
        now = now = (datetime.datetime.now()).strftime("%H:%M:%S")
        
        if not event.is_directory:
            
            path = event.src_path
            
            if hasattr(event, 'dest_path'):
                path = event.src_path
                
            if path.endswith(self.watchPattern):