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
import uuid
from abc import ABCMeta, abstractmethod

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
    A simple web crawler that implements the interface of the abstract class Crawler
    """

    def __init__(self):
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
                file = open(file_name)
                uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, file_name))
                documents[uid] = (file_name, file.read())
                file.close()
        return documents

    def parse(self, documents):
        """
        Read document as dict and tokenize its content
        :param documents: A dict created by the load method
        :return: A new dictionary where the content of the document is overridden with
        a list of its tokens.
        """
        tokenized_documents = collections.defaultdict(set)
        for document in documents.items():
            tokenized_documents[document[0]] = (document[1][0], self.tokenizer
                                                .tokenize(document[1][1]))
        return tokenized_documents
