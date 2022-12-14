import asyncio
import sys
import time
import random

import os
import shutil
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler




directory = 'C:/Users/Last Hokage/Documents/auto-commit'



for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    if os.path.isfile(f):
       print(f)


class FileEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        print(f"Hey, {event.src_path} has been created! ++")
        print(event.src_path)

    def on_deleted(self, event):
        print(f"Oops! Someone deleted {event.src_path}! - -")

    def on_modified(self, event):
        print(f"Hey there!, {event.src_path} has been modified ++")
        
    
    def on_moved(self, event):
        print(f"Someone moved {event.src_path} to {event.dest_path}")
        


# async def main():
#      async for changes in awatch(f, watch_filter=Web):
#          print(changes)

 
# asyncio.run(main())


event_handler = FileEventHandler()

# Initialize Observer
observer = Observer()

# Schedule the Observer
observer.schedule(event_handler, directory, recursive=True)


# Start the Observer
observer.start()

try:
    while True:
        time.sleep(10)
        print("still running...")
except KeyboardInterrupt:
    print("stopped!")
    observer.stop()