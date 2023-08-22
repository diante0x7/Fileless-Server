import asyncio
from datetime import datetime
import sys

def banner():
	print("""
AsyncIO Test Server Applet w Interface
ServUI.py featuring a close connection function and an internal, fileless blacklist.
note: can be adapted to run as a central server for receiving data	       CTRL+C to exit.
--------------------------------------------------------------------------------""")

# globals
serverlist = []
blacklist = []
killID = -1

def list_socks():
     global serverlist
     for i in range(len(serverlist)):
        print("[{}] {}".format(i, serverlist[i]))

def list_help():
    print("[*] APP: HELP")
    print("<blacklist>\tManage the server's blacklist.")
    print("\t<set> Add an IP address to the blacklist.")
    print("\t<remove> Remove an IP address to the blacklist.")
    print("\t<list> List all IP addresses in the blacklist.")
    print("<kill>\tKill connection based on ID.")
    print("<list>\tList all connections and their IP address.")
    print("<help>\tPresent this help screen.")

def blacklistManager(rhost, opt='get'):
    global blacklist

    match opt:
        case 'set':
            blacklist.append(rhost)
            return True
        case 'remove':
            try:
                blacklist.remove(rhost)
                return True
            except:
                return False
        case 'get':
            if rhost in blacklist:
                return True
            return False
        case _:
            return False

def conn_status(id, opt='get'):
    global killID
    global serverlist
    if opt == 'set':
        if id not in range(len(serverlist)): 
            return False
        killID = id
        return True
    
    if id == killID:
        killID = -1
        return False
    return True
    

def interactive():
    opt = ''
    while opt not in ['q', 'quit', 'exit']:
        opt = input("serverlet> ")
        match opt.lower():
            case 'blacklist':
                blacklist_opt = input("blackist> ")
                match blacklist_opt.lower():
                    case "set":
                        blacklist_ip = input("blacklist:set> ")
                        blacklistManager(blacklist_ip, "set")
                        print("[+] APP: Adding IP {} to the blacklist.".format(blacklist_ip))
                    case "remove":
                        blacklist_ip = input("blacklist:remove> ")
                        if blacklistManager(blacklist_ip, "remove"):
                            print("[+] APP: Removing IP {} from the blacklist.".format(blacklist_ip))
                        else:
                            print("[!] APP: IP is not present in the blacklist.")
                    case _:
                        print("[!] APP: Invalid option. Please check your input, then try again.")
            case 'kill':
                kill_id = input("kill> ")
                if conn_status(int(kill_id), "set"):
                    print ("[+] APP: Killing connection ID: {}".format(kill_id))
                else:
                    print("[!] APP: ID does not exist. Please check your input or run <list>, then try again.")
            case 'help':
                list_help()
            case 'list':
                list_socks()
            case '': # makes the invalid option less annoying by allowing empty [enter]/'\n' inputs
                pass
            case _:
                print("[!] APP: Invalid option. Please check your input, then try again.")
    print("[!] APP: Quitting! CTRL+C TO CLOSE.")
    return
    #exit(0)
    
def application():
    try:
        interactive()
    except KeyboardInterrupt:
        return

async def applet(reader, writer):
        global serverlist, blacklist
        id = len(serverlist)
        rhost = writer.get_extra_info('peername')[0]
        serverlist.append(rhost)

        if rhost in blacklist:
            print("\r[!] SYSTEM: BLACKLISTED IP ATTEMPTED TO CONNECT: {} <{}>".format(rhost, datetime.now()))
            writer.close()
            await writer.wait_closed()
            return

        print("\r[*] SYSTEM: New connection from {} (Conn ID: {})".format(rhost, id))

        msg = ''
        while msg != 'kill':
            try:
                if not conn_status(id): 
                    raise BaseException # force exception
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
        return

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

    if len(sys.argv) != 2:
        print("[!] SYSTEM: Improper command...")
        print("usage: {} <LPORT>".format(sys.argv[0]))
        exit(-1)
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
         exit(0)
