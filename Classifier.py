# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Modulo that contains classes responsible for classify the precision of the index engine
"""

# def __classify(self):
#     """
#     Classify the terms inside the inverted index orders it to make easier to find the most
#     common terms when traversing it.
#     """
# def load_documents(self, from_path):
#     """
#     Load files into a documents collection
#
#     :param from_path: path to load documents from
#     """
#     if len(self.forward_index) == 0:
#         if self.persister.load_index():
#             self.forward_index = self.persister.load_index()
#
#     documents = collections.defaultdict(set)
#     for file_name in sorted(os.listdir(from_path)):
#         file = open(from_path + file_name)
#         uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, file_name))
#         self.forward_index[uid] = file.name
#         documents[uid] = file
#     return documents

# def create_index(self, path=None):
#     """
#     Add documents to the index
#
#     :param path: Path that contains the documents to be indexed. If not given, local resources
#     folder will be used as default.
#
#     """
#     if not path:
#         path = self.default_path
#
#     self.add_documents(self.load_documents(path))
#
#     self.persister.csv_inverted_index_writer(self.inverted_index)
#     self.persister.csv_forward_index_writer(self.forward_index)
#

#
# def reset(self):
#     """
#     Clear the two index.
#     """
#     self.forward_index = collections.defaultdict(set)
#     self.inverted_index = collections.defaultdict(list)
