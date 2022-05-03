from ocr import get_awaking
from utils import awaking_aggregator, reporter

if __name__ == '__main__':
    res = awaking_aggregator.normalize(get_awaking())
    comp = awaking_aggregator.compare(res, 'configs/stats_set_1.yml')
    print(res)
    print('comparation:', comp)
    file = 'reports/test.csv'
    # reporter.initialize('awaking', file)

    reporter.report('awaking', file, (0, res, comp, 'test file name'))