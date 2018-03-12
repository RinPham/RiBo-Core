#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

#
# python src/manage.py test shinobi_api.tests --settings=vmscore.settings.test
#

import copy

from shinobi_api.services import UserService
from shinobi_api.const import UserType

__author__ = "hien"
__date__ = "07 13 2016, 9:43 AM"

user_data1 = {
    'first_name': 'Peter',
    'middle_name': 'P',
    'last_name': 'Tester',
    'email': 'email@example.com',
    'user_type': UserType.GUEST,
    'profile': {
        'gender': 0,
        'dob': '1988-07-17'
    },
}

user_data2 = {
    'first_name': 'Maria',
    'middle_name': 'Ozawa',
    'last_name': 'Tester',
    'email': 'test+p2@example.com',
    'password': '123456',
    'user_type': UserType.MANAGER,
    'profile': {
        'gender': 1,
        'dob': '1988-07-19'
    }
}

question_reset_data1 = {
    'question1': '1',
    'question2': '2',
    'question3': '3',
    'answer1': 'answer 1',
    'answer2': 'answer 2',
    'answer3': 'answer 3'
}

question_reset_data_error = {
    'question1': '4',
    'question2': '5',
    'question3': '50',
    'answer1': 'answer update 1',
    'answer2': 'answer update 2',
    'answer3': 'answer update 3'
}

question_reset_data2 = {
    'question1': '4',
    'question2': '5',
    'question3': '6',
    'answer1': 'answer update 1',
    'answer2': 'answer update 2',
    'answer3': 'answer update 3'
}

user_init = {
    'id': 1,
    'first_name': 'Tu',
    'middle_name': 'Minh',
    'last_name': 'Tester',
    'email': 'admintest@example.com',
    'password': 'abc123',
    'user_type': UserType.MANAGER,
    'profile': {
        'gender': 1,
        'dob': '1988-07-19'
    }
}

head = {'HTTP_USER_AGENT': 'tester-human','HTTP_DEVICE': 'abc', 'HTTP_APPID':1, 'HTTP_TYPE': 1}

building_init = {
    'id': 1,
    'location_id': '111',
    'type': 1,
    'name': 'Alibaba',
    'logo': 'image/logo.jpg'
}

def create_users(data1=None, data2=None):
    if data1 is None:
        data1 = copy.deepcopy(user_data1)
    if data2 is None:
        data2 = copy.deepcopy(user_data2)
    peter = UserService.save(data1)
    maria = UserService.save(data2)
    return peter, maria

# For single class testcase
from .test_service_user import UserServiceTestCase
from .test_service_system_app import MSystemServiceTestCase
