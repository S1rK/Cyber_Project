# Tal's Mater Class
# Version 5 - 14.2.19

from commands import Commands
import Tkinter as tk
import ttk
import sys

FONT = ("Fixedsys", 16)


class HighlightText(tk.Text):
    """A text widget with a new method, highlight_pattern()"""
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        """Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        """
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "":
                break
            # degenerate pattern which matches zero-length strings
            if count.get() == 0:
                break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


class GUI(object):
    def __init__(self, command_callback=None, send_callback=None, debug=False):
        """
        :param command_callback: the function to call if the user changes the command
        :param send_callback: the function to call if the user press the send button
        :param debug: debug mode (True-on, False-off)
        """
        # the function to call when pressing the button
        self.__send_callback = send_callback if send_callback is not None else self.__default_send_callback
        # the function to call when changing the command combo box
        self.__command_callback = command_callback if command_callback is not None else self.__default_command_callback
        # the gui's window
        self.__root = tk.Tk('Command Center')
        # a list of the combo boxes
        self.__comboboxes = {}
        # a list of all the entries - (label, entry) for each parameter
        self.__entries = []
        # a text box to print all the output to
        self.__output = None
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
        # change the root's background color
        self.__root.configure(background='black')
        self.__root.title("Command Center")
        # add the title
        title_label = tk.Label(self.__root, justify=tk.LEFT, font=FONT, text=""" _______  _____  _______ _______ _______ __   _ ______       _______ _______ __   _ _______ _______  ______
 |       |     | |  |  | |  |  | |_____| | \  | |     \      |       |______ | \  |    |    |______ |_____/
 |_____  |_____| |  |  | |  |  | |     | |  \_| |_____/      |_____  |______ |  \_|    |    |______ |    \_
                                                                                    """)
        title_label.configure(background='black', foreground='green')
        title_label.grid(row=0, column=0, columnspan=2)

        # add the style
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings={'TCombobox':
                                              {'configure':
                                                   {'selectbackground': 'black', 'fieldbackground': 'black', 'background': 'green', 'foreground': 'green'}}})

        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        combostyle.theme_use('combostyle')

        # add the peasant's ip (label and combo box)
        peasant_label = tk.Label(self.__root, text="Peasant Address:", font=FONT)
        peasant_label.configure(background='black', foreground='green')
        peasant_label.grid(row=1, column=0)

        peasant_combobox = ttk.Combobox(self.__root, state="readonly", values=[], font=FONT)
        peasant_combobox.grid(row=1, column=1)
        peasant_combobox.configure(background='black', foreground='green')
        self.__comboboxes['peasant'] = peasant_combobox

        # add the command (label and combo box)
        command_label = tk.Label(self.__root, text="Command:", font=FONT)
        command_label.configure(background='black', foreground='green')
        command_label.grid(row=2, column=0)

        command_combobox = ttk.Combobox(self.__root, state="readonly", values=Commands.get_commands_names(), font=FONT)
        command_combobox.configure(background='black', foreground='green')
        command_combobox.grid(row=2, column=1)

        self.__comboboxes['command'] = command_combobox

        # add the send button
        send_button = tk.Button(self.__root, text="Send", font=FONT)
        send_button.configure(background='black', foreground='green')
        send_button.grid(row=10, column=0, columnspan=2)

        # add the output highlight-able text
        output = HighlightText(self.__root, state=tk.DISABLED, font=FONT)
        output.config(state=tk.DISABLED, font=FONT)
        output.configure(background='black', foreground='green')
        output.grid(row=11, column=0, columnspan=2)
        # add the red highlight tag
        output.tag_configure("red", foreground="red")
        # add the red highlight tag
        output.tag_configure("blue", foreground="blue")
        # print to the screen a welcome message
        output.config(state=tk.NORMAL)
        output.insert(tk.END, """_ _ _ ____ _    ____ ____ _  _ ____    _  _ ____ ____ ___ ____ ____ 
| | | |___ |    |    |  | |\/| |___    |\/| |__| [__   |  |___ |__/ 
|_|_| |___ |___ |___ |__| |  | |___    |  | |  | ___]  |  |___ |  \ 
                                                                    \n""")
        output.config(state=tk.DISABLED)
        # set the member output to be the output we just used
        self.__output = output

        # bind the command combo-box and the send button to their respective callback functions
        command_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.__command_callback(
            event=event, root=self.__root, command=self.__comboboxes['command'].get(), entries=self.__entries,
            regrid=[send_button, output]))
        send_button.bind("<Button-1>", lambda event=None: self.__send_enhance_callback(event, [send_button, output]))

        # weight the grid
        for col in range(self.__root.grid_size()[0]):
            self.__root.grid_columnconfigure(col, weight=1)
        for row in range(self.__root.grid_size()[1]):
            self.__root.grid_rowconfigure(row, weight=1)

    def __send_enhance_callback(self, event, regrid):
        self.__send_callback(event, self.__comboboxes, self.__entries)
        self.__command_callback("<<ComboboxSelected>>", self.__root, self.__comboboxes['command'].get(), self.__entries,
                                regrid)

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
        for entry in Commands.get_commands_parameters(command):
            # create label and entry
            l = tk.Label(root, text=str(entry) + ":", font=FONT)
            e = tk.Entry(root, font=FONT)
            l.configure(background='black', foreground='green')
            e.configure(background='black', foreground='green')
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
        # print combo-boxes' values
        for cb in comboboxes.values():
            print "<" + str(cb.get()) + ">",
        print ''
        # print entries' values
        for l, e in entries:
            print "<" + str(e.get()) + ">",
            e.delete(0, tk.END)

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
        # print to the output that a new connection has been established
        print "A New Connection From Address: <%s>" % str(address)

    def remove_connection(self, address):
        """
        Remove an existing connection from the peasant's combo-box
        :param address: the existing peasant's address
        :return: nothing, void
        """
        # save the combo-box in a variable
        cb = self.__comboboxes['peasant']['values']
        # if the address is in the combo-box's values
        if str(address) in cb:
            cb = list(cb)
            cb.remove(str(address))
            self.__comboboxes['peasant']['values'] = tuple(cb)
        # print to the output that an existing connection has been disconnected
        if self.__DEBUG:
            print "DEBUG: Server Handled <%s> Disconnection." % str(address)

    def write(self, text):
        """
        A function to print to the gui some given text.
        :param text: the text to print to the gui
        :return: nothing, void
        """
        self.__output.config(state=tk.NORMAL)
        self.__output.insert(tk.END, text)
        # add the red tag to all the ERROR msgs
        self.__output.highlight_pattern("ERROR", "red")
        # add the blue tag to all the DEBUG msgs
        self.__output.highlight_pattern("DEBUG", "blue")
        self.__output.config(state=tk.DISABLED)

    def run(self):
        """
        Runs the gui - the window (with Tkinter.Tk.mainloop())
        :return: nothing, void
        """
        # set the stdout to be the gui
        sys.stdout = self

        # run the tkinter main loop
        self.__root.mainloop()

        # return the normal stdout
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    # create a new gui
    gui = GUI()

    # set the stdout to be the gui
    sys.stdout = gui

    # check the add connection and write (print) functions
#    gui.add_connection("186.125.134.34 : 7854")
#    gui.add_connection("54.86.11.99 : 5114")
#    gui.add_connection("155.118.92.70 : 4521")
#    gui.add_connection("219.210.78.5 : 1148")
    #    print "ERROR: This is an error msg"
#    print "DEBUG: This is a debug msg"

    # run the gui
    gui.run()
