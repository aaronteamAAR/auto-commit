import asyncio
import os
from watchfiles import awatch, Change, DefaultFilter, watch




directory = 'C:/Users/Last Hokage/Documents/auto-commit'

class WebFilter(DefaultFilter):
    allowed_extensions = '.html', '.css', '.js'

    def __call__(self, change: Change, path: str) -> bool:
        return (
            super().__call__(change, path) and
            path.endswith(self.allowed_extensions)
        )

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
    if os.path.isfile(f):
       print(f)



def main():
     for changes in watch(f):
         print(changes)

 
asyncio.run(main())