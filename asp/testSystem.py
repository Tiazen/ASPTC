import os, subprocess

from ascpt import settings


def runcmd(com, par):
    x = subprocess.Popen(com, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    data = bytes(par, 'utf-8')
    result = x.communicate(input=data, timeout=1)
    return result


def runtests(filename):
    file_path = settings.MEDIA_ROOT + '\\' + str(filename)
    a = runcmd(file_path, '1 2')
    err = a[1]
    b = a[0].decode('utf-8')
    print(b, err)
