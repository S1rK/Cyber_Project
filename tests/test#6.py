"""
Tal's Mater Class
Version 5 - 14.2.19
"""


def func1(a, b):
    print a + b


def warapper(func, *args):
    func(*args)


if __name__ == '__main__':
    """
    pic = '1.png'
    with open(pic, 'rb') as f:
        data = f.read()
    with open('2.png', 'wb') as f:
        f.write(data)
    print len(data)
    print len(str(len(data)))
    print pic[pic.rfind('.')+1:]
    
    -----------------------------------
    import win32com.client as cl
    
    sp = cl.Dispatch("SAPI.SpVoice")
    sp.Speak("ELIRAN. STOP PLAYING CHESS")
    
    warapper(func1, 'hi ', 'there')
    """

    x = "hi|there|boi"
    print x.split('|')
