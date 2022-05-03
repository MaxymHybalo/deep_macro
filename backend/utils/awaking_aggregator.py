import re

import numpy as np

from ocr import get_awaking
import config

SUCCESS_RATE = 0.7


normal_props = (
    'сила',
    'энергия',
    'интелект',
    'мудрость',
    'ловкость',
    'сноровка',
    'удача',
    'физ атака',
    'маг атака',
    'точность',
    'маг точность',
    'физ защита',
    'маг защита',
    'уклонение',
    'магическое сопротивление',
    'скорость каста',
    'скорость атаки',
    'шанс крит',
    'сила удар крит',
    'защита блок',
    'скорость передвижения'
)

MATCH_MATRIX = {
    'сила': 'strength',
    'энергия': 'vitality',
    'интелект': 'int',
    'мудрость': 'wisdom',
    'ловкость': 'dexterity',
    'сноровка': 'agility',
    'удача': 'luck',
    'физ атака': 'p_atk',
    'маг атака': 'm_atk',
    'точность': 'acc',
    'маг точность': 'm_acc',
    'физ защита': 'p_def',
    'маг защита': 'm_defd',
    'уклонение': 'evasion',
    'магическое сопротивление': 'm_res',
    'скорость каста': 'cast_speed',
    'скорость атаки': 'atk_speed',
    'шанс крит': 'c_rate',
    'сила удар крит': 'c_rate',
    'защита блок': 'block',
    'скорость передвижения': 'm_speed'
}
def compare(data, targetPath):
    targets = config.load_config(targetPath) # how to preload config?
    print(data)
    prop = 'unknown'
    for goal, value in targets.items():
        # print(goal, value)
        capacitor = 0
        for row in data:
            if row[0] in MATCH_MATRIX:
                if MATCH_MATRIX[row[0]] == goal:
                    prop = row[0]
                    capacitor = capacitor + row[1]
        if capacitor >= value:
            return prop, capacitor
        capacitor = 0
        prop = 'unknown'

    return None


def normalize(data):
    # print(data)
    normalized = []
    for row in data:
        # print(row)
        ratio, prop = normalizeProp(row[1])
        value = normalizeValue(row[2])
        # print(ratio, prop, value)
        normalized.append([prop, value, ratio])
    return normalized

def normalizeProp(prop):
    prop = prop.lower()
    rates = []
    for i in normal_props:
        ratio = levenshtein_ratio_and_distance(prop, i.lower(), ratio_calc=True)
        rates.append(ratio)
    m = max(rates)
    id = rates.index(m)

    if m >= SUCCESS_RATE:
        return round(m, 2), normal_props[id]
    return 0, 'unknown'

def normalizeValue(value):
    return int(re.findall(r'\d+', value)[0])

def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])