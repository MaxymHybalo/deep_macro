# from csv import reader, writer as wt, QUOTE_MINIMAL
import csv
from logging import root
import os
from functools import reduce

root_path = 'D:/code/deep_macro/deep_macro/backend/reports'
results = 'accces.csv'
HEADER = ['#','сила','энергия','интелект','мудрость','ловкость','сноровка','сила удар крит','скорость передвижения','магическое сопротивление','уклонение','маг точность','точность','скорость каста','скорость атаки','физ атака','маг атака','физ защита','маг защита','шанс крит','unknown','Done?','Value','Attempt status','Time', 'awaker', 'date']
exclude_file_props = ['сила удар крит', 'шанс крит']
exlude_column_ids = [7, 19]
char_filter = 'PurpleWave'

files = os.listdir(root_path)
print(len(files))
def char_date_filter(file):
    if char_filter in file:
        # print(f, f.split('_'))
        date = file.split('_')
        # print(date[5])
        # if date[5] == '03':
        return False
        
    return True

# files = list(filter(char_date_filter, files))
print(files)
def squash_values(row):
    res = []
    for r in row:
        values = r.split(';')
        if len(values) > 1:
            squashed = reduce((lambda x, y: int(x) + int(y)), values)
            r = squashed
            # print('squashed', squashed, values)
        res.append(r)
    return res

counter = 0
accessories = []
for part in files:
    with open('{}/{}'.format(root_path, part), 'r') as read_obj:
        pointer = False
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                for exclude in exlude_column_ids:
                    if len(row[exclude]):
                        accessories.append(part)
                        pointer = True
                        break
                if pointer:
                    break

def disjoint(e,f):
    c = e.copy() # [:] works also, but I think this is clearer
    d = f.copy()
    for i in e: # no need for index. just walk each items in the array
        for j in f:
            if i == j: # if there is a match, remove the match.
                c.remove(i)
                d.remove(j)
    return c + d


def cvt_date(name):
    date = name.split('_')
    date[6] = date[6].split('.')[0]
    return '{}/{}/{}'.format(date[4], date[5], date[6])

weapons = disjoint(files, accessories)
print(len(files), len(accessories), len(weapons), len(files) - len(weapons))
# print(accessories, len(accessories))

with open(results, mode='a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(HEADER)
    for part in accessories:
        with open('{}/{}'.format(root_path, part), 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    # row variable is a list that represents a row in csv
                    # print(row)
                    row[0] = str(counter)
                    row = squash_values(row)
                    row.append(part)
                    row.append(cvt_date(part))
                    writer.writerow(row)
                    counter += 1
