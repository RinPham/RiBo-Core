#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
import copy
from rest_framework import status
from rest_framework.test import APITestCase

from shinobi_api.models import Badge
from shinobi_api.models import BadgeType
from shinobi_api.models import Building
from shinobi_api.models import Visitor

from shinobi_api.services import UserService
from shinobi_api.tests import head

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

from . import (
    building_init,
    user_init,
    )

badge_type_1 = {
    'type': 'BadgeType1',
    'name': 'VISITOR',
    'id': '1',
}

badge_type_2 = {
    'type': 'BadgeType2',
    'name': 'CONTRACTOR',
    'id': '2',
}

badge = {
    'id': 1,
    'building_id': 1,
    'location_id': 111,
    'badge_type_id': 1,
    'badge_id': 3,
    'visitor_id': 1
}

vistor1 = {
    'id': 1,
    'name': 'NTHV',
    'dob': '1992-10-10',
    'visitor_code': '122199210105225',
    'id_card': '241225225',
}

class BadgeManagerAPITestCase(APITestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BadgeManagerAPITestCase
    """

    def setUp(self):
        """
        data file:
            "checkin", "visitor_code", "location_id", "badge_id", "date", "time", "destination", "badge_type_id", "name", "id_card", "avatar", "dob"
            1,122199203165225,122,1,2017-03-28,08:30:53,Grade 1 - 101,1,THN,241225225,cmnd/1.jpg,1992-03-16
            1,122199203175224,122,2,2017-03-29,08:30:53,Grade 2 - 102,1,TA,241225224,cmnd/2.jpg,1992-03-17
            1,122199203185223,122,3,2017-04-29,08:30:53,Grade 3 - 103,2,NTHV,241225223,cmnd/3.jpg,1992-03-18
            1,122199203195222,122,4,2017-03-29,08:30:53,Grade 4 - 104,2,TG,241225222,cmnd/4.jpg,1992-03-19
            0,122199203165225,2017-03-29,09:30:53
            0,122199203185223,2017-04-29,09:40:53
        """
        global ADMIN_INIT
        global BUILDING_INIT
        global TOKEN

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)
        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        # login
        url = '/api/v1/auth'
        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'
        }
        response = self.client.post(url, data, **head)
        TOKEN = response.data['token']

        badge_type_1['building_id'] = BUILDING_INIT.id
        badge_type_2['building_id'] = BUILDING_INIT.id
        BadgeType.objects.create(**badge_type_1)
        BadgeType.objects.create(**badge_type_2)

    def test_get_last_badge(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BadgeManagerAPITestCase.test_get_last_badge
        """

        # init data

        Visitor.objects.create(**vistor1)
        Badge.objects.create(**badge)

        url = '/api/v1/manager/badge_manager/last'

        exp_json = {'badge_id': 3,
                    'location_id': 111
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_get_last_badge_without_data(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BadgeManagerAPITestCase.test_get_last_badge_without_data
        """

        url = '/api/v1/manager/badge_manager/last'

        exp_json = {'badge_id': 0,
                    'location_id': 111
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_sync(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BadgeManagerAPITestCase.test_sync
        """
        pass