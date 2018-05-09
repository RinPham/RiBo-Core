#! /usr/bin/python


class const(object):
    class ConstError(TypeError):
        pass  # base exception class

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name %r is not all uppercase' % name)
        self.__dict__[name] = value

class DeviceType(const):
    MOBILE = 1  #
    ANDROID_PHONE = 2
    IOS_PHONE = 3
    WINDOWPHONE = 4
    ANDROID_TABLET = 5
    IOS_TABLET = 6
    MOBILE_WEB = 7
    DESKTOP_WEB = 8

class FromWho(const):
    RIBO_ASSISTANT = 0
    USER = 1

class TypeRepeat(const):
    NONE = 0
    DAILY = 1
    WEEKLY = 2
    WEEKDAYS = 3
    WEEKENDS = 4
    MONTHLY = 5

class Recurrence(const):
    RECURRENCE_NONE = 'no'
    RECURRENCE_WEEKLY = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'weekly']
    RECURRENCE_DAILY = 'daily'
    RECURRENCE_WEEKDAYS = 'weekdays'
    RECURRENCE_MONTHLY = 'monthly'
    RECURRENCE_WEEKENDS = 'weekends'

class TaskType(const):
    NONE = 0
    CALL = 1
    EMAIL = 2

weekday = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6
}

weekday_str = {
    'Mon' : 'monday',
    'Tue' : 'tuesday',
    'Wed' : 'wednesday',
    'Thu' : 'thursday',
    'Fri' : 'friday',
    'Sat' : 'Saturday',
    'Sun' : 'Sunday'
}

