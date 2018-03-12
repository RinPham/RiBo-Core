#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from shinobi_api.const import ReportType
from shinobi_api.models import BadgeType
from shinobi_api.models import Building
from shinobi_api.services import BadgeService
from shinobi_api.services import ReportService
from shinobi_api.services import UserService

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

import copy
from django.test import TestCase
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

class ReportServiceTestCase(TestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.ReportServiceTestCase
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

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)
        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        badge_type_1['building_id'] = BUILDING_INIT.id
        badge_type_2['building_id'] = BUILDING_INIT.id
        BadgeType.objects.create(**badge_type_1)
        BadgeType.objects.create(**badge_type_2)
        input = {}
        input['data'] = 'test/data.csv'
        input['upload_dir'] = 'test/upload'

        act_rs = BadgeService.sync(input, building=BUILDING_INIT.id)


    def test_report_by_date(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.ReportServiceTestCase.test_report_by_date
        """
        input_data = {}
        input_data['building_id'] = BUILDING_INIT.id
        input_data['start_date'] = '2017-03-01'
        input_data['end_date'] = '2017-04-30'
        input_data['type'] = ReportType.DATE

        exp_total = 4
        exp_count_1 = 3
        exp_count_2 = 1
        exp_group_date_1 = '03/2017'
        exp_group_date_2 = '04/2017'

        act_res = ReportService.report(input_data)
        self.assertEqual(exp_total, act_res.get('total', None))
        self.assertEqual(exp_count_1, act_res.get('data')[0].get('count'))
        self.assertEqual(exp_group_date_1, act_res.get('data')[0].get('date'))
        self.assertEqual(exp_count_2, act_res.get('data')[1].get('count'))
        self.assertEqual(exp_group_date_2, act_res.get('data')[1].get('date'))


    def test_report_by_type(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.ReportServiceTestCase.test_report_by_type
        """
        input_data = {}
        input_data['building_id'] = BUILDING_INIT.id
        input_data['start_date'] = '2017-03-01'
        input_data['end_date'] = '2017-04-30'
        input_data['type'] = ReportType.TYPE

        exp_total = 4
        exp_count_1 = 2
        exp_count_2 = 2
        exp_group_type_1 = 'CONTRACTOR'
        exp_group_type_2 = 'VISITOR'

        act_res = ReportService.report(input_data)
        self.assertEqual(exp_total, act_res.get('total', None))
        self.assertEqual(exp_count_1, act_res.get('data')[0].get('count'))
        self.assertEqual(exp_group_type_1, act_res.get('data')[0].get('type'))
        self.assertEqual(exp_count_2, act_res.get('data')[1].get('count'))
        self.assertEqual(exp_group_type_2, act_res.get('data')[1].get('type'))
