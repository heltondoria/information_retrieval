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
import time
from math import log10

from nltk.probability import FreqDist

from Crawler import SimpleXMLCrawler
from Dal import CSVFileDal
from FileUtil import get_logger
from Normalizer import Normalizer, SnowballStemmerNormalizer


class IndexEngine(object):
    """
    An Index Engine that creates a forward index and a inverted index based on files in a given
    path
    """

    def __init__(self, normalizer=None, data_path=None, crawler=None):
        """
        Creates a new instance of the IndexEngine. The IndexEngine is responsible for maintain,
        classify an order the indexes.

        :param normalizer: an object from a class that inherits from Normalizer. It will be used
        strip the texts from unnecessary characters and terms to enhance the assertiveness of the
        index.
        :param data_path: path were the data to be indexed are stored.
        """
        log_file = "./log/" + self.__class__.__name__ + ".log"
        self.logger = get_logger(self.__class__.__name__, log_file)
        self.inverted_index = collections.defaultdict(set)
        self.forward_index = collections.defaultdict(set)
        self.normalizer = normalizer
        self.indexes_dal = CSVFileDal()
        self.data_path = data_path
        if crawler:
            self.crawler = crawler
        else:
            self.crawler = SimpleXMLCrawler()

    def initialize(self):
        """
        Load data into the two indexes.
        """
        self.logger.info("Initializing indexes from their csv files (If they exist)...")
        self.inverted_index = (self.indexes_dal.read('inverted_index.csv'))
        self.forward_index = (self.indexes_dal.read('forward_index.csv'))

    def __normalize__(self, term):
        """
        Normalize the list or terms in each document to maximize the assertivity of the inverted
        index.
        param: terms: list of terms to be normalized
        return: a stem representing a normalized version of a term
        """
        if not self.normalizer or not isinstance(self.normalizer, Normalizer):
            self.normalizer = SnowballStemmerNormalizer()
        return self.normalizer.normalize(term)

    def index_documents(self):
        """
        Index documents contained in data folder
        """
        document_entries = self.crawler.load(self.data_path)
        forward = {key: {(document_entries[key][0])} for key in document_entries.keys()}
        for key in document_entries.keys():
            freq_dist = FreqDist(document_entries[key][1])
            for token in document_entries[key][1]:
                normalized_token = self.__normalize__(token)
                if len(self.inverted_index) is 0 \
                        or normalized_token not in self.inverted_index.keys():
                    self.inverted_index[normalized_token] \
                        .add((freq_dist.get(token), key, freq_dist.freq(token)))
                else:
                    if not freq_dist.get(token) is None:
                        self.inverted_index[normalized_token] \
                            .add((freq_dist.get(token), key, freq_dist.freq(token)))

            self.forward_index.update(forward)
            self.__calc_tf_idf__()
            self.indexes_dal.write(self.forward_index, './index/forward_index.csv')
            self.indexes_dal.write(self.inverted_index, './index/inverted_index.csv')

    def __calc_idf__(self, token):
        """
        Calculate the inverse document frequency represented by the formula
        idf = log_e(total_num_of_docs/num_docs_with_token)
        :return:
        """
        return log10(len(self.forward_index) / len(self.inverted_index[token]))

    def __calc_tf_idf__(self):
        """
        Calculate the TF-IDF for all tokens in the inverted_index using the formula
        TF-IDF = TF*IDF
        """
        self.logger.info("Using TF_IDF Metric to calculate weights...")
        start_time = time.time()
        for token in self.inverted_index.keys():
            idf = self.__calc_idf__(token)
            occurrences = set()
            for entry in self.inverted_index[token]:
                qty_in_doc = entry[0]
                doc_key = entry[1]
                ntf = entry[2]
                occurrences.add((qty_in_doc, doc_key, ntf, ntf * idf))
            self.inverted_index[token] = occurrences
        self.logger.info("Total time of weighting calculus: {:.3f}s".format(time.time() - start_time))

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
        self.indexes_dal.delete_all("./index/forward_index")
        self.indexes_dal.delete_all("./index/inverted_index")
