from datetime import datetime
import cv2
import pytesseract
from ocr import crop_roi, get_text
import re
import config
from utils.awaking_aggregator import levenshtein_ratio_and_distance
from utils.reporter import report, initialize

ETHER_ROI_WIDTH = 135
CONFIG = 'configs/ring_config.yml'
RATIO = 0.7

cfg = config.load_config(CONFIG)

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
    'rate': 'шанс крит удара',
    'deff': 'физ. защита'
}

normal_props = list(match_map.values())
report_name = 'rings_reports.csv'

def init_report():
    print('init')
    initialize('rings', report_name, props=normal_props)

def _find_stat_name(source):
    temp = ''
    for chr in source:
        # print(chr)
        if not chr.isdigit():
            temp += chr
    return temp

def compare(ring):
    # print(ring)
    for c in cfg['config']:
        # print(c)
        matches = 0
        for i, line in enumerate(c.items()):
            t_k, t_v = line
            key = match_map[t_k]
            present_key, present_value = ring[i]
            ratio = levenshtein_ratio_and_distance(key, present_key, ratio_calc=True)
            # print(i, line, present_key, present_value, ratio)
            if ratio > RATIO:
                if present_value >= t_v:
                    matches = matches + 1

        if matches == 3:
            print('[Match]: ', c, ring)
            return True
    return False

def capture(img):
    logImg = img.copy()
    firstEntry = crop_roi(img, (0,0, ETHER_ROI_WIDTH, 17))
    secondEntry = crop_roi(img, (0, 17, ETHER_ROI_WIDTH, 17))
    thirdEntry = crop_roi(img, (0, 17*2, ETHER_ROI_WIDTH, 17))
    field1 = pytesseract.image_to_string(firstEntry, lang="rus")
    field2 = pytesseract.image_to_string(secondEntry, lang="rus")
    field3 = pytesseract.image_to_string(thirdEntry, lang="rus")
    ring = []

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
        ring.append((stat, float(value)))
        # print('match', match)
    log_data(ring, logImg)

    if len(ring) < 3:
        return False
    print('Ring, ', ring)
    return compare(ring)

def is_back_caption(img):
    img = crop_roi(img, (715, 235, 48, 20))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    
    text = get_text(img)
    ratio = levenshtein_ratio_and_distance('Назад', text, ratio_calc=True)
    return ratio > RATIO

init_report()

def log_data(ring, img):
    time = datetime.now().strftime('%H_%M_%S_%d_%m_%y')
    filename = f'ring_{time}'

    
    cv2.imwrite(f'logs/searching/{filename}.png', img)
    l = []
    for r in ring:
        s, v = r
        for m in match_map.values():
            ratio = levenshtein_ratio_and_distance(s, m, ratio_calc=True)
            if ratio > RATIO:
                l.append([m, v])
    report('rings', report_name, [l, filename], props=normal_props)


if __name__ == '__main__':
    import time
    s = time.time()
    for i in range(96):
        # i = 6
        img = cv2.imread(f'logs/searching/ring_{i}.png')
        capture(img)
        # print('__________________')

    print(time.time() - s)