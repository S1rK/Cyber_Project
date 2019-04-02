# Tal's Mater Class
# Version 5 - 14.2.19

from threading import Thread
from commands import Commands
from server_v5 import Server
from gui_v5 import GUI
import sys


class Master(object):
    def __init__(self, ip='0.0.0.0', port=8220, save_dir='received\\', debug=False):
        """
        :param ip: the ip of the master
        :param port: the port of the master socket
        :param debug: debug mode (True-on, False-off)
        """
        # create a server
        self.__server = Server(ip=ip, port=port, connection_callback=self.__handle_new_connection,
                               receiving_callback=self.__handle_receiving,
                               disconnect_callback=self.__handle_disconnection, debug=debug)
        # create a gui
        self.__gui = GUI(send_callback=self.__handle_sending, debug=debug)
        # the directory to save all received files
        self.__save_dir = save_dir
        # the number of received files
        self.__file_counter = 0
        # debug mode
        self.__DEBUG = debug

    def __handle_new_connection(self, address):
        """
        Receives from the server a new address that has connected and adding it to the gui.
        :param address: the address of the new client
        :return: nothing, void
        """
        # set the address to be in the format - ip : port
        address = "%s : %s" % (address[0], str(address[1]))
        # add the new address to the gui
        self.__gui.add_connection(address=address)

    def __handle_disconnection(self, address):
        """
        Receives from the server an existing address that has been disconnected and removing it from the gui.
        :param address: the address of the disconnected client
        :return: nothing, void
        """
        # set the address to be in the format - ip : port
        address = "%s : %s" % (address[0], str(address[1]))
        # add the new address to the gui
        self.__gui.remove_connection(address=address)

    def __handle_sending(self, event=None, comboboxes={}, entries=[]):
        """
        Prints the combo-boxes' and entries' values
        :param event: the event - <Button-1>
        :param comboboxes: all the combo-boxes
        :param entries: all the entries
        :return:
        """
        if self.__DEBUG:
            print '------------SEND CALLBACK------------'
        # get the address to send the request
        address = comboboxes['peasant'].get()

        # check if there is an empty address
        if not address:
            # print an error to the gui
            print "ERROR: Empty Address."
            # exit the function - there is no where to send the request
            return

        address = address.split(" ")

        command = comboboxes['command'].get()
        # check if there is an empty command
        if not command:
            print "ERROR: Empty Command."

        # set the address to be in the format of tuple: (str(ip), int(port))
        address = (address[0], int(address[2]))
        # get the command
        command = Commands.command_number(command)
        # get the params
        params = [e.get() for l, e in entries]
        # if debug is on then print them all
        if self.__DEBUG:
            print "DEBUG: sending to <%s : %s> the command %s with those params: %s" % (address[0], str(address[1]), command, params)
        # get the command's number
        command_number = Commands.command_number(command)
        # combine all the arguments to one message to send to the peasant
        data = command_number + Commands.SEPARATE_CHAR.join(params)
        # send the request throw the server
        self.__server.send(address=address, data=data)

    def __handle_receiving(self, address, data):
        """
        Handling receiving data from the
        :param address: the address of the sending client
        :param data: the data the client have sent
        :return: nothing, void
        """
        # if the debug mode is on, print the received data
        if self.__DEBUG:
            print "DEBUG: received form <%s : %s> the following data: %s" % (address[0], address[1], data)
        # separate the data to command number, params and response
        data = data.split(Commands.SEPARATE_CHAR)
        # get the response
        command = data[0:Commands.COMMAND_LENGTH]
        # get the request
        response = data[Commands.COMMAND_LENGTH:]
        # call the handle response
        print "<%s : %s>: %s" % (address[0], address[1], Commands.handle_command_response(command)(response))

    def run(self):
        # set the stdout to be the gui
        sys.stdout = self.__gui

        print >> sys.__stdout__, "changed stdout"
        server_thread = Thread(target=self.__server.open)
        print >> sys.__stdout__, "created server thread"

        # open the server
        server_thread.start()
        print >> sys.__stdout__, "started server thread"

        # run the gui and wait for him to stop
        print >> sys.__stdout__, "starting gui"
        self.__gui.run()
        print >> sys.__stdout__, "gui finished"

        # close the server
        self.__server.close()
        # wait for the server to finish (close)
        print >> sys.__stdout__, "waiting for server thread to stop"
        server_thread.join()
        print >> sys.__stdout__, "server thread stopped"

        # return the normal stdout
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    # create a new master
    master = Master()
    # run the master
    master.run()
