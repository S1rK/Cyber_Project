# Tal's Mater Class
# Version 5 - 14.2.19

import socket
from time import sleep
from select import select
from commands import Commands


class Server(object):
    def __default_connection_callback(self, address):
        if self.__DEBUG:
            print('--------DEFAULT CONNECTION CALLBACK--------')
        print "new connection from: <%s : %d>" % (address[0], address[1])

    def __default_receiving_callback(self, address, data):
        if self.__DEBUG:
            print('--------DEFAULT RECEIVING CALLBACK--------')
        print "received from client: <%s : %s>" % (address[0], address[1])
        print "data: %s" % data

    def __default_disconnect_callback(self, address):
        if self.__DEBUG:
            print
        print "<%s : %s> has disconnected" % (address[0], address[1])

    def __init__(self, ip='0.0.0.0', port=8220, connection_callback=None, receiving_callback=None, disconnect_callback=None, debug=False):
        """
        :param ip: the ip of the master
        :param port: the port of the master socket
        :param connection_callback: a callback function to call when there is a new connection
        :param receiving_callback: a callback function to call when there is a new received data
        :param disconnect_callback: a callback function to call when a client has been disconnected
        :param debug: debug mode (True-on, False-off)
        """
        # open a TCP\IP socket, and bind it to the given ip and port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((ip, port))
        # if the server is closed
        self.__closed = False
        # a dict of the connected clients - (address : socket)
        self.__connected = {}
        # a list of address and data to send to them - (address, data)
        self.__to_send = []
        # a function to call when receiving a new connection
        self.__connection_callback = self.__default_connection_callback if connection_callback is None \
            else connection_callback
        # a function to call when receiving new data
        self.__receiving_callback = self.__default_receiving_callback if receiving_callback is None \
            else receiving_callback
        self.__disconnect_callback = self.__default_disconnect_callback if disconnect_callback is None \
            else disconnect_callback
        # a counter of how many requests sent and how many responses received
        self.__counter = 0
        # debug mode
        self.__DEBUG = debug

    def __get_address_by_socket(self, sock):
        """
        :param sock: a socket we want to know it's ip
        :return: Returns the address of a socket
        """
        return self.__connected.keys()[self.__connected.values().index(sock)]

    def __handle_sending(self, wlist):
        # copy the requests list
        to_send = self.__to_send
        # go over the requests (socket, request)
        for element in to_send:
            # get the socket to send the data to
            sock, data = element
            # if can send the request to the socket
            if sock in wlist:
                # send to the socket the request
                self.__send_to_socket(sock, data)
                # remove the request from the requests list
                if element in self.__to_send:
                    self.__to_send.remove(element)

    def __handle_receiving(self, rlist):
        # go over every socket we can receive from
        for s in rlist:
            # if it's the server socket - accept new connection
            if s is self.__socket:
                # get the new socket and address (address is a tuple of ip and port)
                (new_socket, address) = self.__socket.accept()
                # add the new client to the open sockets list
                self.__connected[address] = new_socket
                # call the new connection callback
                self.__connection_callback(address)
            else:
                # get the address of the sending client
                address = self.__get_address_by_socket(s)
                # get the response from the socket
                response = self.__recv_from_socket(s)
                # if the client disconnected
                if response == 'EXIT':
                    self.__disconnect_callback(address)
                else:
                    # send to the receiving callback function the address of the sending client and the response he sent
                    self.__receiving_callback(address, response)

    def __send_to_socket(self, sock, data):
        """
        Sends the data to the given socket. First the length of the data
        (DATA_LENGTH digits), and then the data itself.
        :param s: the socket to send the data to
        :param data: the data we want to send to the socket
        :return: if succeeded.
        """
        # TODO: ENCRYPT
        # get the data's length
        data_len = Commands.pad_length(len(data))
        # send the whole message - length and then the data itself
        sock.send(data_len + data)
        # if DEBUG MODE on then print the data we sent
        if self.__DEBUG:
            address = self.__get_address_by_socket(sock)
            print "Sent to <%s : %s> the following command:\n%s" % (address[0], address[1], data)
        # return true
        return True

    def __recv_from_socket(self, s):
        """
        Gets a data from the given socket. First the length of the data
        (DATA_LENGTH digits), and then the data itself.
        :param s: the socket to get the data from
        :return: the data got from the socket
        """
        # decrease the counter
        self.__counter -= 1
        # get the socket address
        address = self.__get_address_by_socket(s)
        # get the data's length
        length = s.recv(Commands.SIZE_LENGTH)
        # if the socket is closing the connection
        if not length:
            if self.__DEBUG:
                print "<%s : %s> has disconnected" % (address[0], address[1])
            # delete the socket from the connected dictionary
            del self.__connected[self.__get_address_by_socket(s)]
            # close the socket
            s.close()
            # return the exit command
            return "EXIT"
        # else, there is data. convert the length to int
        length = int(length)
        # get the data itself
        data = s.recv(length)
        # TODO: DECRYPT
        # if DEBUG MODE on then print the data we got
        if self.__DEBUG:
            print "Got the following response from <%s : %s>:\n%s" % (address[0], str(address[1]), data)
        # return the data we got
        return data

    def get_address(self):
        """
        :return: the ips' of the connected clients
        """
        return self.__connected.keys()

    def open(self):
        """
        Opens the socket, receiving clients and handling them, until the server is closed.
        :return: nothing, void
        """
        import sys
        print >> sys.__stdout__, "YES?"
        # open the socket to listen up to 5 connections
        self.__socket.listen(5)
        # a counter to print while's parameters
        counter = 0
        # loop until the user requested to exit and finished receiving responses
        while not (self.__closed and self.__counter == 0):
            # get the list of the sockets we can read form and send to
            rlist, wlist, xlist = select([self.__socket] + self.__connected.values(), self.__connected.values(), [])
            # handle the sockets we can receive from
            self.__handle_receiving(rlist)
            # handle the sockets we can write to
            self.__handle_sending(wlist)
            # if the debug mode is on
            if self.__DEBUG:
                # increase the counter
                counter = (counter+1) % 10**5
                # if the counter is 0
                if not counter:
                    # print the while's parameters
                    print "CLOSED: %s, COUNTER: %d" % (str(self.__closed), self.__counter)
        # if the debug mode is on, then print information
        if self.__DEBUG:
            print "Finished main loop. Closing sockets"
        # close all the clients' sockets and the server's socket
        for peasant in self.__connected.values():
            peasant.close()
        self.__socket.close()
        self.__socket = None
        # if the debug mode is on, then print information
        if self.__DEBUG:
            print "Finished Server.open function - closed all sockets"

    def send(self, address, data):
        """
        Add a data to send to a specific ip.
        :param address: the address of the client to send the data to
        :param data: the data to send
        :return: nothing, void
        """
        # get the socket to send to
        sock = self.__connected[address]
        # add the socket and data to the 'to_send' list
        self.__to_send.append((sock, data))

    def is_open(self):
        """
        :return: if the server is open
        """
        return not self.__closed

    def close(self):
        """
        Set the server to close
        :return: nothing, void
        """
        self.__closed = True


if __name__ == '__main__':
    from threading import Thread
    # create a new master
    server = Server(port=8220, debug=True)
    # run the master
    t = Thread(target=server.open)
    print 'staring open thread'
    t.start()
    sleep(30)
    print '************\tsent the first client message\t************'
    server.send(server.get_address()[0], "hi there")
    sleep(10)
    print '************\tset to close server\t************'
    server.close()
    print '************\twaiting for server to close\t************'
    t.join()
    print "FIN"
