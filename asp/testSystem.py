import os, subprocess

from ascpt import settings


def runcmd(com, par):
    x = subprocess.Popen(com, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    data = bytes(par, 'utf-8')
    result = x.communicate(input=data, timeout=1)
    return result


def runtests(filename, record_task, record_test):
    file_path = settings.MEDIA_ROOT + '\\' + str(filename)

    test_inputs = record_task.inputs.split(',')
    test_inputs.pop(-1)

    test_output = record_task.outputs.split(',')
    test_output.pop(-1)

    test_result = []
    for i in range(len(test_inputs)):
        a = runcmd(file_path, test_inputs[i])
        print(test_inputs[i], a[0])
        err = a[1]
        if err is None and a[0].decode('utf-8').strip() == test_output[i].strip():
            print('test {} CORRECT. Found {}, expected {}'.format(i,  a[0].decode('utf-8').strip(), test_output[i]))
            test_result.append(1)
        else:
            print('test {} INCORRECT. Found {}, expected {}'.format(i,  a[0].decode('utf-8').strip(), test_output[i]))
            test_result.append(0)

    points = 100
    if 0 in test_result:
        points = 100 - test_result.count(0)*(100//len(test_inputs))
        if points < 0:
            points = 0

    if points == 100:
        record_test.points = points
        record_test.status = "OK"
    elif points < 100:
        record_test.points = points
        record_test.status = "PS"

    record_test.save()

    return test_result
