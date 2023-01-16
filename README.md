# auto-commit
Auto-commit and push your code without having to do it yourself all the time

## Getting Started
This is a simple python script that helps in workflow productivity as it automates some easy git operations and file monitoring


### Prerequisites

What things you need to install the software and how to install them.

- pip install watchdog 



### Usage

You must git clone this repository into your working repository because this project is not yet complete. 
If you clone this repository into a subdirectory that you aren't working on, you must provide the directory you want to watch else the code will detect your current directory position and run there.


**To provide a working directory location replace ⬇️**

```python
curr_dir = os.getcwd()
print(curr_dir.replace('\\', '/'))

```


**with this⬇️** 


```python
curr_dir = {your_current_directory_path}
```
**NOTE**: the path must be in forward slashes







