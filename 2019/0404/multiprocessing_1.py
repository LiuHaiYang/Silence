# multiprocessing.py
import os

print('Process (%s) start...' % os.getpid())
pid = os.fork()
if pid==0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

'''
Process (38198) start...
I (38198) just created a child process (38202).
I am child process (38202) and my parent is 38198.
'''