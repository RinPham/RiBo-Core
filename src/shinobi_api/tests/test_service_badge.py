#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from os.path import join

from django.conf import settings
from shinobi_api.models import Badge
from shinobi_api.models import Visitor
from shinobi_api.models import Building
from shinobi_api.models import BadgeType
from shinobi_api.models import PrintSetup
from shinobi_api.models import SyncSchedule
from shinobi_api.services import UserService
from shinobi_api.services import BadgeService
from shinobi_api.const import BadgeFormat, Printer, BadgeSize, SyncUnit

__author__ = "tu"
__date__ = "05 17 2017, 9:45 AM"

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


class BadgeServiceTestCase(TestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BadgeServiceTestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)
        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

    def test_sync_badge(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BadgeServiceTestCase.test_sync_badge
        """

        badge_type_1['building_id'] = BUILDING_INIT.id
        badge_type_2['building_id'] = BUILDING_INIT.id
        BadgeType.objects.create(**badge_type_1)
        BadgeType.objects.create(**badge_type_2)
        input = {}
        input['data'] = 'test/data.csv'
        input['upload_dir'] = 'test/upload'

        exp_message = 'sync successfully'
        exp_badge_insert_count = 4
        exp_visitor_insert_count = 4
        exp_checkout_count = 2

        act_rs = BadgeService.sync(input, building=BUILDING_INIT.id)
        act_badge_count = Badge.objects.count()
        act_visitor_count = Visitor.objects.count()
        act_checkout_count = Badge.objects.filter(is_active=1).count()

        file = open(join(settings.MEDIA_ROOT, input['data']))
        row_index = 0
        exp_data_1 = []
        for row in file:
            if row_index == 0:
                row_index += 1
                pass
            else:
                row_data = row.split(',')
                exp_data_1 = row_data
                break
        act_data_badge_1 = Badge.objects.first()
        act_data_visitor_1 = Visitor.objects.first()

        self.assertEqual(exp_message, act_rs.data['message'])
        self.assertEqual(exp_badge_insert_count, act_badge_count, "All check_in is saved")
        self.assertEqual(exp_visitor_insert_count, act_visitor_count, "All visitors is created")
        self.assertEqual(exp_checkout_count, act_checkout_count, "2 badges had been checkout")

        # check insert correct data
        #   check vsm_badge
        self.assertEqual(exp_data_1[2], '{}'.format(act_data_badge_1.location_id))
        self.assertEqual(exp_data_1[3], '{}'.format(act_data_badge_1.badge_id))
        self.assertEqual(exp_data_1[4], act_data_badge_1.date_issued.strftime('%Y-%m-%d'))
        self.assertEqual(exp_data_1[5], act_data_badge_1.time_issued.strftime('%H:%M:%S'))
        self.assertEqual(exp_data_1[6], act_data_badge_1.destination)
        self.assertEqual(exp_data_1[7], '{}'.format(act_data_badge_1.badge_type_id))
        self.assertEqual(BUILDING_INIT.id, act_data_badge_1.building_id)

        #   check vms_visitor
        self.assertEqual(BUILDING_INIT.id, act_data_visitor_1.building_id)
        self.assertEqual(exp_data_1[1], '{}'.format(act_data_visitor_1.visitor_code))
        self.assertEqual(exp_data_1[8], act_data_visitor_1.name)
        self.assertEqual(exp_data_1[9], act_data_visitor_1.id_card)
        self.assertEqual(join(input['upload_dir'], exp_data_1[10]), act_data_visitor_1.avatar)
        self.assertEqual(exp_data_1[11].rstrip(), act_data_visitor_1.dob.strftime('%Y-%m-%d'))



    def test_default_setup(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.BadgeServiceTestCase.test_default_setup
        """
        BadgeService.default_setup(BUILDING_INIT.id)
        exp_badge_type_name = ['VISITOR', 'CONTRACTOR', 'VENDOR', 'TEMPORARY', '']
        exp_badge_type_count = 5
        act_badge_type = BadgeType.objects.all()
        act_badge_type_count = BadgeType.objects.count()

        act_print_setup_count = PrintSetup.objects.count()
        act_print_setup = PrintSetup.objects.first()
        exp_print_setup = PrintSetup()
        exp_print_setup.badge_format = BadgeFormat.DESTINATION_AND_NAME
        exp_print_setup.stored_printer = Printer.TEMP_BP4
        exp_print_setup.stored_badge_size = BadgeSize.SM_02050

        act_sync_count = SyncSchedule.objects.count()
        act_sync = SyncSchedule.objects.first()
        exp_sync = SyncSchedule()
        exp_sync.number = 1
        exp_sync.unit = SyncUnit.HOUR

        self.assertEqual(exp_badge_type_count, act_badge_type_count)
        for i in range(5):
            self.assertEqual(exp_badge_type_name[i], act_badge_type[i].name, 'Insert data corrected')

        self.assertEqual(1, act_print_setup_count, '1 record print setup is created')
        self.assertEqual(exp_print_setup.badge_format, act_print_setup.badge_format)
        self.assertEqual(exp_print_setup.stored_printer, act_print_setup.stored_printer)
        self.assertEqual(exp_print_setup.stored_badge_size, act_print_setup.stored_badge_size)

        self.assertEqual(1, act_sync_count, '1 record sync schedule is created')
        self.assertEqual(exp_sync.number, act_sync.number)
        self.assertEqual(exp_sync.unit, act_sync.unit)