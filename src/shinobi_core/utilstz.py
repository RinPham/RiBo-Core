# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#


__author__ = "hien"
__date__ = "07 05 2016, 10:01 AM"
__all__ = [
    'round_time', 'timebetween'
]

import re, pytz
from pytz import *
import datetime
from datetime import timedelta
COUNTRIES_SUPPORTED = ['US', 'CANADA']

def time_to_float(hour, minute):
    """
    Convert time to float number
    :param hour:
    :param minute:
    :return:
    """
    if not isinstance(hour, float):
        hour = float(hour)
    if not isinstance(minute, float):
        minute = float(minute)
    minute = minute * 1 / 60
    if hour > 0:
        return hour + minute
    else:
        return hour - minute


def float_to_time(hour):
    h = int(hour)
    m = hour - h
    return h, abs(int(m * 60))

def round_time(hour, minute, error=30, *args):
    if not isinstance(hour, float):
        hour = int(hour)
    if not isinstance(minute, int):
        minute = int(minute)
    if error == 30:
        if 45 <= minute <= 59:
            if hour > 0:
                hour += 1
            else:
                hour -= 1
            minute = 0
        if 0 < minute <= 15:
            minute = 0
        if 16 <= minute < 45:
            minute = 30
    else:
        _error = error / 2
        if (60 - _error) <= minute <= 59:
            if hour >= 0:
                hour += 1
            else:
                hour -= 1
            minute = 0
        else:
            range = 60 / error
            i = 1
            while i <= range:
                _minute = i * error
                _minute2 = ((i - 1 ) * error) + _error
                if minute < _minute2:
                    minute = (i - 1 ) * error
                    break
                elif minute > _minute2 and minute <= _minute:
                    minute = _minute
                    break
                i += 1
    return hour, minute


def timebetween(a, b):
    start = a.split(':')
    end = b.split(':')
    start = time_to_float(start[0], start[1])
    end = time_to_float(end[0], end[1])
    return float_to_time(start - end)


def get_local_time(timezone_str, utc_time):
    """
    Shift to local timezone from 'now' by 'timezone_id'
    :param timezone_id:
    :param now:
    :return:
    """
    if timezone_str:
        return utc_time.astimezone(pytz.timezone(timezone_str))
    return utc_time

def time_is_between(now, start, end):
    """
    Check now is between start and end
    :param now: string format 'H:M' or datetime.now instance
    :param start: string format 'H:M'
    :param end: string format 'H:M'
    :return: boolean
    """
    if not isinstance(now, basestring):
        now = now.strftime('%H:%M')
    now = time_to_float(*now.split(':'))
    start = time_to_float(*start.split(':'))
    end = time_to_float(*end.split(':'))
    return (start <= now <= end) or (start >= now >= end)


def get_tz_list():
    all_tz = pytz.all_timezones
    regstr = '(?i){}'.format("/|".join(COUNTRIES_SUPPORTED))
    countries_regx = re.compile(regstr)
    tz_supported = filter(lambda x:  countries_regx.match(x) , all_tz)
    now = datetime.datetime.now(pytz.UTC)
    tz_lst = []
    for tz in tz_supported:
        country, timezone_name = tz.split("/")
        offset = now.astimezone(pytz.timezone(tz)).strftime('%z')
        offset_value = int(offset[:3])
        if str(tz) == "US/Pacific-New":
            continue
        tz_str = '(UTC{}) {}'.format(':'.join([offset[:3], offset[3:]]), tz)
        tz_lst.append(dict(
            timezone=tz,
            offset_value=offset_value,
            tz_str=tz_str,
            country=country,
            timezone_name=timezone_name
        ))
    tz_lst = sorted(tz_lst, key=lambda k: (k['country'],k['offset_value']), reverse=True)
    #tz_lst.reverse()
    return tz_lst

def location_to_tz(country, state):
    try:
        from datetime import datetime
        import pytz # $ pip install pytz
        from geopy import geocoders # $ pip install geopy

        # find timezone given country and subdivision
        g = geocoders.GoogleV3()
        location_str = '{0}/{1}'.format(country,state)
        place, (lat, lng) = g.geocode(location_str)
        timezone = g.timezone((lat, lng))
        return timezone
    except:
        return None