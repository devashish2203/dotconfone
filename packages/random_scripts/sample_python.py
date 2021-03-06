#!/usr/bin/env python
"""
eg:
./sample_python.py -w -x opt1 -y 3 -z 1 2 3

"""
from __future__ import print_function

import os
import sys
import argparse
import traceback
import logging
import logging.handlers
import random

# Requires 'pip install retrying' 
import retrying


logger = logging.getLogger()
LOG_FORMATTER = logging.Formatter(
    "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - " +
    "%(lineno)s - %(funcName)s - " +
    "%(message)s",
    "%Y%m%d %H:%M:%S")

def setup_logging(level=logging.INFO, enable_console=True):
    file_log_handler = logging.handlers.RotatingFileHandler(
        "__" + os.path.basename(__file__) + ".main__" + ".log",
        maxBytes=1000000,
        backupCount=5)
    console_log_handler = logging.StreamHandler()
    logger.addHandler(file_log_handler)
    if enable_console:
        logger.addHandler(console_log_handler)
    logger.setLevel(level)
    for handler in logging.root.handlers:
        handler.setFormatter(fmt=LOG_FORMATTER)


def retry_on_result_check(result):
    logger.info("Result: %s", result)
    # Return value should be True (retry) or False (don't retry)
    return result > 3


def retry_on_exception_check(exception):
    exc_mesg = "".join(traceback.format_tb(exception.__traceback__))
    logger.error("\n%s", exc_mesg)
    logger.error("Error: %s", exception)
    # Return value should be True (retry) or False (don't retry)
    return isinstance(exception, NameError)


@retrying.retry(wait_fixed=1000,
                retry_on_result=retry_on_result_check,
                retry_on_exception=retry_on_exception_check)
def retry_example():
    if random.randrange(1, 10) > 3:
        print(a) # Throws NameError
    else:
        print("Avoided exception in retry_example")
    return random.randrange(1, 10)



def print_variables(**kwargs):
    for key, value in kwargs.items():
        print(key, value)


def process(**kwargs):
    wval = kwargs.get("wval", False) # Set default values if needed
    xval = kwargs["xval"]
    yval = kwargs["yval"]
    zval = kwargs["zval"]

    print_variables(**kwargs)

    logger.debug("Message: %s", "debug")
    logger.info("Message: %s, %s", "info", 1)
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")

    logger.info("Example usage of retrying module - start")
    retry_example()
    logger.info("Example usage of retrying module - end")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Generic Application")
    parser.add_argument(
        "-w",
        "--wval",
        dest="wval",
        action="store_true",
        help="This variable is set to True only when '-w' is given",
        default=False
    )
    parser.add_argument(
        "-x",
        "--xval",
        dest="xval",
        choices=["opt1", "opt2"],
        type=str.lower, # Make case-insensitive
        help="Case-insensitive String Argument",
        required=True
    )
    parser.add_argument(
        "-y",
        "--yval",
        dest="yval",
        choices=[3, 4],
        help="Numerical Arguments",
        type=int,
        default=4,
        required=True
    )
    parser.add_argument(
        "-z",
        "--zval",
        dest="zval",
        nargs="+",
        help="Array arguments",
        type=int,
        default=[]
    )

    myargs = parser.parse_args()

    return process(**vars(myargs))


if __name__ == '__main__':
    setup_logging(level=logging.INFO)
    try:
        sys.exit(main()) # Ensure return value is passed to shell
    except Exception as error: # pylint: disable=W0702, W0703
        exc_mesg = traceback.format_exc()
        logger.error("\n%s", exc_mesg)
        logger.error("Error: %s", error)
        sys.exit(-1)
