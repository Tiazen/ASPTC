import json
import os

from ascpt.settings import BASE_DIR


def updateThemes(data):
    data = data.split(',')
    print(data, len(data))
    if data[0] is not '':
        n = {'obj': []}
        for i in range(len(data)):
            n['obj'].append({'id': i, 'name': data[i]})

        with open(os.path.join(BASE_DIR, 'data_j.json'), 'w', encoding='utf-8') as wf:
            json.dump(n, wf, ensure_ascii=False)
    else:
        with open(os.path.join(BASE_DIR, 'data_j.json'), 'w', encoding='utf-8') as wf:
            wf.write('{"obj": []}')

def getThemes():
    data = []
    try:
        with open(os.path.join(BASE_DIR, 'data_j.json'), encoding='utf-8') as f:
            data = json.load(f)['obj']
            return data
    except FileNotFoundError:
        return data
