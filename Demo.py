#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module responsible for the demonstration of the index/search engines at work
"""

from Crawler import SimpleTxtCrawler, SimpleXMLCrawler
from FileUtil import get_logger
from IndexEngine import IndexEngine
from Normalizer import SnowballStemmerNormalizer
from SearchEngine import SearchEngine


class Demo:
    """
    Class responsible for the first set of demonstrations
    """

    def __init__(self, indexer=None, searcher=None):
        log_file = "./log/" + self.__class__.__name__ + ".log"
        self.logger = get_logger(self.__class__.__name__, log_file)
        self.indexer = indexer
        self.searcher = searcher

    def demo1(self):
        """
        Demonstrates the work of the indexer and searcher with txt data files.
        """
        print("\n#######################################################################\n")
        print("                                DEMO 1                                     ")
        print("\n#######################################################################\n")
        self.indexer = IndexEngine(normalizer=SnowballStemmerNormalizer(), data_path='./data',
                                   crawler=SimpleTxtCrawler())
        self.searcher = SearchEngine()
        self.indexer.reset()
        self.indexer.index_documents()

        search_word = "blue"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in sorted(self.searcher.search(search_word))))

    def demo2(self):
        """
        Demonstrates the work of the indexer and searcher with xml data files.
        """
        print("\n#######################################################################\n")
        print("                                DEMO 2                                     ")
        print("\n#######################################################################\n")
        self.indexer = IndexEngine(normalizer=SnowballStemmerNormalizer(), data_path='./data',
                                   crawler=SimpleXMLCrawler())
        self.searcher = SearchEngine()
        self.indexer.reset()
        self.indexer.index_documents()
        self.searcher.batch_search()

        # search_phrase = "The beautiful blue butterfly"
        # print("\nSearch word: '" + search_phrase + "', search result: \n" + "\n".join(
        #     "{} ".format(w) for w in self.searcher.search(search_phrase)))


def main():
    """
    Main class responsible to execute everything
    """
    demo = Demo()
    # demo.demo1()
    demo.demo2()


if __name__ == '__main__':
    main()
