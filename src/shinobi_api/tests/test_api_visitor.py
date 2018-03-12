#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
import copy
from rest_framework import status
from rest_framework.test import APITestCase

from django.conf import settings
from shinobi_api.models import Visitor
from shinobi_api.models import Building

from shinobi_api.services import UserService
from shinobi_api.tests import user_init, head, building_init

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

visitor_1 = {
    'id': 1,
    'building_id': 1,
    'name': 'TG',
    'id_card': '241225222',
    'visitor_code': '122199203195222',
    'avatar': 'sync/cmnd/4.jpg',
    'dob': '1992-03-19',
    'is_block': False,
    'note': '',
    'timestamp': None
}

visitor_2 = {
    'id': 2,
    'building_id': 1,
    'name': 'HN',
    'id_card': '241225223',
    'visitor_code': '122199203195223',
    'avatar': 'sync/cmnd/5.jpg',
    'dob': '1992-03-19',
    'is_block': True,
    'note': '',
    'timestamp': None
}

class VisitorAPITestCase(APITestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorAPITestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT
        global TOKEN
        global VISITOR_1, VISITOR_2

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)
        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        VISITOR_1 = Visitor.objects.create(**visitor_1)
        VISITOR_2 = Visitor.objects.create(**visitor_2)

        # login
        url = '/api/v1/auth'
        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'
        }
        response = self.client.post(url, data, **head)
        TOKEN = response.data['token']

    def test_retrieve_by_code(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorAPITestCase.test_retrieve_by_code
        """
        url = '/api/v1/manager/visitor/retrieve_by_code'
        data = {'visitor_code': visitor_1['visitor_code']}
        exp_json = {
                    'id': 1,
                    'building': 1,
                    'name': 'TG',
                    'id_card': '241225222',
                    'visitor_code': '122199203195222',
                    'avatar': 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT, settings.MEDIA_URL, 'sync/cmnd/4.jpg'),
                    'dob': '1992-03-19',
                    'is_block': False,
                    'note': '',
                    'timestamp': None
                    }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.post(url, data, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_list_visitor(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorAPITestCase.test_list_visitor
        """
        url = '/api/v1/manager/visitor'
        exp_json = {
                    'result': [
                        {
                            'id': 2,
                            'building': 1,
                            'name': 'HN',
                            'id_card': '241225223',
                            'visitor_code': '122199203195223',
                            'avatar': 'http://%s:%s%s%s' % (
                                settings.API_HOST, settings.API_PORT, settings.MEDIA_URL, 'sync/cmnd/5.jpg'),
                            'dob': '1992-03-19',
                            'is_block': True,
                            'note': '',
                            'timestamp': None
                        },
                        {
                            'id': 1,
                            'building': 1,
                            'name': 'TG',
                            'id_card': '241225222',
                            'visitor_code': '122199203195222',
                            'avatar': 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT, settings.MEDIA_URL, 'sync/cmnd/4.jpg'),
                            'dob': '1992-03-19',
                            'is_block': False,
                            'note': '',
                            'timestamp': None
                        }
                    ],
                    'count': 2,
                    }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_block_visitor(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorAPITestCase.test_block_visitor
        """
        url = '/api/v1/manager/visitor/1/block'
        exp_json = {
                    'id': 1,
                    'building': 1,
                    'name': 'TG',
                    'id_card': '241225222',
                    'visitor_code': '122199203195222',
                    'avatar': 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT,
                                                    settings.MEDIA_URL, 'sync/cmnd/4.jpg'),
                    'dob': '1992-03-19',
                    'is_block': True,
                    'note': '',
                    'timestamp': None
                    }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_un_block_visitor(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorAPITestCase.test_un_block_visitor
        """
        url = '/api/v1/manager/visitor/2/unblock'
        exp_json = {
                    'id': 2,
                    'building': 1,
                    'name': 'HN',
                    'id_card': '241225223',
                    'visitor_code': '122199203195223',
                    'avatar': 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT,
                                                    settings.MEDIA_URL, 'sync/cmnd/5.jpg'),
                    'dob': '1992-03-19',
                    'is_block': False,
                    'note': '',
                    'timestamp': None
                    }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)
