# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module that contains classes responsible for tokenize strings
"""
from abc import ABCMeta, abstractmethod

from nltk import RegexpTokenizer, corpus


class Tokenizer(metaclass=ABCMeta):
    """
     Abstract classe responsible to define a common interface for all tokenizers
     """
    @abstractmethod
    def filter(self, content):
        """
        Remove words in self.stopwords
        :return: a list of words without words in self.stopwords list
        """
        pass

    @abstractmethod
    def tokenize(self, content):
        """
        Tokenize words after pass then through the filter
        :return: A list os tokens
        """
        pass


class EnglishRegexpTokenizer(Tokenizer):
    """
    A Tokenizer class that uses a NLTK RegexpTokenizer to tokenize strings in english, with
    stopwords comming from  NLTK corpus.stopwords.words('english')
    """

    def __init__(self):
        self.regexp_tokenizer = RegexpTokenizer(r'\w+')
        self.stopwords = set(corpus.stopwords.words('english'))

    def filter(self, tokens):
        """
        Remove words in self.stopwords
        :return: a list of words without words in self.stopwords list
        """

        return [token for token in tokens if token not in self.stopwords]

    def tokenize(self, content):
        """
        Tokenize words after pass then through the filter
        :return: A list os tokens
        """
        return self.filter(self.regexp_tokenizer.tokenize(content))
