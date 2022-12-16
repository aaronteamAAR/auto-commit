import asyncio
import sys
import os, time
import asyncio, logging

from watchfiles import awatch
from watchfiles import watch, run_process

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot




directory = 'C:/Users/Last Hokage/Documents/auto-commit'
# Watch for changes in dir 

if __name__ == "__main__":
    logging.basicConfig(level= logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
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