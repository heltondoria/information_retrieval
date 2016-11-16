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

from Dal import CSVFileDal
from Normalizer import Normalizer, SnowballStemmerNormalizer


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
        self.dal = dal
        if not self.dal:
            self.dal = CSVFileDal('./index/')

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
        if not self.normalizer or not isinstance(self.normalizer, Normalizer):
            self.normalizer = SnowballStemmerNormalizer()
        return self.normalizer.normalize(term)

    def add_documents(self, document_entries):
        """
        Add new documents to be indexed.
        :param document_entries: a set of objects from the class DocumentEntry
        """
        if document_entries:
            forward = {(key, document_entries[key][0]) for key in document_entries.keys()}
            for key in document_entries.keys():
                freq_dist = FreqDist(document_entries[key][1])
                for token in document_entries[key][1]:
                    if len(self.inverted_index) is 0 \
                            or self.__normalize(token) not in self.inverted_index.keys():
                        self.inverted_index[self.__normalize(token)]\
                            .append((freq_dist.get(token), key))
                    else:
                        if not freq_dist.get(token) is None:
                            self.inverted_index[self.__normalize(token)]\
                                .append((freq_dist.get(token), key))

            self.forward_index.update(forward)
            self.dal.save(self.forward_index, 'forward_index.csv',
                          [key for key in self.forward_index.keys()])
            self.dal.save(self.inverted_index, 'inverted_index.csv',
                          [key for key in self.inverted_index.keys()])

    def lookup_key(self, key):
        """
        Search for a specific key in the inverted index.
        :param key: key to be look up for
        :return: A token representing the key, if it is in the index.
        """
        for token in self.inverted_index.keys():
            if key == token:
                yield token

    def reset(self):
        """
        Reset the indexes to an empty state
        """
        self.inverted_index.clear()
        self.forward_index.clear()
        self.dal.delete_all("./index/forward_index")
        self.dal.delete_all("./index/inverted_index")
