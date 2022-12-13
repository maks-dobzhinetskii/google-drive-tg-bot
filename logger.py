import concurrent.futures
import logging

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def info(self, msg: str, *args):
    executor.submit(logging.info, msg, *args)


def warning(self, msg: str, *args):
    executor.submit(logging.warning, msg, *args)


def error(self, msg: str, *args):
    executor.submit(logging.error, msg, *args)
