import random

word_dict = {}
with open('commit_text.txt', 'r') as file:
    lines = file.readlines()
for line in lines:
    line = line.strip() # remove trailing whitespaces
    if line in word_dict:
        word_dict[line] += 1
    else:
        word_dict[line] = 1

print(random.choice(list(word_dict.keys())))
