#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Trabalho para o Bloco D da pós graduação MIT em BigData sobre ferramentas de busca e indexação.
# Instituição: Infnet
#
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT

import collections
import os
import uuid

from nltk import corpus
from nltk import tokenize
from nltk.stem.snowball import SnowballStemmer

from IndexPersister import IndexPersister


class IndexEngine:
    """
    An Index Engine that creates a document index and a inverted index based on files in a given path
    """

    def __init__(self, tokenizer=None, stemmer=None, lemmatizer=None, stopwords=None, language='english',
                 path='./resources/', write_path='./index/'):
        """
        Creates a new instance of the IndexEngine.

        :param path: path to documents. If not given, local resources folder will be used as default.
        :param tokenizer: tokenizer function. If one is not provided, the NLTK SpaceTokenizer will be used as default.
        :param stemmer: stemmer to be used. If one is not provided, the NLTK SnowballStemmer will be used as default.
        A stemmer and a Lematizer can not be defined até the same fi.Beecausae  wlw?
        :param lemmatizer: lemmatizer to be used. If one is not provided, none will be used.
        :param language: language from where the stopwords will be chosen. If not given, english will be choose as
        default.
        :param stopwords: list of words to be ignored. If one is not provided, nltk.corpus.stopwords will be used as
        default.
        :param write_path: path to write a copy of the index.

        """
        self.default_path = path
        self.language = language
        self.index = collections.defaultdict(set)
        self.inverted_index = collections.defaultdict(set)
        self.stemmer = stemmer
        self.lemmatizer = lemmatizer
        self.default_write_path = write_path
        self.persister = IndexPersister(self.index, self.inverted_index, self.default_write_path)

        if tokenizer:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = tokenize.simple.SpaceTokenizer()

        if stopwords:
            self.stopwords = set(stopwords)
        else:
            self.stopwords = set(corpus.stopwords.words(self.language))

    def load_documents(self, from_path):
        """
        Load files into a documents collection

        :param from_path: path to load documents from
        """
        if len(self.index) == 0:
            if self.persister.load_index():
                self.index = self.persister.load_index()

        documents = collections.defaultdict(set)
        for file_name in sorted(os.listdir(from_path)):
            file = open(from_path + file_name)
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS, file_name))
            self.index[id] = file.name
            documents[id] = file
        return documents

    def add_documents(self, path=None):
        """
        Add documents to the index

        :param path: Path that contains the documents to be indexed. If not given, local resources folder will be used
        as default.

        """
        if not path:
            path = self.default_path

        if len(self.inverted_index) == 0:
            if self.persister.load_inverted_index():
                self.inverted_index = self.persister.load_inverted_index()

        self.normalize(self.load_documents(path))

        self.persister.write_json_index()
        self.persister.write_binary_index()

    def normalize(self, documents):
        for k, v in documents.items():
            for token in [term.lower() for term in self.tokenizer.tokenize(v.read())]:
                if token in self.stopwords:
                    continue

                if not self.stemmer and not self.lemmatizer:
                    self.stemmer = SnowballStemmer(self.language)

                if self.lemmatizer:
                    token = self.lemmatizer.lemmatize(token)
                elif self.stemmer:
                    token = self.stemmer.stem(token)

                if token:
                    if k not in self.inverted_index[token]:
                        self.inverted_index[token].add(k)

    def reset(self):
        self.index = collections.defaultdict(set)
        self.inverted_index = collections.defaultdict(set)
