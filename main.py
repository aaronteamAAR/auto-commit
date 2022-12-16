import asyncio
import sys
import os, time
import asyncio, logging
from colorama import Fore, init

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot

init()


BG_GREEN = Fore.LIGHTGREEN_EX

BG_BLUE = Fore.BLUE

BLANK = Fore.RESET

BG_YELLOW = Fore.YELLOW

BG_RED = Fore.LIGHTRED_EX



directory = 'C:/Users/Last Hokage/Documents/auto-commit'
# Watch for changes in dir

class FileEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        print(f"{BG_GREEN}Hey, {event.src_path} has been created!")

    def on_deleted(self, event):
        print(f"{BG_RED}Oops! Someone deleted {event.src_path}!")

    def on_modified(self, event):
        print(f"{BG_BLUE}Hey there!, {event.src_path} has been modified")
    
    def on_moved(self, event):
        print(f"{BG_YELLOW}Someone moved {event.src_path} to {event.dest_path}")
        


if __name__ == "__main__":
    logging.basicConfig(level= logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = directory
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


# Make sure the files goes through at least 8 events
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()