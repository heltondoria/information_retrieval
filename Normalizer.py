# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Modulo that contains classes responsible for the normalization of the tokens found inside of
document
"""

# if tokenizer:
#     self.tokenizer = tokenizer
# else:
#     self.tokenizer = RegexpTokenizer(r'\w+')
#
# if stopwords:
#     self.stopwords = set(stopwords)
# else:
#     self.stopwords = set(corpus.stopwords.words(self.language))

# def normalize(self, token):
#     """
#     Apply normalization techniques over the token to simplify its structure.
#     :param token:
#     :return:
#     """
#     if not self.stemmer:
#         self.stemmer = SnowballStemmer(self.language)
#     return self.stemmer.stem(token)

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
