# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2016
# Author: Helton Costa <helton.doria@gmail.com>
# URL: <http://github.com/heltondoria/information_retrival>
# For license information, see LICENSE.TXT


class FrequencyInFile:
    def __init__(self, freq=1, file_id=None):
        self.freq = freq
        self.file_id = file_id

    def __repr__(self):
        return " " + str(self.freq) + ", " + str(self.file_id) + " "
