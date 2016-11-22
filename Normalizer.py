# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module that contains classes responsible for the normalization of the tokens found inside of a
document
"""
from abc import ABCMeta, abstractmethod

from nltk import SnowballStemmer


class Normalizer(metaclass=ABCMeta):
    """
    Abstract class to define a interface for normalizers.
    """

    @abstractmethod
    def normalize(self, token):
        """
        Apply normalization techniques over the token to simplify its structure.
        :param token:
        :return: A stem or lemma of the token, or the token, if a stem or lemma could not be
        produced.
        """
        pass

    @abstractmethod
    def normalize_list(self, tokens):
        """
        Normalize a entire list of tokens.
        :param tokens: A list of tokens to be normalized
        :return: Yields a normalized token
        """
        pass


class SnowballStemmerNormalizer(Normalizer):
    """
    A Normalizer that uses the NLTK SnowballStemmer to normalize tokens.
    """

    def __init__(self, language='english'):
        self.language = language
        self.stemmer = SnowballStemmer(self.language)

    def normalize(self, token):
        """
        Apply normalization techniques over the token to simplify its structure.
        :param token:
        :return: A stem of the token, or the token, if a stem could not be produced.
        """

        return self.stemmer.stem(token)

    def normalize_list(self, tokens):
        """
        Normalize a entire list of tokens.
        :param tokens: A list of tokens to be normalized
        :return: Yields a normalized token
        """
        for token in tokens:
            yield self.stemmer.stem(token)
