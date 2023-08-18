#!/usr/bin/env python

import asyncio
import sys
from string import ascii_lowercase, digits as ascii_numbers
import random

def banner():
	print("""
AsyncIO Test Server Applet
Designed to accept TCP connections, assigning an ID number to each connection.
note: has no practical functionalty			       CTRL+C to exit.
--------------------------------------------------------------------------------""")

async def applet(reader, writer):
	id =''.join(random.choices(ascii_lowercase + ascii_numbers, k=8))
	rhost = writer.get_extra_info('peername')[0]

	print("[*] New connection from {} (Conn ID: {})".format(rhost, id))

	# close stream
	writer.close()
	await writer.wait_closed()

async def serverHandler(lport):
	server = await asyncio.start_server(applet, '0.0.0.0', lport)
	print("[+] Server initialized on 0.0.0.0:{}".format(lport))
	async with server:
		await server.serve_forever()

def main():
	if len(sys.argv) != 2:
		print("Usage: {} <LPORT>".format(sys.argv[0]))
		exit(-1)

	lport = 0
	lport = int(sys.argv[1]) if sys.argv[1].isdigit() else 0 # force fail condition

	if lport > 65535 or lport < 1024:
		print("LPORT is invalid. select a port higher than 1023.")
		exit(-1)

	banner()
	try:
		asyncio.run(serverHandler(lport))
	except:
		pass

	print("\r[!] Closing applet!")

if __name__ == '__main__':
	main()
	exit(0)
