# Tal's Commands Class
# Version 6 - 14.2.19

import os
import subprocess
from shutil import copy
from PIL import ImageGrab
import win32com.client as cl


class Commands(object):
    """-----------------THE COMMAND DICTIONARY-----------------"""
    @staticmethod
    def __commands():
        """
        The commands in the format of - command's name : (command's function, command's parameters)
        :return:
        """
        return {'Take Screen Shot': (Commands.__take_screenshot_request, Commands.__print_reponse, []),
                'Download File': (Commands.__send_file_request, Commands.__send_file_reponse, ['File Name']),
                'Dir': (Commands.__dir_request, Commands.__print_reponse, []),
                'Delete File': (Commands.__delete_request, Commands.__print_response, ['File Name']),
                'Copy File': (Commands.__copy_request, Commands.__print_response, ['Source', 'Destination']),
                'Execute': (Commands.__execute_request, Commands.__print_reponse, ['Executable File']),
                'Text To Speech': (Commands.__text_to_speech_request, Commands.__print_response, ['The Text To Say']),
                'Disconnect': (Commands.__disconnect_request, Commands.__print_response, [])}

    """-----------------THE CONSTS-----------------"""
    # the number of digits the length of the messages sending
    SIZE_LENGTH = 10
    # the number of digits the length of a command
    COMMAND_LENGTH = 1
    # the special character that separates params' elements and command number
    SEPARATE_CHAR = '|'
    # the number of images taken
    __image_number = 0
    # indexes in the dictionary
    __REQUEST_INDEX = 1
    __RESPONSE_INDEX = 1
    __PARAM_INDEX = 1

    """-----------------COMMANDS REQUESTS HANDLERS-----------------"""

    @staticmethod
    def __take_screenshot_request(socket):
        # get the picture name
        picture_name = ""
        # take a screen shot
        im = ImageGrab.grab()
        # if there is no given name to the image
        if picture_name == "":
            # set the image's name to be image + image number
            picture_name = "images%d" % Commands.__image_number
            # increase the number of images
            Commands.__image_number += 1
        # save the image with the image name as a png image
        im.save(picture_name+".png", "PNG")
        # return "saved at " + the picture's name
        return "Saved at " + str(picture_name)

    @staticmethod
    def __copy_request(src, dest):
        copy(src, dest)
        return 'Copied %s to %s' % (str(src), str(dest))

    @staticmethod
    def __execute_request(to_execute):
        subprocess.call(to_execute)
        return 'Executed %s' % str(to_execute)

    @staticmethod
    def __delete_request(to_delete):
        os.remove(to_delete)
        return 'Deleted %s' % str(to_delete)

    @staticmethod
    def __dir_request(directory):
        files_list = os.listdir(directory)
        return files_list

    @staticmethod
    def __send_file_request(file_name):
        # get the file's data as binary data
        with open(file_name, "rb") as f:
            data = f.read()
        # get the file's type
        typ = file_name[:file_name.rfind('.')]
        # return : {file's type}{separate char}{data}
        return typ + Commands.SEPARATE_CHAR + data

    @staticmethod
    def __text_to_speech_request(text):
        sp = cl.Dispatch("SAPI.SpVoice")
        sp.Speak(text)
        return 'Said "%s"' % text

    @staticmethod
    def __disconnect_request():
        return 'Bye bye'

    @staticmethod
    def __print_response(response):
        print response

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
        return tuple(Commands.__commands().keys())

    @staticmethod
    def handle_command_request(command_number, *args):
        """
        :param command_number: the command's number
        :param args: a list of arguments to the command's request handler
        :return: the command's request return value
        """
        commands = Commands.__commands()
        return commands[commands.keys()[command_number]][Commands.__REQUEST_INDEX](*args)

    @staticmethod
    def handle_command_response(command_number, *args):
        """
        :param command_number: the command's number
        :param args: a list of arguments to the command's response handler
        :return: the command's response return value
        """
        commands = Commands.__commands()
        return commands[commands.keys()[command_number]][Commands.__RESPONSE_INDEX](*args)

    @staticmethod
    def get_commands_parameters(command_name):
        """
        Returns the command's parameters
        :param command_name: the command's name
        :return: the given command's parameters
        """
        return Commands.__commands()[command_name][Commands.__PARAM_INDEX]

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
