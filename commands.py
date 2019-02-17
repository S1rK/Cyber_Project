# Tal's Peasant Class

import os
import subprocess
from shutil import copy
from PIL import ImageGrab


class Commands(object):
    # the number of digits the length of the messages sending
    SIZE_LENGTH = 10
    # the special character that separates params' elements and command number
    SEPARATE_CHAR = '|'
    # the number of images taken
    __image_number = 0

    @staticmethod
    def pad_length(length):
        """
        :param length: the request's length we want to send to the client
        :return: returns the length, in string, padded with 0 at the start
        """
        length = str(length)
        while len(length) < Commands.SIZE_LENGTH:
            length = "0" + length
        return length

    @staticmethod
    def __commands():
        """
        The commands in the format of - command's name : (command's function, command's parameters)
        :return:
        """
        return {'TAKE_SCREENSHOT': (Commands.take_screenshot_command, []),
                'SEND_FILE': (Commands.send_file_command, ['File Name']),
                'DIR': (Commands.dir_command, []),
                'DELETE': (Commands.delete_command, ['File Name']),
                'COPY': (Commands.copy_command, ['Source', 'Destination']),
                'EXECUTE': (Commands.execute_command, ['Executable File']),
                'EXIT': (Commands.exit_command, [])}

    @staticmethod
    def take_screenshot_command(picture_name=""):
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
        return "saved at " + str(picture_name)

    @staticmethod
    def copy_command(src, dest):
        copy(src, dest)
        return 'copied %s to %s' % (str(src), str(dest))

    @staticmethod
    def execute_command(to_execute):
        subprocess.call(to_execute)
        return 'Executed %s' % str(to_execute)

    @staticmethod
    def delete_command(to_delete):
        os.remove(to_delete)
        return 'Deleted %s' % str(to_delete)

    @staticmethod
    def dir_command(directory):
        files_list = os.listdir(directory)
        return files_list

    @staticmethod
    def send_file_command(file_name):
        # get the file's data as binary data
        with open(file_name, "rb") as f:
            data = f.read()
        # get the file's type
        typ = file_name[:file_name.rfind('.')]
        # return : {file's type}{separate char}{data}
        return typ + Commands.SEPARATE_CHAR + data

    @staticmethod
    def exit_command():
        return 'Bye bye'

    @staticmethod
    def get_commands():
        """
        :return: a dictionary between command's name and their functions
        """
        return {k: v[0] for k, v in Commands.__commands()}

    @staticmethod
    def get_commands_parameters(command):
        """
        Returns the command's parameters
        :param command: the command
        :return: the given command's parameters
        """
        return Commands.__commands()[command][1]

    @staticmethod
    def get_commands_names():
        """
        :return: the commands' names
        """
        return Commands.__commands().keys()
