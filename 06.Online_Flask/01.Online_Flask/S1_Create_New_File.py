import datetime
with open('printtext.txt', 'a+') as f:
	print('Thoi gian hien tai la:',datetime.datetime.now(), file= f)

##--------------------------------------
from time import sleep

your_name = "Henry"
your_great = "Hello! My name is "

for c in your_great + your_name:
    print(c, end='', flush=True)
    sleep(0.5)
print()