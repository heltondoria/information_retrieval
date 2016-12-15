# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module that contains classes responsible to obtain and parse documents to be indexed
"""
import collections
import os
import time
import uuid
from abc import ABCMeta, abstractmethod
from xml.dom.minidom import parse

from FileUtil import get_logger, safe_open
from Tokenizer import EnglishRegexpTokenizer


def list_files(directory):
    """
    Navigate in a directory and returns all files in its path
    :return: Yields a file to be inspected
    """
    for path, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(path, file)


class Crawler(metaclass=ABCMeta):
    """
    Abstract class responsible to define a common interface for crawlers.
    """

    @abstractmethod
    def load(self, path):
        """
        Load a new document in the given path or uri
        :param path: Path from which the files should be loaded
        :return: A dict containing a uuid as key and tuple with the full path name of
          the file and its contents.
        """
        pass

    @abstractmethod
    def parse(self, documents):
        """
        Read documents and tokenize its content
        :param documents: A dict created by the load method
        :return: A new dictionary where the content of the documents are overridden with
        the list of its tokens.
        """
        pass


class SimpleTxtCrawler(Crawler):
    """
    A simple file crawler that parses TXT files
    """

    def __init__(self):
        log_file = "./log/" + self.__class__.__name__ + ".log"
        self.logger = get_logger(self.__class__.__name__, log_file)
        self.tokenizer = EnglishRegexpTokenizer()

    def load(self, path):
        """
        Load a new txt document in the path
        :param path: Path from which the files should be loaded
        :return: A dict containing a uuid as key and tuple with the full path name of
          the file and its contents.
        """
        txt_files = sorted([file for file in list_files(path) if file.endswith('.txt')])

        documents = collections.defaultdict(set)
        if len(txt_files) > 0:
            for file_name in sorted(txt_files):
                txt = open(file_name)
                uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, file_name))
                documents[uid] = (file_name, self.parse(txt.read()))
                txt.close()
        return documents

    def parse(self, content):
        """
        Read document as dict and tokenize its content
        :param documents: A dict created by the load method
        :return: A new dictionary where the content of the document is overridden with
        a list of its tokens.
        """
        start_time = time.time()
        tokenized_content = self.tokenizer.tokenize(content)
        self.logger.info("%s records read successfully in {:.6f}s".format(time.time() - start_time),
                         str(len(tokenized_content)))
        return tokenized_content


class SimpleXMLCrawler(Crawler):
    """
    A simple file crawler that parses XML files from Cystic Fibrosis Collection
    """

    def __init__(self):
        log_file = "./log/" + self.__class__.__name__ + ".log"
        self.logger = get_logger(self.__class__.__name__, log_file)
        self.tokenizer = EnglishRegexpTokenizer()

    def load(self, path):
        """
        Load a new xml document from the path
        :param path: Path from which the files should be loaded
        :return: A dict containing a key and tuple with the full path name of
          the file and its contents.
        """
        xml_files = sorted([file for file in list_files(path) if file.endswith('.xml')])
        documents = collections.defaultdict(set)
        if len(xml_files) > 0:
            for file_name in sorted(xml_files):
                with safe_open(file_name, mode='r') as file:
                    documents.update(self.parse(file))
                    file.close()
        return documents

    def parse(self, file):
        """
        Parse data from a xml file
        :param file: xml file to be parsed
        :return: dict with data loaded from the file
        """
        dictionary = {}
        dom_tree = parse(file)
        collection = dom_tree.documentElement

        records = collection.getElementsByTagName("RECORD")

        start_time = time.time()
        for record in records:
            record_number = record.getElementsByTagName('RECORDNUM')[0].childNodes[0].data
            paper_number = record.getElementsByTagName("PAPERNUM")[0].childNodes[0].data
            try:
                dictionary[record_number] = (paper_number, self.tokenizer.tokenize(
                    record.getElementsByTagName('ABSTRACT')[0].childNodes[0].data))
            except IndexError:
                try:
                    dictionary[record_number] = (paper_number, self.tokenizer.tokenize(
                        record.getElementsByTagName('EXTRACT')[0].childNodes[0].data))
                except IndexError:
                    self.logger.warning("Document[" + record_number + "] doesn't have abstract neither extract!")
        self.logger.info("%s records read successfully in {:.6f}s".format(time.time() - start_time),
                         str(len(dictionary)))
        return dictionary
