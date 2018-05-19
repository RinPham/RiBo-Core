import pytz

__author__ = "thqbop"
__date__ = "$Mar 05, 2018$"
__all__ = ['Utils']

import base64, urllib, json, pprint, random, string, re, logging
from datetime import datetime
from datetime import timedelta
from django.http import request
from django.utils.timesince import timesince
from django.conf import settings
from urllib.parse import urlparse, urlunparse
from decimal import Decimal
logger = logging.getLogger("project")


class Utils:
    request = None

    @staticmethod
    def merge_dict(d1, d2):
        m = d1.copy()
        m.update(d2)
        return m

    @staticmethod
    def media_url(media_path):
        if not isinstance(media_path, str):
            return ''
        if media_path.startswith('http:') or media_path.startswith('https:'):
            return media_path
        return settings.MEDIA_URL + media_path

    @staticmethod
    def chunks(l, n):
        n = max(1, int(n))
        return [l[i:i + n] for i in range(0, len(l), n)]
    
    @staticmethod
    def days_text(tday):
        days_text = "{0} day".format(tday)
        if tday > 1:
            days_text = "{0} days".format(tday)
        return days_text
    
    @staticmethod
    def replace_hyphen(str_data):
        punc_map = {
            "-": " ",
            "_": " "
        }
        for key, value in punc_map.iteritems():
            str_data = str_data.replace(key, value)
        return str_data

    @staticmethod
    def replace_hyphen2(str_data):
        punc_map = {
            "-": "",
            "_": ""
        }
        for key, value in punc_map.iteritems():
            str_data = str_data.replace(key, value)
        return str_data

    @staticmethod
    def remove_punction(str_data):
        if str_data:
            exclude = set(string.punctuation)
            str_data = ''.join(ch for ch in str_data if ch not in exclude)
        return str_data.strip()

    @staticmethod
    def safe_number(val, default=0):
        try:
            return float(val)
        except:
            return default

    @staticmethod
    def validate_password(password, phone):
        try:
            password = str(password)
        except:
            password = ''
        return password

    @staticmethod
    def strip_non_ascii(string):
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    @staticmethod
    def count_words(strs):
        import re
        from string import punctuation
        r = re.compile(r'[{}]'.format(punctuation))
        new_strs = r.sub(' ', strs)
        return len(new_strs.split())

    @staticmethod
    def split_words(strs):
        import re
        from string import punctuation
        r = re.compile(r'[{}]'.format(punctuation))
        new_strs = r.sub(' ', strs)
        return new_strs.split()

    @staticmethod
    def safe_int(val, default=0):
        if isinstance(val, int):
            return val
        try:
            return int(val)
        except:
            return default

    @staticmethod
    def safe_decimal(val, decimal_points, default=0):
        try:
            val = float(val)
            val = format(val, '.{}f'.format(decimal_points))
            return Decimal(val)
        except:
            raise
            return default

    # @staticmethod
    # def safe_unicode(obj, *args):
    #     """ return the unicode representation of obj """
    #     try:
    #         return unicode(obj, *args)
    #     except UnicodeDecodeError:
    #         # obj is byte string
    #         ascii_text = str(obj).encode('string_escape')
    #         return unicode(ascii_text)
    #     except:
    #         return u""

    # @staticmethod
    # def extract_domain(domain_str):
    #     import re
    #     match = re.match('(?:http|https)://', domain_str)
    #     if not match:
    #         domain_str = "{0}{1}".format("http://", domain_str)
    #     from urlparse import urlparse
    #     parsed_uri = urlparse(domain_str)
    #     if parsed_uri.netloc:
    #         return parsed_uri.netloc
    #     return domain_str

    # @staticmethod
    # def safe_str(obj):
    #     """ return the byte string representation of obj """
    #     try:
    #         return str(obj)
    #     except UnicodeEncodeError:
    #         # obj is unicode
    #         return unicode(obj).encode('unicode_escape')
    #     except:
    #         return ""

    @staticmethod
    def id_generator(size=6):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

    @staticmethod
    def num_generator(size=6, salt=''):
        prefix = ''
        if salt:
            import hashlib
            prefix = int(hashlib.sha1(salt).hexdigest(), 16) % (10 ** 8)
        ran_str = ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))
        return str(prefix) + ran_str

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

    @classmethod
    def log_exception(cls, exc):
        logger.error(exc, exc_info=True)

    @staticmethod
    def log(message):
        log = message
        try:
            log = json.dumps(message, indent=4)
        except Exception as e:
            if (hasattr(message, "__dict__")):
                log = message.__dict__
        logger.error(log)

    @staticmethod
    def get_headers(hide_env=True):
        """Returns headers dict from request context."""
        headers = dict(request.headers.items())
        if hide_env and ('show_env' not in request.args):
            for key in ENV_HEADERS:
                try:
                    del headers[key]
                except KeyError:
                    pass
        return CaseInsensitiveDict(headers.items())

    @staticmethod
    def age(value):
        now = datetime.now()
        try:
            difference = now - value
        except Exception as e:
            return value
        if difference <= timedelta(minutes=1):
            return 'just now'
        vage = timesince(value).split(', ')[0]
        vage = vage.replace("minutes", "m").replace("minute", "m")
        vage = vage.replace("days", "d").replace("day", "d")
        vage = vage.replace("hours", "h").replace("hour", "h")
        return vage

    @staticmethod
    def age_in_days(value):
        now = datetime.now()
        try:
            difference = now - value
        except Exception as e:
            return value
        if difference <= timedelta(minutes=1):
            return 0
        vage = timesince(value).split(', ')[0]
        vage = vage.replace("minutes", "m").replace("minute", "m")
        vage = vage.replace("days", "d").replace("day", "d")
        vage = vage.replace("hours", "h").replace("hour", "h")
        return vage

    @staticmethod
    def get_url(request):
        """
        Since we might be hosted behind a proxy, we need to check the
        X-Forwarded-Proto, X-Forwarded-Protocol, or X-Forwarded-SSL headers
        to find out what protocol was used to access us.
        """
        protocol = request.headers.get('X-Forwarded-Proto') or request.headers.get('X-Forwarded-Protocol')
        if protocol is None and request.headers.get('X-Forwarded-Ssl') == 'on':
            protocol = 'https'
        if protocol is None:
            return request.url
        url = list(urlparse(request.url))
        url[0] = protocol
        return urlunparse(url)

    @staticmethod
    def json_safe(string, content_type='application/octet-stream'):
        """Returns JSON-safe version of `string`.
        If `string` is a Unicode string or a valid UTF-8, it is returned unmodified,
        as it can safely be encoded to JSON string.
        If `string` contains raw/binary data, it is Base64-encoded, formatted and
        returned according to "data" URL scheme (RFC2397). Since JSON is not
        suitable for binary data, some additional encoding was necessary; "data"
        URL scheme was chosen for its simplicity.
        """
        try:
            string = string.decode('utf-8')
            _encoded = json.dumps(string)
            return _encoded
        except (ValueError, TypeError):
            return b''.join([
                            b'data:',
                            content_type.encode('utf-8'),
                            b';base64,',
                            base64.b64encode(string)
                            ]).decode('utf-8')

    @staticmethod
    def ca_state(k, get="name"):
        states = {
            'AB': 'Alberta',
            'BC': 'British Columbia',
            'MB': 'Manitoba',
            'NB': 'New Brunswick',
            'NL': 'Newfoundland and Labrador',
            'NS': 'Nova Scotia',
            'ON': 'Ontario',
            'PE': 'Prince Edward Island',
            'QC': 'Quebec',
            'SK': 'Saskatchewan',
            'YT': 'Yukon',
            'NT': 'Northwest Territories',
            'NU': 'Nunavut'
        }
        if (not isinstance(k, str)):
            return None
        if (get == "name"):
            code = k.upper()
            return states[code] if (code in states) else None
        elif (get == "code"):
            name = Utils.normalize_str(k, to_lower=True)
            for (key, val) in states.iteritems():
                val = Utils.normalize_str(val, to_lower=True)
                if (name == val):
                    return key
            return None

    @staticmethod
    def normalize_str(v, to_lower=False):
        v = v.strip()
        v = re.sub(r'\s+', ' ', v)
        if to_lower:
            v = v.lower()
        return v

    @staticmethod
    def list_get(l, idx, default):
        try:
            return l[idx]
        except:
            return default

    @staticmethod
    def dict_get(d, path, default=None):
        try:
            v = d
            for key in path:
                v = v[key]
            return v
        except:
            return default

    @staticmethod
    def us_statename_from_code(code):
        states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming',
            '01': 'Alberta',
            '02': 'British Columbia',
            '03': 'Manitoba',
            '04': 'New Brunswick',
            '05': 'Newfoundland and Labrador',
            '07': 'Nova Scotia',
            '08': 'Ontario',
            '09': 'Prince Edward Island',
            '10': 'Québec',
            '11': 'Saskatchewan',
            '12': 'Yukon',
            '13': 'Northwest Territories',
            '14': 'Nunavut'
        }
        if (not isinstance(code, str)):
            return None
        code = code.upper()
        return states[code] if (code in states) else None

    @staticmethod
    def gen_slug(s):
        if isinstance(s, str):
            s = s.lower()
            s = re.sub(r'[^A-Za-z0-9\s_\-\/,\(\)]', '', s)
            s = re.sub(r'_+', ' ', s)
            s = re.sub(r'\/+', ' ', s)
            s = re.sub(r'\-+', ' ', s)
            s = re.sub(r',+', ' ', s)
            s = re.sub(r'\(+', ' ', s)
            s = re.sub(r'\)+', ' ', s)
            s = re.sub(r'\s+', ' ', s)
            s = s.strip()
            s = re.sub(' ', '-', s)
            return urllib.parse.quote(s)
        return ''

    @staticmethod
    def gen_search_slug(jobtitle_or_keyword, location):
        slug = ''
        if (jobtitle_or_keyword or location):
            if (jobtitle_or_keyword and location):
                slug = Utils.gen_slug(jobtitle_or_keyword) + '-jobs-in-' + Utils.gen_slug(location);
            elif jobtitle_or_keyword:
                slug = Utils.gen_slug(jobtitle_or_keyword) + '-jobs';
            else:
                slug = 'jobs-in-' + Utils.gen_slug(location);
        return slug

    @staticmethod
    def get_public_url(path='', *args, **kwargs):
        protocol = 'http://'
        public_base = settings.PUBLIC_BASE
        if len(path) and path[0] != '/':
            path = '/' + path
        if kwargs.pop('part', '') == 'domain':
            # Return domain
            return public_base
        return protocol + public_base + path

    @classmethod
    def next_weekday(cls, weekday, date=datetime.today()):
        day_gap = weekday - date.weekday()
        if day_gap <= 0:
            day_gap += 7
        return (date + timedelta(days=day_gap))

    @classmethod
    def last_weekday(cls, weekday, date=datetime.today()):
        day_gap = weekday - date.weekday()
        if day_gap >= 0:
            day_gap -= 7
        return (date + timedelta(days=day_gap))

    @classmethod
    def parse_datetime(cls,date_time, tz):
        try:
            date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            try:
                date_time = datetime.strptime(date_time, '%Y-%m-%d')
                date_time = date_time + timedelta(hours=7)
            except ValueError:
                try:
                    date_time = datetime.strptime(date_time, '%H:%M:%S')
                    date_time = datetime.combine(datetime.today(), date_time.time())
                    return date_time
                except ValueError as e:
                    raise e
        local_dt = tz.localize(date_time, is_dst=None)
        date_time = local_dt.astimezone(tz)
        return date_time

    @classmethod
    def parse_start_end_time(cls, date_time_1, date_time_2, tz):
        try:
            date_time_1 = datetime.strptime(date_time_1, '%Y-%m-%dT%H:%M:%SZ')
            date_time_2 = datetime.strptime(date_time_2, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            try:
                date_time_2 = datetime.strptime(date_time_2, '%Y-%m-%dT%H:%M:%SZ')
                date_time_1 = datetime.strptime(date_time_1, '%H:%M:%S')
                date_time_1 = date_time_1.replace(year=date_time_2.year, month=date_time_2.month, day=date_time_2.day)
            except ValueError as e:
                raise e
        if date_time_1 < date_time_2:
            start_time = date_time_1.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_time = date_time_2.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            start_time = date_time_2.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_time = date_time_1.strftime('%Y-%m-%dT%H:%M:%SZ')
        return cls.parse_datetime(start_time,tz).strftime('%Y-%m-%dT%H:%M:%S%z'), cls.parse_datetime(end_time,tz).strftime('%Y-%m-%dT%H:%M:%S%z')



    @classmethod
    def utc_to_local(cls, utc_dt, tz):
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tz)
        return tz.normalize(local_dt)

    @classmethod
    def utc_to_local_str(cls, at_time, tz):
        return Utils.utc_to_local(datetime.strptime(at_time, '%Y-%m-%dT%H:%M:%SZ'),
                                  tz).strftime('%b %d, %Y at %I:%M %p')

    @classmethod
    def in_weekdays(cls, start_day, end_day):
        if start_day != end_day:
            list = [start_day, end_day]
            while(1):
                if start_day + 1 != end_day:
                    start_day = start_day + 1 if start_day + 1 < 7 else start_day + 1 - 7
                    list.append(start_day)
                else:
                    break
            return list
        else:
            return [start_day]


    """
    @staticmethod
    def get_tz(phone_number):
        from phonenumbers import timezone
        import pytz
        try:
            x = phonenumbers.parse(phone_number)
            tz = timezone.time_zones_for_number(x)
            return tz[0]
        except Exception as e:
            return pytz.utc.zone
    """