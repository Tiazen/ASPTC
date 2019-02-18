import os, subprocess, sys

from ascpt import settings


def runcmd(com, par):
    data = bytearray(bytes(par, 'utf-8')).replace(b'\\n', b'\n')
    x = subprocess.Popen(['C:\\Users\\Tiazz0\\AppData\\Local\\Programs\\Python\\Python36\\python.exe', str(com)], stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    try:
        result = x.communicate(input=data, timeout=1)
        return result
    except subprocess.TimeoutExpired:
        x.kill()


def runtests(filename, record_task, record_test):
    test_inputs = record_task.inputs.split(',')
    test_inputs.pop(-1)

    test_output = record_task.outputs.split(',')
    test_output.pop(-1)

    test_result = []
    tt = []

    for i in range(len(test_inputs)):
        a = runcmd(filename, test_inputs[i])
        err = a[1]
        print(bytes(test_inputs[0], 'utf-8'), a[0])
        if err is None and bytearray(a[0].strip()).replace(b'\r\n', b'\n') == bytearray(bytes(test_output[i], 'utf-8')).replace(b'\\n', b'\n').replace(
                bytes(' ', 'utf-8'), b''):
            print('test {} CORRECT. Found {}, expected {}'.format(i,  a[0], bytes(test_output[i], 'utf-8')))
            test_result.append(1)
        else:
            print('test {} INCORRECT. Found {}, expected {}'.format(i,  bytearray(a[0]),
                    bytearray(bytes(test_output[i], 'utf-8')).replace(b'\\n', b'\n').replace(bytes(' ', 'utf-8'), b'')))
            test_result.append(0)

    points = 100
    if 0 in test_result:
        points = test_result.count(1)

    if points == 100:
        record_test.points = points
        record_test.status = "OK"
        record_test.tests = str(test_result)

    elif points < 100:
        record_test.points = points
        record_test.status = "PS"
        record_test.tests = str(test_result)

    record_test.save()

    return test_result
