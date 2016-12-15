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
from FileUtil import get_logger
from Normalizer import SnowballStemmerNormalizer
from QueryProcessor import QueryProcessor
from Tokenizer import EnglishRegexpTokenizer


def ranker(query_result, key, tf_idf=1):
    """
    Sort the query result vector based on the score of each document in the query_result.

    :param query_result: list of documents that is a result of a query
    :param key: key for a position in the index
    :param tf_idf: Value of the tf-idf for that particular key
    :return: The query_result vector ordered by the score of each document
    """
    # ranking = {}
    # try:
    #     weight = ranking[key] + tf_idf
    #     ranking.update({key: 1 / weight})
    # except KeyError:
    #     if tf_idf > 0:
    #         ranking.update({key: 1 / tf_idf})
    return sorted(query_result.items(), key=operator.itemgetter(1), reverse=False)


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
        log_file = "./log/" + self.__class__.__name__ + ".log"
        self.logger = get_logger(self.__class__.__name__, log_file)
        self.language = language
        self.normalizer = stemmer
        self.tokenizer = EnglishRegexpTokenizer()
        self.dal = CSVFileDal()
        self.inverted_index = collections.defaultdict(set)
        self.forward_index = collections.defaultdict(set)
        self.queries = None
        if not self.normalizer:
            self.normalizer = SnowballStemmerNormalizer()

    def search(self, sentence=None, query_number=1):
        """
        Search by the words in the sentence and bring a result ordered by relevance
        :param sentence: string of words to be searched for
        :return: A list of references ordered by relevance
        """
        self.load_index()
        result = {}
        if sentence:
            ranking = {}
            tokens = self.tokenizer.tokenize(sentence)
            for stem in self.normalizer.normalize_list(tokens):
                if stem in self.inverted_index.keys():
                    for doc in self.inverted_index[stem]:
                        # doc_set = self.forward_index[doc[1]]
                        try:
                            tf_idf = doc[3]
                            weight = ranking[doc[1]] + tf_idf
                            ranking[doc[1]] = 1 / weight
                        except KeyError:
                            if tf_idf > 0:
                                ranking.update({doc[1]: 1 / tf_idf})
                        # for doc_id in doc_set:
                        #     pass
            if len(ranking) > 0:
                result.update({query_number: sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)})
            else:
                self.logger.warning("word '" + sentence + "' not found!")
        else:
            self.logger.info("Nothing to do!")
        return result

    def batch_search(self, xml_query_storage=None):
        """
        Do a series of searches based on a set of pre-defined queries stored
        in a xml file
        """
        if not xml_query_storage:
            xml_query_storage = "./data/cfquery.xml"
        query_processor = QueryProcessor(xml_query_storage, "./data/queries.csv", "./data/expected_results.csv")
        query_processor.process_queries()
        self.load_queries()
        rankings = {}
        for query_number in self.queries.keys():
            ranking = self.search(self.queries[query_number], query_number)

            rankings.update({query_number: ranking[query_number]})
        query_processor.write_results_csv(rankings, "./result/result.csv")
        return rankings

    def load_index(self):
        """
        Load index from csv files
        """
        self.inverted_index = self.dal.read("./index/inverted_index.csv")
        self.forward_index = self.dal.read("./index/forward_index.csv")

    def load_queries(self):
        """
        load pre-defined queries from a csv file
        """
        self.queries = self.dal.read("./data/queries.csv")
