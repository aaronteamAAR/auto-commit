import asyncio
import sys, subprocess, click
import os, time, datetime
import asyncio, logging
from colorama import Fore, init

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot

init()

@click.command()
@click.option('--count', prompt="Your count number", default=1, help="Number of times to greet")
@click.option('--name', prompt="Your name please!",  help="Who to greet")
@click.option("--path", prompt="path to watch", help="choice a path to watch changes")

def main(count, name):
    '''SIMPLE PROGRAM TO GREET MULTI TIMES'''
    for _ in range(count):
        click.echo(f"helo,{name}")










BG_GREEN = Fore.LIGHTGREEN_EX

BG_BLUE = Fore.BLUE

BLANK = Fore.RESET

BG_YELLOW = Fore.YELLOW

BG_RED = Fore.LIGHTRED_EX

# Get directory location 

curr_dir = os.getcwd()
print(curr_dir.replace('\\', '/'))

directory = curr_dir
num_changes = 20
changes = 0
# Watch for changes in dir
now =  (datetime.datetime.now()).strftime("%H:%M:%S")
last_trigger_time = time.time()


# current branch

def currentBranch():
    res = subprocess.run(['git', 'rev-parse', '--abbrev-ref', "HEAD"], capture_output=True)
    return res.stdout.decode().strip()


branch = currentBranch()

print(branch)


class FileEventHandler(FileSystemEventHandler):
    
    
    def __init__(self):
        self.event_time=time.time()

    def on_any_event(self, event):
        now=time.time()
        timedelta=now-self.event_time
        self.event_time=now
        
    def on_created(self, event):
        # self.plugins_pending.append(event.src_path)
        print(f"{BG_GREEN}{now} Hey, {event.src_path} has been created!")

    def on_deleted(self, event):
        print(f"{BG_RED}{now} Oops! Someone deleted {event.src_path}!")

    def on_modified(self, event):
        global last_trigger_time, changes
        changes += 1
        current_time = time.time()
        try:
            if changes >= num_changes:
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m',"my commit"], check=True)
                subprocess.run(['git', 'push', 'origin', f'{branch}'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Git push error with changes to : {e}, try to resolve this manually")
            changes = 0
        
        if event.src_path.find('~') == -1 and (current_time - last_trigger_time) > 1:
            last_trigger_time = current_time
            print(f"{BG_BLUE}{now} Hey there!, {event.src_path} has been modified")
       
    
    def on_moved(self, event):
        print(f"{BG_YELLOW}{now} Someone moved {event.src_path} to {event.dest_path}")
        


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