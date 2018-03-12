#! /usr/bin/python
import json

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Sep 11, 2015 3:06:34 PM$"

import pprint
from django.test import TransactionTestCase

class BaseTestCase(TransactionTestCase):
    reset_sequences = False
    
    @staticmethod
    def dump(v):
        try:
            print(json.dumps(v, indent=4))
        except:
            pp = pprint.PrettyPrinter(indent=4)
            if (hasattr(v, "__dict__")):
                pp.pprint(v.__dict__)
            else:
                pp.pprint(v)
