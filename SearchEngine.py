# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module that contains search engines that will look for information held by the index
"""
import collections
import operator

from Dal import CSVFileDal
from IndexEngine import IndexEngine
from Normalizer import SnowballStemmerNormalizer
from Tokenizer import EnglishRegexpTokenizer


def ranking(query_result):
    """
    Sort the query result vector based on the score of each document in the query_result.
    :param query_result: list of documents that is a result of a query
    :return: The query_result vector ordered by the score of each document
    """
    return sorted(query_result.items(), key=operator.itemgetter(1), reverse=True)


class SearchEngine:
    """
    An search engine that search for words in a set of documents based on a given index.
    """

    def __init__(self, stemmer=None, language='english'):
        """
        Creates a new instance of the SearchEngine.
        :param stemmer: A stemmer to be used to normalize the searched terms. If either a stemmer is
        not provided, uses NLTK SnowballStemmer as default.
        :param language: Language to use during normalization fase
        """
        self.language = language
        self.normalizer = stemmer
        self.tokenizer = EnglishRegexpTokenizer()
        self.dal = CSVFileDal('./index/')
        self.inverted_index = collections.defaultdict(set)
        self.forward_index = collections.defaultdict(set)
        if not self.normalizer:
            self.normalizer = SnowballStemmerNormalizer()

    def search(self, sentence=None):

        """
        Search by the words in the sentence and bring a result ordered by relevance
        :param sentence: string of words to be searched for
        :return: A list of references ordered by relevance
        """
        self.load_index()
        if sentence:
            result = dict()
            tokens = self.tokenizer.tokenize(sentence)
            for stem in self.normalizer.normalize_list(tokens):
                if stem in self.inverted_index.keys():
                    for doc in self.inverted_index[stem]:
                        doc_set = self.forward_index[doc[1]]
                        for doc_name in doc_set:
                            if doc_name in result.keys():
                                result[doc_name] = result[doc_name] + doc[3]
                            else:
                                result[doc_name] = doc[3]
            if len(result) > 0:
                return ranking(result)
        else:
            print("Nothing to do")

    def load_index(self):
        """
        Load index from csv files
        """
        self.inverted_index = self.dal.load("inverted_index.csv")
        self.forward_index = self.dal.load("forward_index.csv")
