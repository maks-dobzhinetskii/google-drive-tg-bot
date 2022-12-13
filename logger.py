import concurrent.futures
import logging

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


def info(msg: str, *args):
    logging.basicConfig(filename='logs/INFO.log', format='%(levelname)s:%(message)s', level=logging.INFO)
    executor.submit(logging.info, msg, *args)


def warning(msg: str, *args):
    logging.basicConfig(filename='logs/WARNING.log', format='%(levelname)s:%(message)s', level=logging.WARNING)
    executor.submit(logging.warning, msg, *args)


def error(msg: str, *args):
    logging.basicConfig(filename='logs/ERROR.log', format='%(levelname)s:%(message)s', level=logging.ERROR)
    executor.submit(logging.error, msg, *args)
