from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# from checker import FileChecker
from colorama import Fore, Style, init
import time,  os, datetime


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
        # self.fc = FileChecker(self.expectionPattern)
        
    def on_any_event(self, event):
        now = now = (datetime.datetime.now()).strftime("%H:%M:%S")
        
        if not event.is_directory:
            
            path = event.src_path
            
            if hasattr(event, 'dest_path'):
                path = event.src_path
                
                if path.endswith(config.LOG_FILES_EXTENSIONS):
                    for type, msg in self.fc.checkForException(event=event, path=path):
                            printColor(msg, color=eventColor[event.event_type])
                    else:
                         printColor(msg, color=eventColor[event.event_type])
                else:
                      printColor(msg, color=eventColor[event.event_type])
        elif self.doWatchDirectories:
            msg = f"{now} -- {event.event_type} -- Folder: {event.src_path}"
            printColor(msg, color=eventColor[event.event_type])

    def on_modified(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_created(self, event):
        pass

    def on_moved(self, event):
        pass
    
    
    
class LogWatcher:
    # Initialize the observer
    observer = None
    # Initialize the stop signal variable
    stop_signal = 0
    # The observer is the class that watches for any file system change and then dispatches the event to the event handler.
    def __init__(self, watchDirectory, watchDelay, watchRecursively, watchPattern, doWatchDirectories, exceptionPattern, sessionid, namespace):
        # Initialize variables in relation
        self.watchDirectory = watchDirectory
        self.watchDelay = watchDelay
        self.watchRecursively = watchRecursively
        self.watchPattern = watchPattern
        self.doWatchDirectories = doWatchDirectories
        self.exceptionPattern = exceptionPattern
        self.namespace = namespace
        self.sessionid = sessionid

        # Create an instance of watchdog.observer
        self.observer = Observer()
        # The event handler is an object that will be notified when something happens to the file system.
        self.event_handler = LogHandler(watchPattern, exceptionPattern, self.doWatchDirectories)

    def schedule(self):
        print("Observer Scheduled:", self.observer.name)
        # Call the schedule function via the Observer instance attaching the event
        self.observer.schedule(
            self.event_handler, self.watchDirectory, recursive=self.watchRecursively)

    def start(self):
        print("Observer Started:", self.observer.name)
        self.schedule()
        # Start the observer thread and wait for it to generate events
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Observer: {self.observer.name} - Started On: {now} - Related To Session: {self.sessionid}"
        print(msg)

        msg = (
            f"Watching {'Recursively' if self.watchRecursively else 'Non-Recursively'}: {self.watchPattern}"
            f" -- Folder: {self.watchDirectory} -- Every: {self.watchDelay}(sec) -- For Patterns: {self.exceptionPattern}"
        )
        print(msg)
        self.observer.start()

    def run(self):
        print("Observer is running:", self.observer.name)
        self.start()
        try:
            while True:
                time.sleep(self.watchDelay)

                if self.stop_signal == 1:
                    print(
                        f"Observer stopped: {self.observer.name}  stop signal:{self.stop_signal}")
                    self.stop()
                    break
        except:
            self.stop()
        self.observer.join()

    def stop(self):
        print("Observer Stopped:", self.observer.name)

        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Observer: {self.observer.name} - Stopped On: {now} - Related To Session: {self.sessionid}"
        print(msg)
        self.observer.stop()
        self.observer.join()

    def info(self):
        info = {
            'observerName': self.observer.name,
            'watchDirectory': self.watchDirectory,
            'watchDelay': self.watchDelay,
            'watchRecursively': self.watchRecursively,
            'watchPattern': self.watchPattern,
        }
        return info
    
    
def is_dir_path(path):
    """Utility function to check whether a path is an actual directory"""
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Watchdog script for watching for files & directories' changes")
    # parser.add_argument("path",
    #                     default=config.WATCH_DIRECTORY,
    #                     type=is_dir_path,
    #                     )
    parser.add_argument("-d", "--watch-delay",
                        help=f"Watch delay, default is {config.WATCH_DELAY}",
                        default=config.WATCH_DELAY,
                        type=int,
                        )
    parser.add_argument("-r", "--recursive",
                        action="store_true",
                        help=f"Whether to recursively watch for the path's children, default is {config.WATCH_RECURSIVE}",
                        default=config.WATCH_RECURSIVE,
                        )
    parser.add_argument("-p", "--pattern",
                        help=f"Pattern of files to watch, default is {config.WATCH_PATTERN}",
                        default=config.WATCH_PATTERN,
                        )
    parser.add_argument("--watch-directories",
                        action="store_true",
                        help=f"Whether to watch directories, default is {config.DO_WATCH_DIR}",
                        default=config.DO_WATCH_DIR,
                        )
    # parse the arguments
    args = parser.parse_args()
    # define & launch the log watcher
    log_watcher = LogWatcher(
        watchDirectory=args.path,
        watchDelay=args.watch_delay,
        watchRecursively=args.recursive,
        watchPattern=tuple(args.pattern.split(",")),
        doWatchDirectories=args.watch_directories,
        exceptionPattern=config.EXCEPTION_PATTERN,
    )
    log_watcher.run()