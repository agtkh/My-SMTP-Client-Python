#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMTP Client
K.Agata
Created on 2023.10.31
"""
import sys
import socket


class SmtpClient:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))
        res = self.__recv()
        return self.__parse(res)

    def helo(self, hostname):
        self.__send("HELO " + hostname)
        res = self.__recv()
        return self.__parse(res)

    def mail_from(self, from_addr):
        self.__send("MAIL FROM: " + from_addr)
        res = self.__recv()
        return self.__parse(res)

    def rcpt_to(self, to_addr):
        self.__send("RCPT TO: " + to_addr)
        res = self.__recv()
        return self.__parse(res)

    def data(self, message):
        self.__send("DATA")
        self.__recv()
        self.__send(message)
        self.__send(".")
        res = self.__recv()
        return self.__parse(res)

    def quit(self):
        self.__send("QUIT")
        self.__recv()
        self.socket.close()

    def __recv(self):
        msg = self.socket.recv(1024).decode()
        for l in msg.split("\r\n"):
            if len(l):
                print(">> " + l)
        return msg

    def __send(self, msg):
        for l in msg.split("\r\n"):
            print("<< " + l)
        self.socket.sendall((msg + "\r\n").encode())

    def __parse(self, msg):
        temp = msg.split(" ", maxsplit=1)
        status_code = int(temp[0])
        status_msg = temp[1]
        return status_code, status_msg


if __name__ == "__main__":
    try:
        smtp_server_hostname = sys.argv[1]
        smtp_server_port = int(sys.argv[2])
    except (IndexError, ValueError):
        print(f"Usage: {sys.argv[0]} <smtp_server_hostname> <smtp_server_port>")
        sys.exit(1)
    
    from_addr = input("From addr: ")
    to_addr = input("To addr: ")
    subject = input("Subject: ")
    msg = input("Message: ")

    msg_data = f"From: {from_addr}\r\nTo: {to_addr}\r\nSubject: {subject}\r\n\r\n{msg}"

    client = SmtpClient(smtp_server_hostname, smtp_server_port)
    client.connect()
    client.helo(f"<{from_addr}>")
    client.mail_from(f"<{from_addr}>")
    client.rcpt_to(f"<{to_addr}>")
    client.data(msg_data)
    client.quit()
