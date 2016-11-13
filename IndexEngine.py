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

from nltk import RegexpTokenizer, corpus
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer

from IndexPersister import IndexPersister


class IndexEngine(object):
    """
    An Index Engine that creates a document index and a inverted index based on files in a given
    path
    """

    def __init__(self, tokenizer=None, stemmer=None, stopwords=None,
                 language='english', path='./resources/', write_path='./index/'):
        """
        Creates a new instance of the IndexEngine.

        :param path: path to documents. If not given, local resources folder will be used as
        default.
        :param tokenizer: tokenizer function. If one is not provided, the NLTK RegexpTokenizer will
         be used as default.
        :param stemmer: stemmer to be used. If one is not provided, the NLTK SnowballStemmer will
        be used as default.
        :param language: language from where the stopwords will be chosen. If not given, english
        will be choose as default.
        :param stopwords: set of words to be ignored. If one is not provided,
        nltk.corpus.stopwords will be used as default.
        :param write_path: path to write a copy of the index.

        """
        self.default_path = path
        self.language = language
        self.inverted_index = collections.defaultdict(list)
        self.forward_index = collections.defaultdict(set)
        self.stemmer = stemmer
        self.default_write_path = write_path
        self.persister = IndexPersister(index=self.forward_index,
                                        inverted_index=self.inverted_index,
                                        path=self.default_write_path)

        if tokenizer:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = RegexpTokenizer(r'\w+')

        if stopwords:
            self.stopwords = set(stopwords)
        else:
            self.stopwords = set(corpus.stopwords.words(self.language))

    def load_documents(self, from_path):
        """
        Load files into a documents collection

        :param from_path: path to load documents from
        """
        if len(self.forward_index) == 0:
            if self.persister.load_index():
                self.forward_index = self.persister.load_index()

        documents = collections.defaultdict(set)
        for file_name in sorted(os.listdir(from_path)):
            file = open(from_path + file_name)
            uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, file_name))
            self.forward_index[uid] = file.name
            documents[uid] = file
        return documents

    def create_index(self, path=None):
        """
        Add documents to the index

        :param path: Path that contains the documents to be indexed. If not given, local resources
        folder will be used as default.

        """
        if not path:
            path = self.default_path

        self.add_documents(self.load_documents(path))

        self.persister.csv_inverted_index_writer(self.inverted_index)
        self.persister.csv_forward_index_writer(self.forward_index)

    def normalize(self, token):
        """
        Apply normalization techniques over the token to simplify its structure.
        :param token:
        :return:
        """
        if not self.stemmer:
            self.stemmer = SnowballStemmer(self.language)
        return self.stemmer.stem(token)

    def add_documents(self, documents):
        """
        Add a new set of documents do the inverted index.
        :param documents: Dict withe a set of documents to be indexed.
        """
        freq_dist = FreqDist()
        for k, v in documents.items():
            content = v.read()
            v.close()
            tknzd_content = self.tokenizer.tokenize(content)
            freq_dist.update(tknzd_content)
            for token in [term.lower() for term in tknzd_content if term not in self.stopwords]:

                stem = self.normalize(token)

                if len(self.inverted_index) == 0 or not self.inverted_index[stem]:
                    self.inverted_index[stem].append(FrequencyInFile(freq_dist.get(token), k))
                else:
                    for item in self.inverted_index[stem]:
                        if k != item.file_id:
                            self.inverted_index[stem] \
                                .append(FrequencyInFile(freq_dist.get(token), k))

    def reset(self):
        """
        Clear the two index.
        """
        self.forward_index = collections.defaultdict(set)
        self.inverted_index = collections.defaultdict(list)


class FrequencyInFile(object):
    """
    Class that represents the value of a element in the inverted index.
    """

    def __init__(self, freq=1, file_id=None):
        self.freq = freq
        self.file_id = file_id

    def __repr__(self):
        return " " + str(self.freq) + ", " + str(self.file_id) + " "
