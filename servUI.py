import asyncio
from datetime import datetime
import sys

def banner():
	print("""
AsyncIO Test Server Applet w Interface
Designed to accept TCP connections, assign an ID and List IPs.
note: has no practical functionalty			       CTRL+C to exit.
--------------------------------------------------------------------------------""")

serverlist = []

def list_socks():
     global serverlist
     for i in range(len(serverlist)):
        print("[{}] {}".format(i, serverlist[i]))

def list_help():
    print("[*] SYSTEM: HELP")
    print("<list>\tList all connections and their IP address.")
    print("<help>\tPresent this help screen.")

def interactive():
    opt = ''
    while opt not in ['q', 'quit', 'exit']:
        opt = input("serverlet> ")
        match opt.lower():
            case 'help':
                list_help()
            case 'list':
                list_socks()
            case _:
                print("[!] APP: Invalid option. Please check your input, then try again.")
    print("[!] SYSTEM: Quitting! CTRL+C TO CLOSE.")
    return
    #exit(0)
    
def application():
    try:
        interactive()
    except KeyboardInterrupt:
        return

async def applet(reader, writer):
        global serverlist
        id = len(serverlist)
        rhost = writer.get_extra_info('peername')[0]
        serverlist.append(rhost)

        print("\r[*] SYSTEM: New connection from {} (Conn ID: {})".format(rhost, id))

        msg = ''
        while msg != 'kill':
            try:
                msg = await reader.readline()
                msg = msg.decode('utf-8').strip('\n')
                writer.write(b"ACK\n")
                await writer.drain()
                print("\r[+] INFO: {} says {} <{}>".format(id, msg, datetime.now()))
            except:
                msg = 'kill'

        print("\r[-] INFO: Connection ID={} from {} closed.".format(id, serverlist[id]))
        serverlist.pop(id)
        writer.close()
        try:
            await writer.wait_closed()
        except:
             pass

async def main():
    lport = sys.argv[1]
    loop = asyncio.get_running_loop()
    
    server = await asyncio.start_server(applet, '0.0.0.0', lport)
    print("[+] SYSTEM: Server initialized on 0.0.0.0:{}".format(lport))

    loop.create_task(asyncio.to_thread(application))

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    banner()
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
         exit(0)