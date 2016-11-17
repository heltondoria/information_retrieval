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

from nltk import SnowballStemmer

from IndexEngine import IndexEngine


class SearchEngine:
    """
    An search engine that search for words in a set of documents based on a given index.
    """

    def __init__(self, stemmer=None, index_engine=IndexEngine(), language='english'):
        """
        Creates a new instance of the SearchEngine.
        :param stemmer: A stemmer to be used to normalize the searched terms. If either a stemmer is
        not provided, uses NLTK SnowballStemmer as default.
        :param index_engine: the index engine to be used to search for the words.
        """
        self.index_engine = index_engine
        self.language = language
        self.stemmer = stemmer

    def search_single_word(self, token):
        """
        Search for a single word in the index to locate the documents that contains that word.

        :param token: word to searched for.
        :return: A set of documents where the word can be found.

        """
        token = token.lower()

        if not self.stemmer:
            self.stemmer = SnowballStemmer(self.language)

        stem = self.stemmer.stem(token)

        documents = collections.defaultdict(set)
        for token in self.index_engine.inverted_index.keys():
            if stem == token:
                for entry in self.index_engine.inverted_index[token]:
                    documents[entry[3]] = (self.index_engine.forward_index.get(entry[1]))

        return self.ranking(documents)

    def search_sentence(self, sentence=None):
        """
        Search by the words in the sentence and bring a result ordered by relevance
        :param sentence: string of words to be searched for
        :return: A list of references ordered by relevance
        """
        pass

    def score(self, query_terms):
        """
        Calculate the score of a document d as the sum of the tf-idf weight of each term
        in d that appears in query_terms.

        :param query_terms: list of term being searched
        :return: return a number representing the score of a document
        """
        pass

    def ranking(self, query_result):
        """
        Sort the query result vector based on the score of each document in the query_result.
        :param query_result: list of documents that is a result of a query
        :return: The query_result vector ordered by the score of each document
        """
        return sorted(query_result.items(), key=operator.itemgetter(0))
