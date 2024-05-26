import socket, threading, time


def accept_client():
    while True:
        #accept    
        cli_sock, cli_add = ser_sock.accept()
        uname = cli_sock.recv(1024).decode()
        #accept the public key
        CONNECTION_LIST.append((uname, cli_sock))
        q=cli_sock.recv(1024).decode()
        h=cli_sock.recv(1024).decode()
        g=cli_sock.recv(1024).decode()
        print("\nq received "+q)
        print("\nh receiced "+h)
        print("\ng received "+g)
        publicKey.append((uname,q,h,g))
        #first user connected
        if(len(publicKey)==1):
            #no previous user 	
            cli_sock.send(bytes(str(-1),'utf-8'))
        #second user connected
        elif(len(publicKey)>1):
            #sending the public key of previous user to new user
            cli_sock.send(bytes("protocol100",'utf-8'))
            time.sleep(0.3)
            cli_sock.send(bytes(publicKey[0][0],'utf-8'))
            time.sleep(0.3)
            cli_sock.send(bytes(publicKey[0][1],'utf-8'))
            time.sleep(0.3)
            cli_sock.send(bytes(publicKey[0][2],'utf-8'))
            time.sleep(0.3)
            cli_sock.send(bytes(publicKey[0][3],'utf-8'))
            
            #sending the public key of new user to existing user
            CONNECTION_LIST[0][1].send(bytes("protocol100",'utf-8'))
            time.sleep(0.3)
            CONNECTION_LIST[0][1].send(bytes(uname,'utf-8'))
            time.sleep(0.3)
            CONNECTION_LIST[0][1].send(bytes(q,'utf-8'))
            time.sleep(0.3)
            CONNECTION_LIST[0][1].send(bytes(h,'utf-8'))
            time.sleep(0.3)
            CONNECTION_LIST[0][1].send(bytes(g,'utf-8'))
            
        
        print('%s is now connected' %uname)
        thread_client = threading.Thread(target = broadcast_usr, args=[uname, cli_sock])
        thread_client.start()

def broadcast_usr(uname, cli_sock):
    while True:
        try:
            protocol=cli_sock.recv(1024).decode()
            if protocol=="protocol101":
                print("{0} spoke".format(uname))
                p=cli_sock.recv(1024)
                #print("p received")
                l=int(cli_sock.recv(1024).decode())
                #print("message of size "+str(l))
                received_msg=[]
                for i in range(l):
                    characterOfMsg=cli_sock.recv(1024).decode()
                    received_msg.append(characterOfMsg)
                print(received_msg)
                b_usr(cli_sock, uname,p, received_msg)
        except Exception as x:
            print(x.message)
            break

def b_usr(cs_sock, sen_name, p,received_msg):
    for client in CONNECTION_LIST:
        if client[1] != cs_sock:
            #received msg in array of string
            #p is in bytes format
            #sen_name is in string format
            
            #sending the protocol name
            #print("sending")
            client[1].send(bytes("protocol101",'utf-8'))
            time.sleep(0.3)
            #sending username of sender
            client[1].send(bytes(sen_name,'utf-8'))
            time.sleep(0.3)
            #sending p
            client[1].send(p)
            time.sleep(0.3)
            #sending the length of message
            client[1].send(bytes(str(len(received_msg)),'utf-8'))
            #sending the encrypted message
            for i in received_msg:
                time.sleep(0.3)
                client[1].send(bytes(i,'utf-8'))
                
            

if __name__ == "__main__":    
    CONNECTION_LIST = []
    publicKey=[]
    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 9999
    ser_sock.bind((HOST, PORT))

    # listen    
    ser_sock.listen(1)
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target = accept_client)
    thread_ac.start()

    #thread_bs = threading.Thread(target = broadcast_usr)
    #thread_bs.start()

