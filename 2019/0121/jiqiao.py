# 1. 字典推导(Dictionary comprehensions)和集合推导(Set comprehensions)
some_list = [1,2,3,4,5]
another_list = [x+1 for x in some_list]
print(another_list)

some_list_1 = [1,2,3,4,5,2,3,4,6,8]
event_set = {x for x in some_list if x % 2 ==0 }
print(event_set)


d = { x: x % 2 == 0 for x in range(1, 11) }
print(d)

from collections import Counter
c = Counter('hello world')

print(c)

print(c.most_common(2))

import json
data= {"status": "OK", "count": 2, "results": [{"age": 27, "name": "Oz", "lactose_intolerant": "true"}, {"age": 29, "name": "Joe", "lactose_intolerant": "false"}]}

print(json.dumps(data))

print(json.dumps(data, indent=2))  # With indention
