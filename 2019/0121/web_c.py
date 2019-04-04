import xmlrpclib
proxy = xmlrpclib.ServerProxy('http://localhost:8000/')

proxy.file_reader('/tmp/secret.txt')