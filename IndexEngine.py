# -*- coding: utf-8 -*-
#
# Trabalho para o Bloco D da pós graduação MIT em BigData sobre ferramentas de busca e indexação.
# Instituição: Infnet
#
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module may contain different index engines
"""

import collections

from nltk.probability import FreqDist

from Dal import CSVFileDal, FrequencyInFile


class IndexEngine(object):
    """
    An Index Engine that creates a forward index and a inverted index based on files in a given
    path
    """

    def __init__(self, normalizer=None, classifier=None, dal=None):
        """
        Creates a new instance of the IndexEngine. The IndexEngine is responsible for maintain,
        classify an order the indexes.

        :param normalizer: an object from a class that inherits from Normalizer. It will be used
        strip the texts from unnecessary characters and terms to enhance the assertiveness of the
        index.
        :param classifier: an object from a class that inherits from Classifier. It will be used
        to classify frequency of occurrence of the same word through the indexed documents.
        :param dal: an object from a class that inherits from Dal. It will be used to load and
        persist the indexes. It can be either a connection to a database or a simple file writer.

        """
        self.inverted_index = collections.defaultdict(list)
        self.forward_index = collections.defaultdict(set)
        self.normalizer = normalizer
        self.classifier = classifier
        if not dal:
            self.dal = CSVFileDal('./index')

    def initialize(self):
        """
        Load data into the two indexes.
        """
        self.inverted_index = (self.dal.load('inverted_index.csv'))
        self.forward_index = (self.dal.load('forward_index.csv'))

    def __normalize(self, term):
        """
        Normalize the list or terms in each document to maximize the assertivity of the inverted
        index.
        param: terms: list of terms to be normalized
        return: a stem representing a normalized version of a term
        """
        if self.normalizer:
            return self.normalizer.normalize(term)

    def add_documents(self, document_entries):
        """
        Add new documents to be indexed.
        :param document_entries: a set of objects from the class DocumentEntry
        """
        if document_entries:
            forward = {(document.key, document.name) for document in document_entries}
            inverted = {(self.__normalize(token),
                         FrequencyInFile(countInFile.get(token), document.key))
                        for document in document_entries
                        for countInFile in [FreqDist.update(document)
                                            for document in document_entries.tokens]
                        for token in document.tokens
                        if self.__normalize(token) not in self.inverted_index.keys()}
            self.forward_index.update(forward)
            self.inverted_index.update(inverted)
