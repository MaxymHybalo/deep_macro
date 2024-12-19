import logging

def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] - %(asctime)s | %(name)s | %(message)s',
                        handlers=[
                            logging.FileHandler("debug.log"),
                            logging.StreamHandler()
                        ])
    logging.getLogger().setLevel(logging.DEBUG)
