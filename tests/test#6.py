"""
Tal's Mater Class
Version 5 - 14.2.19
"""


if __name__ == '__main__':
    pic = '1.png'
    with open(pic, 'rb') as f:
        data = f.read()
    with open('2.png', 'wb') as f:
        f.write(data)
    print len(data)
    print len(str(len(data)))
    print pic[pic.rfind('.')+1:]
