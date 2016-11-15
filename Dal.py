# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module that contains classes responsible for data persistence in the index engine.
"""
import csv
import errno
import os
from abc import ABC, abstractmethod


class Dao(ABC):
    """
    Abstract class to define the common interface for a Dao class.
    """

    @abstractmethod
    def load(self, indexname=None):
        """
        Load data from the storage object
        :param indexname: name of the index to be load
        :return: data stored in some place
        """
        pass

    @abstractmethod
    def save(self, indexdata, indexname=None, fields=None):
        """
        Save data in the storage object
        :param fields: Name of the columns in the persistence unit
        :param indexname: name of the index to be saved
        :param indexdata: data to be persisted
        """
        pass


class CSVFileDal(Dao):
    """
    A concrete implementation of Dao abstract class that persist data in a simple csv file.
    """

    def __init__(self, path=None):
        self.path = path

    def load(self, indexname=None):
        """
        Load data from a simple csv file
        :param indexname: name of the csv file to be loaded
        :return: dict with data loaded from the file
        """
        with self.safe_open(indexname, mode='w') as file:
            reader = csv.DictReader(file)
            index = dict()
            if indexname == "forward_index.csv":
                for line in reader:
                    index[line[0]] = set()
                    index[line[0]].add(line[1])
            elif indexname == "inverted_index.csv":
                for line in reader:
                    index[line[0]] = list()
                    index[line[0]].append(FrequencyInFile(line[1], line[2]))

            return index

    def save(self, indexdata, indexname=None, fields=None):
        """
        Save data in the storage object
        :param fields: Name of the columns in the csv file
        :param indexname: name of the csv file were the index will be saved
        :param indexdata: data to be persisted
        """
        with self.safe_open(filename=indexname, mode='w') as file:
            csv_obj = csv.DictWriter(file, fields)
            csv_obj.writerow(indexdata)

    def safe_mkdir(self):
        """
        method responsible for create directories in a safe way.
        """
        try:
            name = os.path.dirname(self.path)
            os.makedirs(name)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(self.path):
                pass
            else:
                raise

    def safe_open(self, filename=None, mode='+'):
        """
        Open "path" for writing, creating any parent directories as needed.

        :param filename: Name of the index to be open
        :param mode: mode to access the file, i.e., 'r', 'w', 'x', 'a','b' and so on
        :return: An opened file, if it exists.
        """
        if not filename:
            raise FileNotFoundError("A filename was expected")
        self.safe_mkdir()
        return open(self.path + filename, mode)


class FrequencyInFile(object):
    """
    Class that represents the value of a element in the inverted index.
    """

    def __init__(self, freq=1, file_id=None):
        self.freq = freq
        self.file_id = file_id

    def __repr__(self):
        return " " + str(self.freq) + ", " + str(self.file_id) + " "

    def frequency(self):
        """
        Returns the frequency in a specific document
        :return: Frequency for that specific document
        """
        return self.freq

    def doc_id(self):
        """
        Returns the uuid for a specific document
        :return: Uuid of the document
        """
        return self.file_id
