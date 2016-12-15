# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module that contains helper functions that can be useful when handle files
"""

import errno
import logging
import os


def safe_mkdir(path):
    """
    method responsible for create directories in a safe way.
    :param path: path to be created
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open(filepath, mode='+'):
    """
    Open a file for writing, creating any parent directories if needed.

    :param filepath: full path to the file to be open
    :param mode: mode to access the file, i.e., 'r', 'w', 'x', 'a','b' and so on
    :return: An opened file, if it exists.
    """
    full_path = os.path.abspath(filepath)
    path = full_path.strip(os.path.basename(filepath))
    safe_mkdir(path)
    try:
        file = open(full_path, mode)
    except FileNotFoundError:
        file = open(full_path, 'x')
    return file


def get_logger(name, log_file):
    """
    A function that helps to create a logger that can be used anywhere.
    This function came from:
    "https://github.com/heltondoria/Systems-Engineering/blob/master/BRI/Work_1/InvertedIndex.py"

    :param name: name of the logger
    :param log_file: full path to the log file
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(stream_handler)

    return logger
