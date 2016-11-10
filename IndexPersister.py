# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2016 
# Author: Helton Costa <helton.doria@gmail.com>
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
import errno
import os
import pickle
import csv


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
    def __init__(self, index, inverted_index, path='./index/'):

        self.index = index
        self.inverted_index = inverted_index
        self.path = path

    def write_binary_index(self):
        """
        Writes a binary version of the inverted index to reload later.
        """
        try:
            with safe_open(self.path + 'index.pkl', 'wb') as f:
                pickle.dump(self.index, f, pickle.HIGHEST_PROTOCOL)
            with safe_open(self.path + 'inverted_index.pkl', 'wb') as f:
                pickle.dump(self.inverted_index, f, pickle.HIGHEST_PROTOCOL)
        except:
            raise

    def __load_binary_index(self, file_name):
        """
        If exists, load the binary version of the chosen index to continue from the last load.
        """
        try:
            with safe_open(self.path + file_name + '.pkl', 'rb') as f:
                return pickle.load(f)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass

    def load_inverted_index(self):
        """
        Serialize the inverted index
        :return: A deserialized version of the index
        """
        try:
            with safe_open(self.path + 'inverted_index.pkl', 'rb') as f:
                return pickle.load(f)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass

    def load_index(self):
        """
        Deserialize the forward index
        :return: A deserialized version of the index
        """
        try:
            with safe_open(self.path + 'index.pkl', 'rb') as f:
                return pickle.load(f)
        except EOFError:
            pass
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass

    def csv_inverted_index_writer(self, data):
        """
        Write the a inverted index in csv format
        """
        with safe_open(self.path + 'inverted_index.csv', 'w') as f:
            csv_obj = csv.writer(f)
            for key in data.keys():
                for item in data[key]:
                    csv_obj.writerow([key + ";" + str(item.freq) + ";" + item.file_id])

    def csv_forward_index_writer(self, data):
        """
        Write the a forward index in csv format
        """
        with safe_open(self.path + 'index.csv', 'w') as f:
            csv_obj = csv.writer(f)
            for key in data.keys():
                csv_obj.writerow([key + ";" + data[key]])

