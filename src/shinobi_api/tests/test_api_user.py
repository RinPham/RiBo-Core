#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
import copy
from rest_framework import status
from rest_framework.test import APITestCase

from shinobi_api.const import UserType
from shinobi_api.models import QuestionReset
from shinobi_api.models import User
from shinobi_api.services import UserService
from shinobi_api.tests import user_init, head

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

question_reset_1 = {
    'id': 1,
    'question_id': '1',
    'number_question': '1',
    'answer': 'answer 1',
}
question_reset_2 = {
    'id': 2,
    'question_id': '2',
    'number_question': '2',
    'answer': 'answer 2',
}
question_reset_3 = {
    'id': 3,
    'question_id': '3',
    'number_question': '3',
    'answer': 'answer 3',
}

user_2 = {
    'id': 2,
    'first_name': 'Tu',
    'middle_name': 'Minh',
    'last_name': 'Tester',
    'email': 'admin2@example.com',
    'password': 'abc123',
    'user_type': UserType.MANAGER,
    'profile': {
        'gender': 1,
        'dob': '1988-07-19'
    }
}

class UserAPITestCase(APITestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.UserAPITestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)

        question_reset_1['user_id'] = ADMIN_INIT.id
        question_reset_2['user_id'] = ADMIN_INIT.id
        question_reset_3['user_id'] = ADMIN_INIT.id
        QuestionReset.objects.create(**question_reset_1)
        QuestionReset.objects.create(**question_reset_2)
        QuestionReset.objects.create(**question_reset_3)

    def test_register_user(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.UserAPITestCase.test_register_user
        """
        url = '/api/v1/user'
        data = user_2
        response = self.client.post(url, data, format='json', **head)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check database
        user = User.objects.get(pk=2)
        self.assertIsNotNone(user)

    def test_change_user_password(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.UserAPITestCase.test_change_user_password
        """
        url = '/api/v1/user/password'
        data = {
            'email': user_init['email'],
            'password': user_init['password'],
            'new_password': '123abc'
        }

        data2 = {
            'email': user_init['email'],
            'password': '123abcd',
            'new_password': '123abc'
        }

        exp_json = {
            "message": "Your password has been updated"
        }
        response = self.client.post(url, data, format='json', **head)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

        response = self.client.post(url, data2, format='json', **head)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reset_pass_code(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.UserAPITestCase.test_reset_pass_code
        """
        url = '/api/v1/user/reset_pass_code'
        data1 = {
            'email': user_init['email'],
            'answer1': 'answer 1',
            'answer2': 'answer 2',
            'answer3': 'answer 3',
        }

        exp_json = {
            "message": "Your password has been updated"
        }
        response = self.client.post(url, data1, format='json', **head)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        data2 = {
            'uid': response.data['uid'],
            'token': response.data['token'],
            'password': '123abc'
        }

        response = self.client.put(url, data2, format='json', **head)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)
