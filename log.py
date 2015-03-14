import logging


def init_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s')

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel(logging.INFO)

    fileHandler = logging.FileHandler('waar.log')
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    return logger