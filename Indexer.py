#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Trabalho para o Bloco D da pós graduação MIT em BigData sobre ferramentas de busca e indexação.
# Instituição: Infnet
#
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria>

import collections
import errno
import json
import os
import pickle

from nltk import RegexpTokenizer, tokenize
from nltk import corpus
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer


class Indexer:
    """
    An class that construct a inverted index based on a path containing a
    list of text files, a stemmer or lemmatizer and a list of stopwords
    """

    def __init__(self, path='./resources/', tokenizer=None, stemmer=None, lemmatizer=None, language='english',
                 stopwords=None, writepath='./results/'):
        """
        Creates a new instance of the Indexer.

        :param path: path to documents. If not given, local resources folder will be used as default.
        :param tokenizer: tokenizer function. If one is not provided, the NLTK SpaceTokenizer will be used as default.
        :param stemmer: stemmer to be used. If one is not provided, the NLTK SnowballStemmer will be used as default.
        :param lemmatizer: lemmatizer to be used. If one is not provided, none will be used.
        :param language: language from where the stopwords will be chosen. If not given, english will be choose as
        default.
        :param stopwords: list of words to be ignored. If one is not provided, nltk.corpus.stopwords will be used as
        default.
        :param writepath: path to write a copy of the index.

        """
        self.path = path
        self.language = language
        self.documents = {}
        self.__document_uid = 1
        self.invertedindex = collections.defaultdict(set)
        self.lemmatizer = lemmatizer
        self.writepath = writepath

        if not tokenizer:
            self.tokenizer = tokenize.simple.SpaceTokenizer()
        else:
            self.tokenizer = tokenizer

        if not stemmer:
            self.stemmer = SnowballStemmer(language)
        else:
            self.stemmer = stemmer

        if not stopwords:
            self.stopwords = set(corpus.stopwords.words(language))
        else:
            self.stopwords = set(stopwords)

    def __mkdir(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def __safe_open(self, path, qualifier):
        """
        Open "path" for writing, creating any parent directories as needed.

        :param path: path to be opened
        :return: An opened file, if it exists.
        """
        self.__mkdir(os.path.dirname(path))
        return open(path, qualifier)

    def __write_binary_index(self):
        """
        Writes a bynary version of the inverted index to reload later.
        """
        obj = self.invertedindex
        with self.__safe_open(self.writepath + 'index.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def __load_binary_index(self):
        """
        If exists, load the binary version of the inverted index to continue from the last load.
        """
        try:
            with self.__safe_open(self.writepath + 'index.pkl', 'rb') as f:
                self.invertedindex = pickle.load(f)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass

    def __loadfiles(self, loadpath):
        """
        Load files into the documents collection

        :param loadpath: path to load documents from
        """
        for file_name in sorted(os.listdir(loadpath)):
            file = open(loadpath + file_name)
            self.documents[str(self.__document_uid)] = file
            self.__document_uid += 1

    def __write_json_file(self):
        """
        Write the inverted index as a JSON file to be human readable.
        """

        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        with self.__safe_open(self.writepath + 'index.json', 'w') as f:
            json.dump(self.invertedindex, f, default=set_default)

    def add_documents(self, path=None):
        """
        Add documents to the index

        :param path: path to documents. If not given, local resources folder will be used as default.

        """
        if not path:
            path = self.path

        self.__loadfiles(path)

        self.__load_binary_index()
        for k, v in self.documents.items():
            for token in [term.lower() for term in self.tokenizer.tokenize(v.read())]:
                if token in self.stopwords:
                    continue

                if self.stemmer:
                    stem = self.stemmer.stem(token)

                if k not in self.invertedindex[stem]:
                    self.invertedindex[stem].add(k)

                if self.lemmatizer:
                    lemma = self.lemmatizer.lemmatize(token)
                    if k not in self.invertedindex[lemma]:
                        self.invertedindex[lemma].add(k)
        self.__write_json_file()
        self.__write_binary_index()

    def search(self, word):
        """
        Search for a single word in the indexed documents.

        :param word: word to searched for.
        :return: A set of documents where the word can be found.

        """
        word = word.lower()
        words = set()
        if self.lemmatizer:
            words.add(self.lemmatizer.lemmatize(word))
        if self.stemmer:
            words.add(self.stemmer.stem(word))

        documents = set()
        for word in words:
            for uid in self.invertedindex.get(word):
                documents.add((self.documents.get(uid)).name)

        return documents


index = Indexer(tokenizer=RegexpTokenizer(r'\w+'), lemmatizer=WordNetLemmatizer())
index.add_documents()
index.add_documents('./extra_files/')
print("{" + "\n".join("{}: {}".format(k, v) for k, v in index.invertedindex.items()) + "}")
search_word = "engrossed"
print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join("{} ".format(w) for w in index.search(search_word)))
