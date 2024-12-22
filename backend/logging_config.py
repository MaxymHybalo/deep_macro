import logging
import colorlog

def setup_logging():
    log_format = (
        '%(log_color)s[%(levelname)s] - %(asctime)s | %(name)s | %(message)s'
    )
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(log_color)s[%(levelname)s] - %(asctime)s | %(name)s | %(message)s',
    #                     handlers=[
    #                         logging.FileHandler("debug.log"),
    #                         logging.StreamHandler()
    #                     ])
    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    formatter = colorlog.ColoredFormatter(log_format, log_colors=log_colors)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('debug.log')
    file_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] - %(asctime)s | %(name)s | %(message)s'
    ))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)