# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module that contains classes responsible for data persistence in the index engine.
"""
import collections
import csv
import os
from abc import ABC, abstractmethod

from FileUtil import get_logger, safe_open


class Dao(ABC):
    """
    Abstract class to define the common interface for a Dao class.
    """

    @abstractmethod
    def read(self, indexname=None):
        """
        Load data from the storage object
        :param indexname: name of the index to be load
        :return: data stored in some place
        """
        pass

    @abstractmethod
    def write(self, indexdata, indexname=None):
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

    def __init__(self):
        log_file = "./log/" + self.__class__.__name__ + ".log"
        self.logger = get_logger(self.__class__.__name__, log_file)

    def read(self, indexname=None, delimiter=None):
        """
        Load data from a simple csv file
        :param indexname: name of the csv file to be loaded
        :param delimiter: delimiter used to separate data in the file (Optional)
        :return: dict with data loaded from the file
        """
        if delimiter is None:
            delimiter = ','

        with safe_open(filepath=indexname, mode='r') as file:
            csv.register_dialect("unix_dialect")
            reader = csv.reader(file, delimiter=delimiter)
            index = collections.defaultdict(set)
            for line in reader:
                index[line[0]] = eval(line[1])

            return index

    def write(self, indexdata, indexname=None):
        """
        Save data in the storage object
        :param indexname: name of the csv file were the index will be saved
        :param indexdata: data to be persisted (in dict format)
        """
        with safe_open(filepath=indexname, mode='w') as file:
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
