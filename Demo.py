#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2016 
# Author: Helton Costa <helton.doria@gmail.com>
# URL: <>
# For license information, see LICENSE.TXT
from nltk import RegexpTokenizer, WordNetLemmatizer

from IndexEngine import IndexEngine
from SearchEngine import SearchEngine


class Demo:
    def __init__(self, indexer=None, searcher=None):
        self.indexer = indexer
        self.searcher = searcher


def main():
    indexer = IndexEngine(tokenizer=RegexpTokenizer(r'\w+'), lemmatizer=WordNetLemmatizer())
    searcher = SearchEngine(lemmatizer=WordNetLemmatizer(), index_engine=indexer)
    demo = Demo(indexer, searcher)

    # Demonstrate the indexer capability
    demo.indexer.add_documents()
    print("{" + "\n".join("{}: {}".format(k, v) for k, v in demo.indexer.inverted_index.items()) + "}")

    # the search for the word blue should point to 2 documents, based on the load documents in the index
    search_word = "blue"
    print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
        "{} ".format(w) for w in demo.searcher.search_single_word(search_word)))

    # add more documents without reset the index
    demo.indexer.add_documents('./extra_files/')
    print("\n{" + "\n".join("{}: {}".format(k, v) for k, v in demo.indexer.index.items()) + "}")

    # the search for the word 'blue' should point to 3 documents, based on the load documents in the index
    search_word = "exquisite"
    print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
        "{} ".format(w) for w in demo.searcher.search_single_word(search_word)))

    # restart the index to remake the it based on the default stemmer
    demo.indexer.reset()
    demo.indexer.lemmatizer = None
    demo.indexer.add_documents()
    print("\n{" + "\n".join("{}: {}".format(k, v) for k, v in demo.indexer.index.items()) + "}")
    print("\n\n{" + "\n".join("{}: {}".format(k, v) for k, v in demo.indexer.inverted_index.items()) + "}")

    # the search for the word 'blue' should point to 3 documents, based on the load documents in the index
    search_word = "blue"
    print("\nSearch word: '" + search_word + "', search result: \n" + "\n".join(
        "{} ".format(w) for w in demo.searcher.search_single_word(search_word)))


if __name__ == '__main__':
    main()
