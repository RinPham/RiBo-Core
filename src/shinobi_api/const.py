#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "$Jul 05, 2016 10:34:03 AM$"

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

class ResourceType(const):
    RS_USER = 1
    RS_APP = 1


class ResourceStatus(const):
    ACTIVE = 1
    ARCHIVED = 2


class PrefType(const):
    pass


class PrefValue(const):
    ON = 1
    OFF = 0


class UserSignupType(const):
    BY_EMAIL = 0
    BY_FACEBOOK = 1
    BY_GOOGLE = 2

class UserStatus(const):
    ACTIVE = 1
    UNVERIFIED = 2
    DELETED = 3
    BLOCKED = 4
    BLOCKED_UNVERIFIED = 5


class UserType(const):
    GUEST = 1
    VISITOR = 2
    EMPLOYEE = 3
    MANAGER = 4
    STAFF = 5
    SUPERUSER = 6

    @classmethod
    def is_manager(cls, user_type):
        return (user_type == cls.STAFF or user_type == cls.SUPERUSER)

    @classmethod
    def is_valid_type(cls, user_type):
        return user_type in [
            cls.GUEST,
            cls.VISITOR,
            cls.EMPLOYEE,
            cls.MANAGER,
            cls.STAFF,
            cls.SUPERUSER
        ]


class MMSType(const):
    VIDEO = "video"
    IMAGE = "image"


class DeviceType(const):
    MOBILE = 1  #
    ANDROID_PHONE = 2
    IOS_PHONE = 3
    WINDOWPHONE = 4
    ANDROID_TABLET = 5
    IOS_TABLET = 6
    MOBILE_WEB = 7
    DESKTOP_WEB = 8


class Gender(const):
    MALE = 0
    FEMALE = 1


class BuildingType(const):
    BUILDING = 1
    HOTEL = 2
    RESORT = 3
    HOSPITAL = 4


class ReportType(const):
    DATE = 1
    TYPE = 2


class BadgeFormat(const):
    DESTINATION_AND_NAME = 1
    DESTINATION = 2


class Printer(const):
    TEMP_BP4 = 1


class BadgeSize(const):
    SM_02050 = 1


class SyncUnit(const):
    HOUR = 1
    DAY = 2
    WEEK = 3


BUILDING_TYPE_CHOICES = [
    (BuildingType.BUILDING, 'Building'),
    (BuildingType.HOTEL, 'Hotel'),
    (BuildingType.RESORT, 'Resort'),
    (BuildingType.HOSPITAL, 'Hospital'),
]

USER_TYPE_CHOICES = [
    (UserType.GUEST, 'Guest'),
    (UserType.VISITOR, 'Visitor'),
    (UserType.EMPLOYEE, 'Employee'),
    (UserType.MANAGER, 'Manager'),
    (UserType.STAFF, 'Staff'),
    (UserType.SUPERUSER, 'Superuser'),
]

USER_GENDERS = [
    (Gender.MALE, 'Male'),
    (Gender.FEMALE, 'Female')
]

SYNC_UNIT_CHOICES = [
    (SyncUnit.HOUR, 'hour'),
    (SyncUnit.DAY, 'day'),
    (SyncUnit.WEEK, 'week'),
]

BADGE_FORMAT_CHOICES = [
    (BadgeFormat.DESTINATION_AND_NAME, 'Destination and Name'),
    (BadgeFormat.DESTINATION, 'Destination'),
]

PRINTER_CHOICES = [
    (Printer.TEMP_BP4, 'TEMPBadge BP4'),
]

BADGE_SIZE_CHOICES = [
    (BadgeSize.SM_02050, '02050 sm TEMPBadge VMS badge'),
]