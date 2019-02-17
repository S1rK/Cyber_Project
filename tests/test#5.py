# testing tkinter gui
import Tkinter as tk
import ttk
import random
import threading
import time


def change_command_callback(event=None, root=None, comboboxes=[], entries=[], regrid=[]):
    print('------------CHANGED COMMAND------------')
    # destroy all previous entries
    for ent in entries:
        l, e = ent
        l.destroy()
        e.destroy()
    # forger grid of the widgets below the entries
    for w in regrid:
        w.grid_forget()

    # get the row to add the new entries
    row = root.grid_size()[1]
    # create new entries based on the selected command
    for i in range(random.randint(3, 5)):
        print str(i)
        # create label and entry
        l = tk.Label(root, text=str(i)+":")
        e = tk.Entry(root)
        l.grid(row=row, column=0)
        e.grid(row=row, column=1)
        row += 1
        entries.append((l, e))

    # re grid the widgets to be below the new entries
    for w in regrid:
        w.grid(row=row, columnspan=2)
        row += 1


def send_callback(event=None, comboboxes=[], entries=[]):
    print('------------PRESSED SEND------------')
    # print combo boxes' values
    for cb in comboboxes:
        print "<" + str(cb.get()) + ">"
    # print entries' values
    for l, e in entries:
        print "<" + str(e.get()) + ">"


def run(peasants_cb):
    """use for select to add new peasants' ips"""
    time.sleep(2)
    peasants_cb['values'] += ("New Shit",)

    time.sleep(2)
    peasants_cb['values'] = peasants_cb['values'][:-1]



def main():
    comboboxes = []
    entries = []

    root = tk.Tk()
    title_label = tk.Label(root, text=r"""
 _      __    __                     __  ___        __         
| | /| / /__ / /______  __ _  ___   /  |/  /__ ____/ /____ ____
| |/ |/ / -_) / __/ _ \/  ' \/ -_) / /|_/ / _ `(_-< __/ -_) __/
|__/|__/\__/_/\__/\___/_/_/_/\__/ /_/  /_/\_,_/___|__/\__/_/
                                                                    
""")
    title_label.grid(row=0, column=0, columnspan=2)

    peasant_label = tk.Label(root, text="Peasant IP:")
    peasant_label.grid(row=1, column=0)
    peasant_combobox = ttk.Combobox(root, values=("256.256.10.2", "173.0.0.5", "58.176.2.4", "127.0.0.1"))
    peasant_combobox['values'] = peasant_combobox['values'] + ("255.255.255.255",)
    if len(peasant_combobox["values"]):
        peasant_combobox.set(peasant_combobox["values"][0])

    peasant_combobox.grid(row=1, column=1)
    comboboxes.append(peasant_combobox)

    command_label = tk.Label(root, text="Command:")
    command_label.grid(row=2, column=0)
    command_combobox = ttk.Combobox(root, values=("Take Screenshot", "Copy", "Delete", "Shutdown"))
    if len(command_combobox["values"]):
        command_combobox.set(command_combobox["values"][0])
    command_combobox.grid(row=2, column=1)
    command_combobox.bind("<<ComboboxSelected>>", lambda event: change_command_callback(event, root, comboboxes, entries, [send_button]))
    comboboxes.append(command_combobox)

    send_button = tk.Button(root, text="Send")
    send_button.bind("<Button-1>", lambda event: send_callback(event, comboboxes, entries))
    send_button.grid(row=10, column=0, columnspan=2)

    peasant_combobox['values'] = peasant_combobox['values'] + ("0.0.0.0",)

    threading.Thread(target=run, args=[peasant_combobox]).start()

    root.mainloop()


if __name__ == '__main__':
    main()
