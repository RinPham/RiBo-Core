#! /usr/bin/python
from shinobi_api.services.utils import Utils

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/

__author__ = "trung"
__date__ = "$Jul 05, 2016 3:39:07 PM$"

class BaseSearch(object):
    _debug = False
    _highlight = False
    _page = 1
    _per_page = 20
    _offset = -1
    _filter_must = {}
    _filter_must_not = {}
    
    def __init__(self):
        super(BaseSearch, self).__init__()
        self._reset_params()

    def set_debug(self, b):
        self._debug = b
        
    def set_highlight(self, b):
        self._highlight = b 
        
    def _log_debug(self, v):
        if self._debug:
            Utils.dump(v)

    def set_offset(self, offset):
        self._offset = max(Utils.safe_int(offset, 0), -1)
        return self

    def set_page(self, page):
        self._page = max(Utils.safe_int(page, 1), 1)
        return self

    def set_per_page(self, per_page):
        self._per_page = max(Utils.safe_int(per_page, 1), 1)
        return self
    
    def _reset_params(self):
        self._page = 1
        self._per_page = 20
        self._offset = -1
        self._filter_must = {}
        self._filter_must_not = {}
        self._highlight = False

    def _eq(self, field, value):
        self._filter_must[field+"_eq"] = {"term": {field: value}}
        return self

    def _in(self, field, value):
        self._filter_must[field+"_in"] = {"terms": {field: value}}
        return self

    def _gt(self, field, value):
        self._filter_must[field+"_gt"] = {"range": {field: {"gt": value}}}
        return self

    def _between(self, field, min_, max_):
        self._filter_must[field+"_between"] = {"range": {field: {"gt": min_, "lte": max_}}}
        return self

    def _is_filtered(self, field, filter_="eq"):
        return ((field+"_"+filter_ in self._filter_must) or (field+"_"+filter_ in self._filter_must_not))

    def _remove_filter(self, field, filter_="eq"):
        self._filter_must.pop(field+"_"+filter_, None)
        self._filter_must_not.pop(field+"_"+filter_, None)
        
    def _build_filter(self):
        out = {}
        if (self._filter_must or self._filter_must_not):
            out["bool"] = {}
            if self._filter_must:
                out["bool"]["must"] = self._filter_must.values()
            if self._filter_must_not:
                out["bool"]["must_not"] = self._filter_must_not.values()
        return out
