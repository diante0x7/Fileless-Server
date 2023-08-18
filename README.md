# Fileless-Server
A test project utilizing Asyncio and Threading to perform basic admin operations and receive data from multiple sockets.

*developed in this order: test_serv.py -> servUI.py -> better_servui.py*
## Features
Currently, the fileless-server can receive data from an unlimited number of hosts over a tcp socket with an interactive administration tool capable of the following:
### List
This command performs a listing operation, printing the IDs and remote addresses of each socket connection.
### Kill
This command queue's up a socket closing operation by setting the killID value to one that belongs to an active connection. This is a way to control the data flow when the ability to disconnect on the remote host is not possible or you would like to end it yourself.
### BlacklistManager
The server comes equipped with an internal blacklist manager that currently has the ability to add an IP to the blacklist or remove a value if it's already present. The server applet has the ability to query the blacklist once an incoming connection is initialized, killing it if it fails the check.
## Outro
This was a learning experience dedicated to strengthening my ability to write asynchronous and multi-threaded applications while also practicing my skills relative to developing useful applications. As of right now there is not much of a practical usage and it could be (and will likely be, in the future) better written while having more features. It is, however, an opportunity to generate new ideas and allow myself a greater understanding of how such applications interact within each other and with external connections!
