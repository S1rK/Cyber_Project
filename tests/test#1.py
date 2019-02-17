# testing encryption - decryption

import os
import random
import datetime
import base64
from PIL.ImageGrab import grab


def convert_to_binary(string):
    return ' '.join(format(ord(x), 'b') for x in string)


def convert_from_binary(binary):
    return binary.decode('ascii')


def encrypt(key, string):
    encrypted_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encrypted_c = chr(ord(string[i]) + ord(key_c) % 256)
        encrypted_chars.append(encrypted_c)
    encrypted_string = ''.join(encrypted_chars)
    return base64.urlsafe_b64encode(encrypted_string).rstrip(b'=')


def decrypt(key, string):
    string = base64.urlsafe_b64decode(string + b'===')
    decrypted_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        decrypted_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        decrypted_chars.append(decrypted_c)
    decrypted_string = ''.join(decrypted_chars)
    return decrypted_string


def dir():
    data = "Directory of: " + os.getcwd() + '\n'
    ls = os.listdir(os.getcwd())
    dircounter = 0
    for thing in ls:
        pth = os.getcwd() + '\\' + thing

        st = datetime.datetime.fromtimestamp(os.path.getctime(pth)).strftime('%Y-%m-%d %H:%M:%S') + '\t'
        if os.path.isdir(pth):
            st += "<DIR>"
            dircounter += 1
        else:
            st += thing[thing.rfind('.') + 1:]
        st += '\t' + thing
        data += st + '\n'

    data += '\n' + str(len(ls) - dircounter) + " File(s), " + str(dircounter) + " Dir(s)"
    return data


def encrypt_file(key, path):
    f = open(path, 'r')
    string = f.read()
    f.close()
    f = open(path, 'w')
    f.truncate(0)
    f.write(encrypt(key, string))
    f.close()


def decrypt_file(key, path):
    f = open(path, 'r')
    string = f.read()
    f.close()
    f = open(path, 'w')
    f.truncate(0)
    f.write(decrypt(key, string))
    f.close()


def screen_grab():
    # snapshot of screen
    im = grab()
    image_name = os.getcwd() + r'\boi.jpg'
    # saves in current work directory with name based on time of pic
    im.save(image_name)
    with open(image_name, 'rb') as image:
        image_data = image.read()
    os.remove(image_name)
    return image_data


s = 'Tal Was Here'
k = ''.join(random.choice('0123456789ABCDEF') for n in xrange(30))
print s
binary = convert_to_binary(s)
print binary
encrypted = encrypt(binary, k)
print encrypted
decrypted = decrypt(encrypted, k)
print decrypted
binary = convert_from_binary(decrypted)
print binary

command = raw_input("1 for encrypt, 2 for decrypt: ")
if command == '1':
    k = ''.join(random.choice('0123456789ABCDEF') for n in xrange(30))
    with open(os.getcwd() + r'\key.txt', 'w') as f:
        f.write(k)
    with open(os.getcwd() + r'\img.txt', 'w') as f:
        f.write(encrypt(key=k, string=convert_to_binary(screen_grab())))


elif command == '2':
    with open(os.getcwd() + r'\key.txt', 'w') as f:
        k = f.read()
    with open(os.getcwd() + r'\img.txt', 'r') as f:
        data = f.read()
    with open(os.getcwd() + r'\img.jpg', 'wb') as f:
        f.write(decrypt(key=k, string=data))
