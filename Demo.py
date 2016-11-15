#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module responsible for the demonstration of the index/search engines at work
"""

from IndexEngine import IndexEngine
from SearchEngine import SearchEngine


class Demo:
    """
    Class responsible for the first set of demonstrations
    """

    def __init__(self, indexer=None, searcher=None):
        self.indexer = indexer
        self.searcher = searcher

    def demo1(self):
        """
        First demonstration: the search for the word blue should point to 2 documents
        based on the loaded documents in the index
        """
        print("\n#######################################################################\n")
        print("                                DEMO 1                                     ")
        print("\n#######################################################################\n")

        # Demonstrate the indexer capability
        self.indexer.create_index()
        print("{" + "\n".join("{}: {}".format(k, v)
                              for k, v in self.indexer.inverted_index.items()) + "}")

        search_word = "blue"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search_single_word(search_word)))

    def demo2(self):
        """
        Second demonstration: add more documents to the index and the search for the word
        "exquisite". This should point to 3 documents based on the loaded documents
        in the index
        """
        print("\n#######################################################################\n")
        print("                                DEMO 2                                     ")
        print("\n#######################################################################\n")

        self.indexer.create_index('./extra_files/')
        print("\n{" + "\n".join("{}: {}".format(k, v)
                                for k, v in self.indexer.forward_index.items()) + "}")

        search_word = "exquisite"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search_single_word(search_word)))

    def demo3(self):
        """
        Third demonstration: Restar the index, load the initial files again and
        demonstrate that when searching for the word blue, the result should point
        to the same 2 documents saw in demo1.
        """
        print("\n#######################################################################\n")
        print("                                DEMO 3                                     ")
        print("\n#######################################################################\n")

        self.indexer.reset()
        self.indexer.create_index()
        print("\n{" + "\n".join("{}: {}".format(k, v)
                                for k, v in self.indexer.forward_index.items()) + "}")
        print("\n\n{" + "\n".join("{}: {}".format(k, v)
                                  for k, v in self.indexer.inverted_index.items()) + "}")

        search_word = "blue"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search_single_word(search_word)))


def main():
    """
    Main class responsible to execute everything
    """
    indexer = IndexEngine()
    searcher = SearchEngine(index_engine=indexer)
    demo = Demo(indexer, searcher)
    demo.demo1()
    demo.demo2()
    demo.demo3()


if __name__ == '__main__':
    main()
