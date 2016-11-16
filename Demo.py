#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module responsible for the demonstration of the index/search engines at work
"""
from Crawler import SimpleTxtCrawler
from Dal import CSVFileDal
from IndexEngine import IndexEngine
from Normalizer import SnowballStemmerNormalizer
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

        self.indexer.reset()
        crawler = SimpleTxtCrawler()
        self.indexer.add_documents(crawler.parse(crawler.load('./resources/')))
        print("{" + "\n".join("{}: {}".format(k, v)
                              for k, v in sorted(self.indexer.inverted_index.items())) + "}")

        search_word = "blue"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in sorted(self.searcher.search_single_word(search_word))))

    def demo2(self):
        """
        Second demonstration: add more documents to the index and the search for the word
        "exquisite". This should point to 3 documents based on the loaded documents
        in the index
        """
        print("\n#######################################################################\n")
        print("                                DEMO 2                                     ")
        print("\n#######################################################################\n")

        self.indexer.reset()
        crawler = SimpleTxtCrawler()
        self.indexer.add_documents(crawler.parse(crawler.load('./resources/')))
        self.indexer.add_documents(crawler.parse(crawler.load('./extra_files/')))
        print("\n{" + "\n".join("{}: {}".format(k, v)
                                for k, v in sorted(self.indexer.inverted_index.items())) + "}")
        print("\n{" + "\n".join("{}: {}".format(k, v)
                                for k, v in sorted(self.indexer.forward_index.items())) + "}")

        search_word = "exquisite"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search_single_word(search_word)))

    def demo3(self):
        """
        Third demonstration: Reset the indexes, load the initial files again and
        demonstrate that when searching for the word blue, the result should point
        to the same 2 documents saw in demo1.
        """
        print("\n#######################################################################\n")
        print("                                DEMO 3                                     ")
        print("\n#######################################################################\n")

        self.indexer.reset()
        crawler = SimpleTxtCrawler()
        self.indexer.add_documents(crawler.parse(crawler.load('./resources/')))
        print("\n{" + "\n".join("{}: {}".format(k, v)
                                for k, v in sorted(self.indexer.forward_index.items())) + "}")
        print("\n\n{" + "\n".join("{}: {}".format(k, v)
                                  for k, v in sorted(self.indexer.inverted_index.items())) + "}")

        search_word = "blue"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search_single_word(search_word)))


def main():
    """
    Main class responsible to execute everything
    """
    indexer = IndexEngine(normalizer=SnowballStemmerNormalizer(), dal=CSVFileDal(path='./index'))
    searcher = SearchEngine(index_engine=indexer)
    demo = Demo(indexer, searcher)
    demo.demo1()
    demo.demo2()
    demo.demo3()


if __name__ == '__main__':
    main()
