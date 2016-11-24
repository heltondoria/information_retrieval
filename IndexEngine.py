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

from math import log10
from nltk.probability import FreqDist

from Dal import CSVFileDal
from Normalizer import Normalizer, SnowballStemmerNormalizer


class IndexEngine(object):
    """
    An Index Engine that creates a forward index and a inverted index based on files in a given
    path
    """

    def __init__(self, normalizer=None, dal=None):
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
        self.inverted_index = collections.defaultdict(set)
        self.forward_index = collections.defaultdict(set)
        self.normalizer = normalizer
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
            forward = {key: {(document_entries[key][0])} for key in document_entries.keys()}
            for key in document_entries.keys():
                freq_dist = FreqDist(document_entries[key][1])
                for token in document_entries[key][1]:
                    if len(self.inverted_index) is 0 \
                            or self.__normalize(token) not in self.inverted_index.keys():
                        self.inverted_index[self.__normalize(token)] \
                            .add((freq_dist.get(token), key, freq_dist.freq(token)))
                    else:
                        if not freq_dist.get(token) is None:
                            self.inverted_index[self.__normalize(token)] \
                                .add((freq_dist.get(token), key, freq_dist.freq(token)))

            self.forward_index.update(forward)
            self.tf_idf()
            self.dal.save(self.forward_index, 'forward_index.csv')
            self.dal.save(self.inverted_index, 'inverted_index.csv')

    def idf(self, token):
        """
        Calc the inverse document frequency represented by the formula
        idf = log_e(total_num_of_docs/num_docs_with_token)
        :return:
        """
        return log10(len(self.forward_index) / len(self.inverted_index[token]))

    def tf_idf(self):
        """
        Calc the TF-IDF for all tokens in the inverted_index using the formula
        TF-IDF = TF*IDF
        """
        for token in self.inverted_index.keys():
            idf = self.idf(token)
            occurrences = set()
            for entry in self.inverted_index[token]:
                qty_in_doc = entry[0]
                doc_key = entry[1]
                ntf = entry[2]
                occurrences.add((qty_in_doc, doc_key, ntf, ntf * idf))
            self.inverted_index[token] = occurrences

    def get_doc(self, key):
        """
        Return a document based in it's key in the forward index.
        :return: The path to the document on the file system
        """
        return self.forward_index[key]

    def reset(self):
        """
        Reset the indexes to an empty state
        """
        self.inverted_index.clear()
        self.forward_index.clear()
        self.dal.delete_all("./index/forward_index")
        self.dal.delete_all("./index/inverted_index")
