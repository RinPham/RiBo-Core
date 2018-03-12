#! /usr/bin/python
from elasticsearch.client import Elasticsearch
from django.conf import settings
import math
from shinobi_api.services.utils import Utils

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__ = "trung"
__date__ = "$Jul 05, 2016 11:33:10 AM$"

DT_FORMAT_ES = "yyyy-MM-dd HH:mm:ss"
DT_FORMAT_PY = "%Y-%m-%d %H:%M:%S"

_elastic = None
def _engine():
    ":rtype elasticsearch.Elasticsearch"
    global _elastic
    if (not _elastic):
        _elastic = Elasticsearch([{"host": settings.ELASTIC_HOST, "port": int(settings.ELASTIC_PORT)}])
    return _elastic

class SearchResult(object):
    total_item = 0
    total_page = 0
    per_page = 1
    cur_page = 1
    items = []
    def __init__(self, total_item=0, per_page=1, cur_page=1, items=[]):
        self.total_item = total_item
        self.per_page = per_page
        self.cur_page = cur_page
        self.items = items
        self.cal_total_page()
    
    def cal_total_page(self):
        self.total_page = int(math.ceil(self.total_item/float(self.per_page)))
        return self.total_page
