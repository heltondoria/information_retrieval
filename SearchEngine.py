#!/usr/bin/env python
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

    def __init__(self, lemmatizer=None, stemmer=None, index_engine=IndexEngine()):
        """
        Creates a new instance of the SearchEngine.
        :param lemmatizer: A lemmatizer to be used to normalize the searched terms (optional)
        :param stemmer: A stemmer to be used to normalize the searched terms. If either a lemmatizer or a stemmer are
        not given, uses NLTK SnowballStemmer as default.
        :param index_engine: the index engine to be used to search for the words.
        """
        self.index_engine = index_engine
        self.language = index_engine.language
        self.lemmatizer = lemmatizer
        self.stemmer = stemmer

    def search_single_word(self, word):
        """
        Search for a single word in the index to locate the documents that contains that word.

        :param word: word to searched for.
        :return: A set of documents where the word can be found.

        """
        word = word.lower()
        if not self.lemmatizer:
            self.lemmatizer = self.index_engine.lemmatizer

        if not self.stemmer:
            self.stemmer = self.index_engine.stemmer

        if not self.stemmer and not self.lemmatizer:
            self.stemmer = SnowballStemmer(self.language)

        if self.lemmatizer:
            word = self.lemmatizer.lemmatize(word)
        elif self.stemmer:
            word = self.stemmer.stem(word)

        documents = set()
        for uid in self.index_engine.inverted_index.get(word):
            documents.add((self.index_engine.documents.get(uid)).name)

        return documents
