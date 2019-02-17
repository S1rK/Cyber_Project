# test image grabbing (screenshots and then video)

from PIL.ImageGrab import grab
import os
import time


def screen_grab():
    # snapshot of screen
    im = grab()
    image_name = os.getcwd() + r'\boi.jpg'
    # saves in current work directory with name based on time of pic
    im.save(image_name)
    with open(image_name, 'rb') as image:
        print len(image.read())


def main():
    time.sleep(3)
    screen_grab()
    print 'hi'


if __name__ == '__main__':
    main()
