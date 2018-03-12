#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "07 27 2016, 3:16 PM"


class LoggingDecorators(object):
    @classmethod
    def ignore(cls, fn):
        def decorator(cl, request, *args, **kwargs):
            setattr(request._request, 'ignore_activity_log', True)
            return fn(cl, request, *args, **kwargs)

        return decorator


logging = LoggingDecorators
