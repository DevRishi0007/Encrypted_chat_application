import socket, threading, time


###encryption

import random
from math import pow

a = random.randint(2, 10)


def gcd(a, b):
	if a < b:
		return gcd(b, a)
	elif a % b == 0:
		return b
	else:
		return gcd(b, a % b)

# Generating large random numbers
def gen_key(q):
	key = random.randint(pow(10, 20), q)
	while gcd(q, key) != 1:
		key = random.randint(pow(10, 20), q)

	return key

# Modular exponentiation
def power(a, b, c):
	x = 1
	y = a

	while b > 0:
		if b % 2 != 0:
			x = (x * y) % c
		y = (y * y) % c
		b = int(b / 2)

	return x % c

# Asymmetric encryption
def encrypt(msg, q, h, g):
	localq=int(q)
	localh=int(h)
	localg=int(g)
	en_msg = []

	k = gen_key(localq)# Private key for sender
	s = power(localh, k, localq)
	p = power(localg, k, localq)
	
	for i in range(0, len(msg)):
		en_msg.append(msg[i])

	
	for i in range(0, len(en_msg)):
		en_msg[i] = s * ord(en_msg[i])

	return en_msg, p

def decrypt(en_msg, p, key, q):

	dr_msg = []
	h = power(p, key, q)
	for i in range(0, len(en_msg)):
		dr_msg.append(chr(int(int(en_msg[i])/h)))
		
	return dr_msg



###
def send():
    while True:
        msg = input('\nMe > ')
        l=len(msg)
        encrypted_msg,p=encrypt(msg,sen_q,sen_h,sen_g)
        #
        #print("p generarted = "+str(p))
        cli_sock.send(bytes("protocol101",'utf-8'))
        time.sleep(0.3)
        #sending p
        cli_sock.send(bytes(str(p),'utf-8'))
        time.sleep(0.3)
        #sending length of the message
        cli_sock.send(bytes(str(l),'utf-8'))
        
        for i in range(l):
            time.sleep(0.3)
            cli_sock.send(bytes(str(encrypted_msg[i]),'utf-8'))
    #end

        
        

def receive():
    while True:
        receive=(cli_sock.recv(1024)).decode()
        if(receive=="protocol100"):
            #new user connected , recieve the public key for new user
            global sen_name,sen_q,sen_h,sen_g
            sen_name = cli_sock.recv(1024).decode()
            sen_q=int(cli_sock.recv(1024).decode())
            sen_h=int(cli_sock.recv(1024).decode())
            sen_g=int(cli_sock.recv(1024).decode())
            print("public key of "+sen_name+" received")
            print("q = "+str(sen_q))
            print("h = "+str(sen_h))
            print("g = "+str(sen_g))
            continue
        elif(receive == "protocol101"):
            #print("message form server protocol 101")
            sen_name=(cli_sock.recv(1024)).decode()
            p=int((cli_sock.recv(1024)).decode())
            #print("p received "+str(p))
            l=int((cli_sock.recv(1024)).decode())
            #print("l received "+str(l))
            encrypted_msg=[]
            for i in range(l):
                temp=int((cli_sock.recv(1024)).decode())
                encrypted_msg.append(temp)
            #print("\nafter l")
            #print(encrypted_msg)
            dr_msg = decrypt(encrypted_msg, p, key, q)
            dmsg = ''.join(dr_msg)
            print('\n' + str(sen_name) + ' > ' + str(dmsg))
    	
        
    	
    	
    	
    	

if __name__ == "__main__":   
    
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #encryption (generating public and private keys)
    q = random.randint(pow(10, 20), pow(10, 50))
    g = random.randint(2, int(q))
    key = gen_key(int(q))# Private key of user
    h = power(g, key, q)
    
    
    
    # connect
    HOST = 'localhost'
    PORT = 9999
    cli_sock.connect((HOST, PORT))     
    print('Connected to remote host...')
    uname = input('Enter your name to enter the chat > ')
    
    #sending the username to server
    cli_sock.send(bytes(uname, 'utf-8'))
    #sending public key to server
    time.sleep(0.3)
    cli_sock.send(bytes(str(q),'utf-8'))
    time.sleep(0.3)
    cli_sock.send(bytes(str(h),'utf-8'))
    time.sleep(0.3)
    cli_sock.send(bytes(str(g),'utf-8'))
    
    print("my public keys are:\n q:"+str(q)+"\nh:"+str(h)+"\ng:"+str(g))
    #print("\nkey:"+str(key))
    
    #sen_name=0
    sen_q=0
    sen_h=0
    sen_g=0
    
    
    #recieve the public key list and the list of user
    flag=(cli_sock.recv(1024)).decode()
    #if flag="protocol100" server has another user so receive their public key
    #in case the user is the first to connect server send value -1
    #else user is the first to connect 
    if(flag=="protocol100"):
        sen_name = cli_sock.recv(1024).decode()
        sen_q=int(cli_sock.recv(1024).decode())
        sen_h=int(cli_sock.recv(1024).decode())
        sen_g=int(cli_sock.recv(1024).decode())
        print("public key of "+sen_name+"  received")
        print("q = "+str(sen_q))
        print("h = "+str(sen_h))
        print("g = "+str(sen_g))
    	
    
    
    
    #
    thread_send = threading.Thread(target = send)
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()