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

import collections


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
    def save(self, indexdata, indexname=None):
        """
        Save data in the storage object
        :param indexname: name of the index to be saved
        :param indexdata: data to be persisted
        """
        pass

    @abstractmethod
    def delete_all(self, container_name):
        """
        Delete all records in the container specified by container_name

        :param container_name: Name of the container that holds the data to be removed
        """


class CSVFileDal(Dao):
    """
    A concrete implementation of Dao abstract class that persist data in a simple csv file.
    """

    def __init__(self, path):
        self.path = path

    def load(self, indexname=None):
        """
        Load data from a simple csv file
        :param indexname: name of the csv file to be loaded
        :return: dict with data loaded from the file
        """
        with self.safe_open(indexname, mode='r') as file:
            csv.register_dialect("unix_dialect")
            reader = csv.reader(file, delimiter=',')
            index = collections.defaultdict(set)
            for line in reader:
                index[line[0]] = eval(line[1])

            return index

    def save(self, indexdata, indexname=None):
        """
        Save data in the storage object
        :param indexname: name of the csv file were the index will be saved
        :param indexdata: data to be persisted (in dict format)
        """
        with self.safe_open(filename=indexname, mode='w') as file:
            csv.register_dialect("unix_dialect")
            writer = csv.writer(file)
            for key, value in indexdata.items():
                writer.writerow([key, value])
            file.close()

    def delete_all(self, indexname):
        """
        Delete the storage object.

        :param indexname: Name of the index file to be removed
        """
        try:
            if os.path.exists(indexname):
                os.remove(indexname)
            else:
                pass
        except OSError:
            raise

    def safe_mkdir(self):
        """
        method responsible for create directories in a safe way.
        """
        try:
            os.makedirs(self.path)
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
        fullpath = self.path + "/" + filename
        if not fullpath:
            raise FileNotFoundError("A filename was expected")
        self.safe_mkdir()
        return open(fullpath, mode)
