#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.test import override_settings

from shinobi_api.models import Visitor
from shinobi_api.models import Building
from shinobi_api.services import UserService
from shinobi_api.services.visitor import VisitorService

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

import copy
from django.test import TestCase
from . import (
    building_init,
    user_init,
    )

vistor1 = {
    'name': 'NTHV',
    'dob': '1992-10-10',
    'visitor_code': '122199210105225',
    'id_card': '241225225',
}

vistor2 = {
    'name': 'TTHN',
    'dob': '1992-02-28',
    'visitor_code': '122199202285226',
    'id_card': '241225226',
}

vistor3 = {
    'name': 'HTKV',
    'dob': '1992-04-19',
    'visitor_code': '122199204195227',
    'id_card': '241225227',
}

class VisitorServiceTestCase(TestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorServiceTestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT

        global NTHV, THHN, HTKV
        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)
        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

        # Add visitor
        vistor1['building_id'] = BUILDING_INIT.id
        NTHV = Visitor.objects.create(**vistor1)
        vistor2['building_id'] = BUILDING_INIT.id
        THHN = Visitor.objects.create(**vistor2)
        vistor3['building_id'] = BUILDING_INIT.id
        HTKV = Visitor.objects.create(**vistor3)

    def test_get_visitors_without_search(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorServiceTestCase.test_get_visitors_without_search
        """

        limit_visitor1 = 3
        limit_visitor2 = 2
        exp_total = 3
        kwargs = {}

        # get full data
        kwargs['limit'] = limit_visitor1
        kwargs['offset'] = 0

        act_res = VisitorService.get_visitors(**kwargs)
        act_visitor1 = act_res.get('result', None)
        act_count1 = act_res.get('count', 0)
        act_visitor_count1 = act_visitor1.count()

        self.assertEqual(exp_total, act_count1)
        self.assertEqual(limit_visitor1, act_visitor_count1)
        self.assertEqual(HTKV.name, act_visitor1.first().name)
        self.assertEqual(HTKV.dob, act_visitor1.first().dob.strftime('%Y-%m-%d'))
        self.assertEqual(HTKV.visitor_code, act_visitor1.first().visitor_code)
        self.assertEqual(HTKV.id_card, act_visitor1.first().id_card)

        # get a part data
        kwargs['limit'] = limit_visitor2
        act_res = VisitorService.get_visitors(**kwargs)
        act_visitor2 = act_res.get('result', None)
        act_count2 = act_res.get('count', 0)
        act_visitor_count2 = act_visitor2.count()

        self.assertEqual(exp_total, act_count2)
        self.assertEqual(limit_visitor2, act_visitor_count2)

    def test_get_visitors_with_search(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.VisitorServiceTestCase.test_get_visitors_with_search
        """

        limit_visitor1 = 3
        exp_total = 1
        kwargs = {}

        kwargs['limit'] = limit_visitor1
        kwargs['offset'] = 0
        kwargs['search'] = '199204'

        act_res = VisitorService.get_visitors(**kwargs)
        act_visitor1 = act_res.get('result', None)
        act_count1 = act_res.get('count', 0)
        act_visitor_count1 = act_visitor1.count()

        self.assertEqual(exp_total, act_count1, 'Only get record mapping visitor_code')
        self.assertEqual(exp_total, act_visitor_count1, 'Only get record mapping visitor_code')
        self.assertEqual(HTKV.name, act_visitor1.first().name)
        self.assertEqual(HTKV.dob, act_visitor1.first().dob.strftime('%Y-%m-%d'))
        self.assertEqual(HTKV.visitor_code, act_visitor1.first().visitor_code)
        self.assertEqual(HTKV.id_card, act_visitor1.first().id_card)
