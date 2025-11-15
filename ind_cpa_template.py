#!/usr/bin/env python3

import random
import socket
import threading
import time

SLEEP_TIME = 1
N_CORRECT = 2
FLAG = "FLAG{I love indcpa}"

def encrypt(m):
    """
    TODO: add encryption scheme here
    """
    return m

def choose_bit():
    b = random.random()
    if b < 0.5:
        return 1
    else:
        return 0

def run_game():
    print(f"Lets play a game!\n Choose the correct answer {N_CORRECT} times to win a flag!")
    
    correct_answers = 0
    m0 = ''
    m1 = ''

    while len(m0) < 1 :
        try:
            m0 = input("Set message 0: ")
        except:
            pass

    while len(m1) < 1 :
        try:
            m1 = input("Set message 1: ")
        except:
            pass
    
    while True:
        b = choose_bit()
        if b:
            c = encrypt(m1)
        else:
            c = encrypt(m0)
        print(f"Here is your ciphertext: {c}")
        choice = input("Choose 0 if this ciphertext is from message 0 or 1 for message 1:\n")
        try:
            if int(choice) == b:
                print("Correct!")
                correct_answers += 1
            else:
                print("Wrong! Better luck next time!")
                return
        except:
            print("Wrong! Better luck next time!")
            return
        if correct_answers == N_CORRECT:
            print(f"You got {N_CORRECT} correct! Here's your flag: \n{FLAG}")
            return

def run_game_socketed(conn):
    conn.sendall(f"Lets play a game!\nChoose the correct answer {N_CORRECT} times to win a flag!\n".encode())
    correct_answers = 0

    m0 = b""
    m1 = b""

    while len(m0) < 1 :
        try:
            conn.sendall(b"Set message 0: ")
            m0 = conn.recv(4096).strip()
        except:
            pass
    
    while len(m1) < 1:
        try:
            conn.sendall(b"Set message 1: ")
            m1 = conn.recv(4096).strip()
        except:
            pass
    
    while True:
        time.sleep(SLEEP_TIME)
        b = choose_bit()
        if b:
            c = encrypt(m1)
        else:
            c = encrypt(m0)

        conn.sendall(f"Here is your ciphertext: {c}\n".encode())
        conn.sendall(f"Choose 0 if this ciphertext is from message 0 or 1 for message 1:\n".encode())
        choice = conn.recv(4096).strip()
        try:
            if int(choice) == b:
                conn.sendall("Correct!\n".encode())
                correct_answers += 1
            else:
                conn.sendall("Wrong! Better luck next time!\n".encode())
                return
        except:
            conn.sendall("Wrong! Better luck next time!\n".encode())
            return
        if correct_answers == N_CORRECT:
            conn.sendall(f"You got {N_CORRECT} correct! Here's your flag: \n{FLAG}\n".encode())
            return

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    try: 
        try:
            run_game_socketed(conn)
            conn.close()
            print(f"Closed connection from {addr}")
        except Exception as e:
            print(e)
            conn.close()
            print(f"Closed connection from {addr}")
    except:
        pass

if __name__ == "__main__":
    # TODO: add socket/thread handler that runs game and then closes socket on return
    HOST = "0.0.0.0"   # listen on all interfaces
    PORT = 1234
    print(f"[*] Listening on port {PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            # handle each client in a thread so multiple players can connect
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    # TODO: add socket/thread handler that runs game and then closes socket on return
    run_game()
