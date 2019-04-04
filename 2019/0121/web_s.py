'''
创建一次性的、快速的小型web服务
有时候，我们需要在两台机器或服务之间做一些简便的、很基础的RPC之类的交互。我们希望用一种简单的方式使用B程序调用A程序里的一个方法——有时是在另一台机器上。仅内部使用。

我并不鼓励将这里介绍的方法用在非内部的、一次性的编程中。我们可以使用一种叫做XML-RPC的协议 (相对应的是这个Python库)，来做这种事情。

下面是一个使用SimpleXMLRPCServer模块建立一个快速的小的文件读取服务器的例子：
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer

def file_reader(file_name):

    with open(file_name, 'r') as f:
        return f.read()

server = SimpleXMLRPCServer(('localhost', 8000))
server.register_introspection_functions()

server.register_function(file_reader)

server.serve_forever()