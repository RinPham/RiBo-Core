#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
import copy
from rest_framework import status
from rest_framework.test import APITestCase

from shinobi_api.models import Building

from shinobi_api.services import UserService
from shinobi_api.tests import head, building_init

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

from . import user_init

building_1 = {'location_id': 100,
              'name': 'ABCD',
              'type': 1,
              'logo': 'logo/image1.jpg',
              'is_disabled': True
              }



class BuildingAPITestCase(APITestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BuildingAPITestCase
    """

    def setUp(self):

        global ADMIN_INIT
        global BUILDING_INIT
        global TOKEN

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)

        # login
        url = '/api/v1/auth'
        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'
        }
        response = self.client.post(url, data, **head)
        TOKEN = response.data['token']

    def test_create_building(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BuildingAPITestCase.test_create_building
        """

        exp_number_building = 1
        url = '/api/v1/manager/building'
        data = building_1

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.post(url, data, **head_copy)

        act_number_building = Building.objects.count()
        act_building = Building.objects.first()
        self.assertEqual(exp_number_building, act_number_building, "building had been created")

        # check data create in database
        self.assertEqual(data['location_id'], act_building.location_id)
        self.assertEqual(data['name'], act_building.name)
        self.assertEqual(data['type'], act_building.type)
        self.assertEqual(data['logo'], act_building.logo)
        self.assertEqual(data['is_disabled'], act_building.is_disabled)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error_create_building(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BuildingAPITestCase.test_create_building
        """

        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        exp_number_building = 1
        url = '/api/v1/manager/building'
        data = building_1

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.post(url, data, **head_copy)

        act_number_building = Building.objects.count()
        act_building = Building.objects.first()
        self.assertEqual(exp_number_building, act_number_building)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_building(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BuildingAPITestCase.test_update_building
        """

        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        url = '/api/v1/manager/building/1'
        data = building_1

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, data, **head_copy)

        act_building = Building.objects.first()

        # check data create in database
        self.assertEqual(data['location_id'], act_building.location_id)
        self.assertEqual(data['name'], act_building.name)
        self.assertEqual(data['type'], act_building.type)
        self.assertEqual(data['logo'], act_building.logo)
        self.assertEqual(data['is_disabled'], act_building.is_disabled)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_logo_building(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BuildingAPITestCase.test_change_logo_building
        """

        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        url = '/api/v1/manager/building/1/logo'
        data = {'logo': 'logo/new_image.jpg'}

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, data, **head_copy)

        act_building = Building.objects.first()

        # check data create in database
        self.assertEqual(data['logo'], act_building.logo)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_location_name_building(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BuildingAPITestCase.test_change_location_name_building
        """

        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        url = '/api/v1/manager/building/1/location_name'
        data = {'location_id': 222,
                'name': 'New name'}

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, data, **head_copy)

        act_building = Building.objects.first()

        # check data create in database
        self.assertEqual(data['location_id'], act_building.location_id)
        self.assertEqual(data['name'], act_building.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_building_by_user(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BuildingAPITestCase.test_list_building_by_user
        """

        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        url = '/api/v1/manager/building/list_by_user'
        exp_json = {'building':[
            {'id': 1,
                'location_id': 111,
                'name': 'Alibaba',
                'type': 1,
                'logo': 'image/logo.jpg',
                'is_disabled': False,
                'user': ADMIN_INIT.id
             }
            ]
        }
        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)