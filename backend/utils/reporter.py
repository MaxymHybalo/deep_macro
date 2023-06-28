import csv
from datetime import datetime

from utils import awaking_aggregator

def report(type, filename, data, props=[]):
    if type == 'awaking':
        reportAwake(filename, data)
    if type == 'rings':
        reportRings(filename, data, props=props)


def reportRings(filename, data, props=[]):
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        d, f = data
        row = [*_build_awaking_props_row(d, props=props), f]
        writer.writerow(row)


def reportAwake(filename, data):
    # write
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        i, d, s, l = data
        done = True if s is not None else False
        value = s[1] if done else ''
        done_mark = '+' if done else '-'
        timestamp = datetime.now().strftime('%H:%M:%S')
        row = [i, *_build_awaking_props_row(d), done_mark, value, l, timestamp]
        writer.writerow(row)
        print(row)

def initialize(type, filename, props=awaking_aggregator.normal_props):
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        heading = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if type == 'rings':
            heading.writerow([*props, 'File'])
        else:
            heading.writerow(['#', *props, 'Done?','Value', 'Attempt status', 'Time'])

def buildFileName(name):
    date = datetime.now().strftime('%H_%M_%S_%d_%m_%y')
    return 'reports/{}_{}.csv'.format(name, date)

def _build_awaking_props_row(data, props=awaking_aggregator.normal_props):
    row = []
    for prop in props:
        value = ''
        for r in data:
            if r[0] == prop:
                value = value + str(r[1]) + ';' # customize cell output (rate calculation etc)
        row.append(value[:-1])
    return row