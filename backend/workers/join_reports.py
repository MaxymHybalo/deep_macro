# from csv import reader, writer as wt, QUOTE_MINIMAL
import csv
from logging import root
import os
from functools import reduce

root_path = 'D:/code/deep_macro/deep_macro/backend/reports'
results = 'full_report.csv'
header = ['#','сила','энергия','интелект','мудрость','ловкость','сноровка','сила удар крит','скорость передвижения','магическое сопротивление','уклонение','маг точность','точность','скорость каста','скорость атаки','физ атака','маг атака','физ защита','маг защита','шанс крит','unknown','Done?','Value','Attempt status','Time', 'awaker']

files = os.listdir(root_path)
# print(files)

test = files[0]
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
with open(results, mode='a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    for part in files:
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
                    writer.writerow(row)
                    counter += 1
