import datetime, re
from pygtail import Pygtail



class FileChecker:
    
    def __init__(self, expectionPattern) -> None:
        self.expectionPattern = expectionPattern
        
        
    def checkForException(self, event, path):
        now = (datetime.datetime.now()).strftime("%H:%M:%S")
        
        for num, line in enumerate(Pygtail(path), 1):
            line = line.strip()
            
            
            if line and any(re.findall('|'.join(self.expectionPattern), line, flags=re.I | re.X)):
                   type = 'observation'
                   message = f"{now} -- {event.event_type} -- src => {path} -- focus: {line}" 
                   yield type, message
            elif line:
                type = 'msg'
                message = f"{now} -- {event.event_type} -- src => {path}"
                yield type, message  