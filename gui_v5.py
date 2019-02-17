# Tal's Mater Class
# Version 5 - 14.2.19

from commands import Commands
import Tkinter as tk
import ttk


class GUI(object):
    def __init__(self, command_callback=None, send_callback=None, debug=False):
        """
        :param command_callback: the function to call if the user changes the command
        :param send_callback: the function to call if the user press the send button
        :param debug: debug mode (True-on, False-off)
        """
        # if the server is closed
        self.__closed = False
        # the function to call when pressing the button
        self.__send_callback = send_callback if send_callback is not None else self.__default_send_callback
        # the function to call when changing the command combo box
        self.__command_callback = command_callback if command_callback is not None else self.__default_command_callback
        # the gui's window
        self.__root = tk.Tk()
        # a list of the combo boxes
        self.__comboboxes = {}
        # a list of all the entries - (label, entry) for each parameter
        self.__entries = []
        # debug mode
        self.__DEBUG = debug
        # initialize the gui
        self.__initialize()

    def __initialize(self):
        """
        Initialize - add to the window (root) all the labels, button and combo-boxes and bind them to their functions
        :return:
        """
        # if debug mode is on, print that right now initializing the gui
        if self.__DEBUG:
            print "Initializing The GUI"
        # add the title
        title_label = tk.Label(self.__root, justify=tk.LEFT, text=r"""
             _      __    __                     __  ___        __         
            | | /| / /__ / /______  __ _  ___   /  |/  /__ ____/ /____ ____
            | |/ |/ / -_) / __/ _ \/  ' \/ -_) / /|_/ / _ `(_-< __/ -_) __/
            |__/|__/\__/_/\__/\___/_/_/_/\__/ /_/  /_/\_,_/___|__/\__/_/

            """)
        title_label.grid(row=0, column=0, columnspan=2)

        # add the peasant's ip (label and combo box)
        peasant_label = tk.Label(self.__root, text="Peasant IP:")
        peasant_label.grid(row=1, column=0)

        peasant_combobox = ttk.Combobox(self.__root, state="readonly", values=[])
        if len(peasant_combobox["values"]):
            peasant_combobox.set(peasant_combobox["values"][0])
        peasant_combobox.grid(row=1, column=1)
        self.__comboboxes['peasant'] = peasant_combobox

        # add the command (label and combo box)
        command_label = tk.Label(self.__root, text="Command:")
        command_label.grid(row=2, column=0)

        command_combobox = ttk.Combobox(self.__root, state="readonly", values=Commands.get_commands_names())
        if len(command_combobox["values"]):
            command_combobox.set(command_combobox["values"][0])
        command_combobox.grid(row=2, column=1)

        self.__comboboxes['command'] = command_combobox

        # add the send button
        send_button = tk.Button(self.__root, text="Send")
        send_button.grid(row=10, column=0, columnspan=2)

        # bind the command combo-box and the send button to their respective callback functions
        command_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.__command_callback(
            event=event, root=self.__root, command=self.__comboboxes['command'].get(), entries=self.__entries,
            regrid=[send_button]))
        send_button.bind("<Button-1>", lambda event=None: self.__send_callback(
            event=event, comboboxes=self.__comboboxes, entries=self.__entries))

    def __default_command_callback(self, event, root, command, entries, regrid):
        """
        Changes the entries to be the new command's parameters (via the Commands class)
        :param event: the event - <<ComboboxSelected>>
        :param root: the Tk'swindows
        :param command: the chosen command
        :param entries: the current entries
        :param regrid: what should be re-grid after changing the entries
        :return:
        """
        if self.__DEBUG:
            print('--------DEFAULT COMMAND CALLBACK--------')
        else:
            print('------------COMMAND CALLBACK------------')
        # destroy all previous entries and remove them from the list
        for ent in entries[::-1]:
            l, e = ent
            l.destroy()
            e.destroy()
            entries.remove(ent)
        # forger grid of the widgets below the entries
        for w in regrid:
            w.grid_forget()

        # get the row to add the new entries
        row = root.grid_size()[1]
        # create new entries based on the selected command
        print command
        for entry in Commands.get_commands_parameters(command):
            # create label and entry
            l = tk.Label(root, text=str(entry) + ":")
            e = tk.Entry(root)
            l.grid(row=row, column=0)
            e.grid(row=row, column=1)
            row += 1
            entries.append((l, e))

        # re grid the widgets to be below the new entries
        for w in regrid:
            w.grid(row=row, columnspan=2)
            row += 1

    def __default_send_callback(self, event, comboboxes, entries):
        """
        Prints the combo-boxes' and entries' values
        :param event: the event - <Button-1>
        :param comboboxes: all the combo-boxes
        :param entries: all the entries
        :return:
        """
        if self.__DEBUG:
            print('--------DEFAULT SEND CALLBACK--------')
        else:
            print('------------SEND CALLBACK------------')
        # print combo-boxes' values
        for cb in comboboxes.values():
            print "<" + str(cb.get()) + ">",
        print ''
        # print entries' values
        for l, e in entries:
            print "<" + str(e.get()) + ">",

    def add_connection(self, address):
        """
        Add a new connection to the peasant's combo-box
        :param address: the new peasant's address
        :return: nothing, void
        """
        # save the combo-box in a variable
        cb = self.__comboboxes['peasant']
        # if the combo-box's values is empty
        if not cb['values']:
            # add a dummy into the values
            cb['values'] += '$'
            # add the address
            cb['values'] += (str(address),)
            # remove the dummy by setting the values to a tuple with only the address
            cb['values'] = (str(address),)
        # the combo-box's values isn't empty
        else:
            # add to the values a tuple with only the address
            cb['values'] += (str(address),)

    def run(self):
        """
        Runs the gui - the window (with Tkinter.Tk.mainloop())
        :return: nothing, void
        """
        self.__root.mainloop()


if __name__ == '__main__':
    # create a new master
    gui = GUI()
    gui.add_connection("127.0.0.1 : 80")
    gui.add_connection("127.0.0.1 : 5400")
    gui.add_connection("127.0.0.1 : 1000")
    # run the gui
    gui.run()
