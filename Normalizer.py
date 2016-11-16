# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Modulo that contains classes responsible for the normalization of the tokens found inside of
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

#
# def add_documents(self, documents):
#     """
#     Add a new set of documents do the inverted index.
#     :param documents: Dict withe a set of documents to be indexed.
#     """
#     freq_dist = FreqDist()
#     for k, v in documents.items():
#         content = v.read()
#         v.close()
#         tknzd_content = self.tokenizer.tokenize(content)
#         freq_dist.update(tknzd_content)
#         for token in [term.lower() for term in tknzd_content if term not in self.stopwords]:
#
#             stem = self.normalize(token)
#
#             if len(self.inverted_index) == 0 or not self.inverted_index[stem]:
#                 self.inverted_index[stem].append(FrequencyInFile(freq_dist.get(token), k))
#             else:
#                 for item in self.inverted_index[stem]:
#                     if k != item.file_id:
#                         self.inverted_index[stem] \
#                             .append(FrequencyInFile(freq_dist.get(token), k))
