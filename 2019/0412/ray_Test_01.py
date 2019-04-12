#### Basic####
'''
import time
import datetime
def f():
    time.sleep(1)
    return 1


b_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
res = [f() for i in range(20)]
e_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
print(b_date,e_date)
'''


#### Ray####
import time
import datetime
import  ray
@ray.remote
def f():
    time.sleep(1)
    return 1


b_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
ray.init()
res = ray.get([f.remote() for i in range(20)])
e_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
print(b_date,e_date)