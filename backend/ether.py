import cv2
import pytesseract
from ocr import crop_roi
import re
import config
from utils.awaking_aggregator import levenshtein_ratio_and_distance

ETHER_ROI_WIDTH = 135
CONFIG = 'configs/ring_config.yml'
RATIO = 0.8

cfg = config.load_config(CONFIG)
print(cfg)

match_map = {
    'strength': 'сила',
    'vitality': 'энергия',
    'int': 'интелект',
    'wisdom': 'мудрость',
    'dexterity': 'ловкость',
    'agility': 'сноровка',
    'cp': 'сила крит. удар',
    'move': 'скор. бега',
    'acc':  'точность',
    'macc': 'маг. точность',
    'eva': 'уклонение',
    'res': 'м. сопр.',
    'cast': 'скор. заклинаний',
    'speed': 'скор. атаки',
    'pb': 'полный блок',
    'rate': 'шанс крит удара'
}

def _find_stat_name(source):
    temp = ''
    for chr in source:
        # print(chr)
        if not chr.isdigit():
            temp += chr
    return temp

def compare(stat, value):
    for ring in cfg['config']:
        # print(ring)
        for line in ring.items():
            target, t_value = line
            k = match_map[target]
            ratio = levenshtein_ratio_and_distance(k, stat, ratio_calc=True)
            if ratio > RATIO:
                print(stat, k, t_value, value)
                return 1 if value >= t_value else 0
            # for k, v in match_map.items():
            #     print(v, target)
            #     ratio = levenshtein_ratio_and_distance( v, target, ratio_calc=True)
            #     if ratio > RATIO:
            #         print(stat, v, t_value)
    return 0

def capture(img):
    firstEntry = crop_roi(img, (0,0, ETHER_ROI_WIDTH, 17))
    secondEntry = crop_roi(img, (0, 17, ETHER_ROI_WIDTH, 17))
    thirdEntry = crop_roi(img, (0, 17*2, ETHER_ROI_WIDTH, 17))
    field1 = pytesseract.image_to_string(firstEntry, lang="rus")
    field2 = pytesseract.image_to_string(secondEntry, lang="rus")
    field3 = pytesseract.image_to_string(thirdEntry, lang="rus")
    # print(field1)
    # print(field2)
    # print(field3)
    for i in [field1, field2, field3]:
        # print(i)
        if len(i) < 2:
            continue
        stat = _find_stat_name(i)
        stat = stat.split('+')[0].strip().lower()
        # value = value.strip()
        value = re.findall(r'\d*?\.?\d+', i)
        
        value = ''.join(value)
        if value == '':
            value = 0
            
        # print(stat, value)
        match = compare(stat, float(value))
        print('match', match)

if __name__ == '__main__':
    
    for i in range(1):
        i = 6
        img = cv2.imread(f'logs/searching/ring_{i}.png')
        capture(img)
        print('__________________')