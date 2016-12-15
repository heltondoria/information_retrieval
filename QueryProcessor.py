# -*- coding: utf-8 -*-
# Author: Helton Dória Costa <helton.doria@gmail.com>
# Copyright (C) 2016-2016
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT
"""
Module to contain code related to processing xmls design to contain queries in a specific structure
"""
import csv
import operator
from xml.dom.minidom import parse

from FileUtil import get_logger, safe_open


def count_score(score_value):
    """
    Calculates the score for the expected results.

    :return: An integer representing a score for a particular item
    """
    score = 0
    score_list = list(score_value)
    for i in score_list:
        score += int(i)
    return score


class QueryProcessor(object):
    """
    Class responsible for process set of queries stored as xml with a specific structure
    """

    def __init__(self, xml_query, csv_query, csv_expected_results):
        """
        Creates a new instance of QueryProcessor.
        """
        log_file = "./log/" + self.__class__.__name__ + ".log"
        self.logger = get_logger(self.__class__.__name__, log_file)
        self.xml_query_file = xml_query
        self.csv_query_file = csv_query
        self.csv_expected_results_file = csv_expected_results

    def parse_xml(self):
        """
        Process the xml that contains the queries that must be submitted to the search engine.

        :return A dictionary with the queries to be used by the search engine
        """
        self.logger.info('Reading ' + self.xml_query_file + '...')

        dictionary = {}

        dom_tree = parse(self.xml_query_file)
        collection = dom_tree.documentElement

        queries = collection.getElementsByTagName("QUERY")

        self.logger.info('Processing score list of expected results...')

        for query in queries:
            query_number = query.getElementsByTagName('QueryNumber')[0].childNodes[0].data
            expected = {}
            try:
                query_text = query.getElementsByTagName('QueryText')[0].childNodes[0].data
                query_text = query_text.replace('\n', '').upper()
                query_text = query_text.replace('"', '\'').upper()
                query_text = " ".join(query_text.split())
                try:
                    records = query.getElementsByTagName('Item')
                    for record in records:
                        if record.hasAttribute("score"):
                            score = record.getAttribute("score")
                            key = record.childNodes[0].data
                            expected.update({key: count_score(score)})
                    dictionary[query_number] = [query_text, expected]
                except IndexError:
                    self.logger.warning('Document["+query_number+"] doesn\'t have records!')
            except IndexError:
                self.logger.warning("Document[" + query_number + "] doesn't have query text!")

        return dictionary

    def write_queries_csv(self, queries):
        """
        Creates a csv file with the queries extracted from the xml

        :param queries: dictionary with the queries extracted from the xml
        """
        with safe_open(filepath=self.csv_query_file, mode='w') as file:
            csv.register_dialect("unix_dialect")
            writer = csv.writer(file)
            for key in queries.keys():
                writer.writerow([key, '"' + queries[key][0] + '"'])
            file.close()

    def write_results_csv(self, queries, filepath):
        """
        Creates a csv file with the expected results from the queries

        :param queries: dictionary with the queries extracted from the xml
        """
        with safe_open(filepath=filepath, mode='w') as file:
            csv.register_dialect("unix_dialect")
            writer = csv.writer(file)
            for key in queries.keys():
                try:
                    writer.writerow([key, sorted(queries[key][1].items(), key=operator.itemgetter(1), reverse=True)])
                except AttributeError:
                    writer.writerow([key, queries[key]])

            file.close()

    def process_queries(self):
        """
        Process the queries and write down the queries and the expected results as csv files
        """
        queries = self.parse_xml()
        self.write_queries_csv(queries)
        self.write_results_csv(queries, self.csv_expected_results_file)
