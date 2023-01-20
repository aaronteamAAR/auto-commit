import subprocess, click
import os, time, datetime
import logging
from halo import Halo
from git import Repo
from git.exc import InvalidGitRepositoryError
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

# Get directory location 

curr_dir = os.getcwd()
print(curr_dir.replace('\\', '/'))

directory = curr_dir

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



# i want to take the path to a file as an argument 
# i want to take the number of chnages as an argument 
# i want to take  an argumnet to ask user wether to push auto or not  


PUSHES=dict(ap="autoPush", mp="manualPush")


@click.group()

def main():
    pass




@click.command()
@click.option("-i", "--init", prompt="initalize empty git repo", help="set to initalize an empty git repo", default=False)
def git_init(init):
    spinner = Halo(text='working on it', spinner='dots')
    spinner.start()
    if type(init) == bool and init == True:
        try:
            repo_dir = curr_dir
            repo = Repo.init(repo_dir)
        except InvalidGitRepositoryError as e:
            print(f"Error: {e}")
        time.sleep(3)
        print("\nthanks")
        spinner.stop()
    else:
        print("hey")
        

@click.command()
@click.option("--branch_name", "-b", required=True, help="Name of the branch to create")
@click.option("--remote", "-r", required=True, help="Name of the remote to push to")
def create_branch(branch_name, remote):
    repo = Repo()
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()
    repo.remotes[remote].push(new_branch.name)
    click.echo(f"Successfully created and pushed branch {branch_name} to remote {remote}.")


@click.command()
@click.option("-p", "--push", prompt="Set to auto-push || manual-push", type=click.Choice(PUSHES.keys()), help="Select to auto push or not!", default=PUSHES['mp'])
def push_type(push):

    if push == "mp":
        print("Good, your code won't auto push itself")
    else:
      print("Your code will now auto-push after a few number of file changes!")
      subprocess.run(['git', 'push', 'origin', f'{branch}'], check=True)


@click.command()
@click.option("--num_changes", "-n", type=int, required=True, help="Number of changes to make to occur for each commit session")
def file_changes(changes):
    num_changes = changes
    change = 0
    changes += 1
    try:
        if changes >= num_changes:
            with open("commit_text.txt", "r") as f:
                  contents = f.read()
                    # split the contents into words
                  words = contents.split()
                    # create an empty dictionary to store the words
                  word_count = {}
                    # iterate through the words and add them to the dictionary
                  for word in words:
                        if word in word_count:
                            word_count[word] += 1
                        else:
                            word_count[word] = 1
                        print(word_count)

    except subprocess.CalledProcessError as e:
        print(f"Git push error with changes to : {e}, try to resolve this manually")
        changes = 0
    

main.add_command(push_type)
main.add_command(git_init)
main.add_command(create_branch)
main.add_command(file_changes)


if __name__ == "__main__":
     main()