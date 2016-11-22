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

        search_word = "blue"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in sorted(self.searcher.search(search_word))))

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

        search_word = "exquisite"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search(search_word)))

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

        search_word = "blue"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search(search_word)))

    def demo4(self):
        """
        Forth demonstration: add more documents to the index and the search for the word
        "ye". This should point to 3 documents ranked based its weight in the query.
        """
        print("\n#######################################################################\n")
        print("                                DEMO 4                                     ")
        print("\n#######################################################################\n")

        self.indexer.reset()
        crawler = SimpleTxtCrawler()
        self.indexer.add_documents(crawler.parse(crawler.load('./resources/')))
        self.indexer.add_documents(crawler.parse(crawler.load('./extra_files/')))

        search_word = "ye"
        print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search(search_word)))

    def demo5(self):
        """
        fifth demonstration: search by a phrase
        """
        print("\n#######################################################################\n")
        print("                                DEMO 5                                     ")
        print("\n#######################################################################\n")

        self.indexer.reset()
        crawler = SimpleTxtCrawler()
        self.indexer.add_documents(crawler.parse(crawler.load('./resources/')))
        self.indexer.add_documents(crawler.parse(crawler.load('./extra_files/')))

        search_phrase = "The beautiful blue butterfly"
        print("\nSearch word: '" + search_phrase + "', search result: \n" + "\n".join(
            "{} ".format(w) for w in self.searcher.search(search_phrase)))


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
    demo.demo4()
    demo.demo5()


if __name__ == '__main__':
    main()
