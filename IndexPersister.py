#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2016 
# Author: Helton Costa <helton.doria@gmail.com>
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
import errno
import json
import os
import pickle


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open(path, qualifier):
    """
    Open "path" for writing, creating any parent directories as needed.

    :param qualifier: method to access the file, i.e., r, w, b and so on
    :param path: path to be opened
    :return: An opened file, if it exists.
    """
    mkdir(os.path.dirname(path))
    return open(path, qualifier)


class IndexPersister:
    def __init__(self, index, path='./index/'):

        self.index = index
        self.path = path

    def write_binary_index(self):
        """
        Writes a binary version of the inverted index to reload later.
        """
        try:
            with safe_open(self.path + 'index.pkl', 'wb') as f:
                return pickle.dump(self.index, f, pickle.HIGHEST_PROTOCOL)
        except:
            raise

    def load_binary_index(self):
        """
        If exists, load the binary version of the inverted index to continue from the last load.
        """
        try:
            with safe_open(self.path + 'index.pkl', 'rb') as f:
                return pickle.load(f)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass

    def write_json_index(self):
        """
        Write the inverted index as a JSON file to be human readable.
        """

        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        with safe_open(self.path + 'index.json', 'w') as f:
            json.dump(self.index, f, default=set_default)
