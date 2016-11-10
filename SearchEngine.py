# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2016 
# Author: Helton Costa <helton.doria@gmail.com>
# URL: <>
# For license information, see LICENSE.TXT
from nltk import SnowballStemmer

from IndexEngine import IndexEngine


class SearchEngine:
    """
    An search engine that search for words in a set of documents based on a given index.
    """

    def __init__(self, stemmer=None, index_engine=IndexEngine()):
        """
        Creates a new instance of the SearchEngine.
        :param stemmer: A stemmer to be used to normalize the searched terms. If either a stemmer is
        not provided, uses NLTK SnowballStemmer as default.
        :param index_engine: the index engine to be used to search for the words.
        """
        self.index_engine = index_engine
        self.language = index_engine.language
        self.stemmer = stemmer

    def search_single_word(self, token):
        """
        Search for a single word in the index to locate the documents that contains that word.

        :param token: word to searched for.
        :return: A set of documents where the word can be found.

        """
        token = token.lower()

        if not self.stemmer:
            self.stemmer = self.index_engine.stemmer

        if not self.stemmer:
            self.stemmer = SnowballStemmer(self.language)

        stem = self.stemmer.stem(token)

        documents = set()
        for token in self.index_engine.inverted_index.keys():
            if stem == token:
                for item in self.index_engine.inverted_index[token]:
                    documents.add(self.index_engine.forward_index.get(item.file_id))

        return documents
