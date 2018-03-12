#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com
#
__author__ = "hien"
__date__ = "$Jul 21st, 2016 10:16:08 AM$"

from shinobi_api.services.utils import Utils
from shinobi_api.models.location import Location
from shinobi_api.models.country import Country
from shinobi_api.models.admin1 import Admin1
from shinobi_api.services.base import BaseService
from shinobi_api.services.vmscache import VMSCacheService
import json
from shinobi_api.const import (
    ResourceType
)
class GeoError(TypeError): pass  # base exception class

class GeoService(BaseService):
    
    @classmethod
    def _get_cache_service(cls):
        return VMSCacheService.factory(ResourceType.RS_LOCATION);
    
    @classmethod
    def _get_location_list(cls, locs, get_nearby=True):
        loc_list={}
        try:
            for loc in locs:
                if not loc_list.get(loc.id):
                    loc_list[loc.id] = loc
                if not loc.city:
                    if loc.admin1_code:
                        #cities in states
                        cities = Location.objects.order_by("city").filter(admin1_code=loc.admin1_code, country=loc.country)
                        for city in cities:
                            if not loc_list.get(city.id):
                                loc_list[city.id] = cls.prepare_location(city)
                else:
                    if get_nearby:
                        if loc.nearby:
                            nearby_ids = json.loads(loc.nearby)
                            for city_id in nearby_ids:
                                city_id = int(city_id)
                                if not loc_list.get(city_id):
                                    city = cls.get_location(city_id)
                                    loc_list[city.id] = cls.prepare_location(city)  
        except Exception as e:
            cls.log_exception(e)
        return loc_list
    
    @classmethod
    def get_neary_locs(cls, location_id):
        loc = cls.get_location(location_id)
        if loc:
            return cls._get_location_list([cls.prepare_location(loc)],True)
        return {}
    
    @classmethod
    def get_location(cls, location_id):
        try:
            if location_id:
                cache_service = cls._get_cache_service()
                cached_location = cache_service.get(location_id)
                if(cached_location):
                    loc = cached_location
                else:
                    loc = Location.objects.get(pk=location_id)
                    loc = cls.prepare_location(loc)
                    cache_service.set(location_id,loc)
                return loc
        except Exception as ex:
            Utils.log_exception(ex)
        return None  
        
    
    """
    loc_data = {
        'country': "Vietnam",
        "admin1_name":"An Giang",
        "admin1_code":"AN",
        "city":"An Giang"
    }
    """
    @classmethod
    def get_location_by_meta(cls, loc_data):
        try:
            filter_args = {}
            if loc_data.get('country'):
                filter_args['country'] = loc_data['country']
            if loc_data.get('admin1_code'):
                filter_args['admin1_code'] = loc_data['admin1_code']  
            else:
                if loc_data.get('admin1_name'):
                    filter_args['admin1_name'] = loc_data['admin1_name']
            if ('city' in loc_data):
                filter_args['city'] = loc_data['city']
            loc = Location.objects.get(**filter_args)
        except Exception as e:
            loc = Location(**loc_data)
            loc.save()
            return loc
        return loc
    
    @classmethod
    def prepare_location(cls, loc):
        loc.display_text = Utils.safe_unicode(loc)
        return loc
    
    @classmethod
    def delete_location(cls, location_id):
        try:
            loc = Location.objects.get(pk=location_id)
        except:
            return None
        cache_service = cls._get_cache_service()
        cache_service.delete(loc.id);
        loc.delete()
        return True


    @classmethod
    def count_admin1(cls, **kwargs):
        return Location.objects.values('admin1_name').distinct().count()

    @classmethod
    def get_location_by_offset(cls, offset):
        offset = int(offset)
        if offset > 0:
            offset = offset - 1
        location = Location.objects.values_list('admin1_name', flat=True).distinct()
        return location[offset]

    @classmethod
    def get_admin1_by_country(cls, country_cd='US'):
        try:
            admin1 = Admin1.objects.order_by('admin1_name').filter(country_code=country_cd)
            return admin1
        except:
            return None
        return True