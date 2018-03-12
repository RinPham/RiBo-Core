#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
import copy
from rest_framework import status
from rest_framework.test import APITestCase

from shinobi_api.services import UserService
from shinobi_api.tests import user_init, head

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"


class AuthAPITestCase(APITestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.AuthAPITestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)

    def test_login(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.AuthAPITestCase.test_login
        """
        url = '/api/v1/auth'
        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'}
        response = self.client.post(url, data, format='json', **head)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.AuthAPITestCase.test_logout
        """
        url = '/api/v1/auth'

        # login

        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'}
        response = self.client.post(url, data, format='json', **head)

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(response.data['token'])
        response = self.client.delete(url, format='json', **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
