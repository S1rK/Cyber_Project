# testing string shit ,functions shit (with list and args and so on) and tkinter list in combo box
import Tkinter
import ttk

def function_warrper(func, args):
    func(*args)


def func1(x, y, z):
    print "%s, %s, %s" % (str(x), str(y), str(z))


def func2():
    print "func2"


def main():
    """
    name = raw_input("enter name: ")
    print 'hi there %s' % name
    age = raw_input("enter age: ")
    print "so %s... you're %s yo"% (name, age)
    ----------------------------------------------
    lst = [1]
    function_warrper(func1, [1, 2, 3])
    print lst[1:]
    function_warrper(func2, lst[1:])
    ----------------------------------------------
    """

    root = Tkinter.Tk()

    combo = ttk.Combobox(root, values=['hi', 'hello', 'greetings'])
    combo.pack()

    combo['values'] = ('howdy',) + combo['values']

    root.mainloop()


if __name__ == '__main__':
    main()
