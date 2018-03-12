#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
import copy
from rest_framework import status
from rest_framework.test import APITestCase

from shinobi_api.models import BadgeType
from shinobi_api.models import Building
from shinobi_api.models import BuildingDepartment
from shinobi_api.models import Department
from shinobi_api.models import PrintSetup
from shinobi_api.models import SyncSchedule

from shinobi_api.services import UserService
from shinobi_api.tests import user_init, head, building_init

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

badge_type_1 = {
    'type': 'BadgeType1',
    'name': 'VISITOR',
    'id': 1,
}

badge_type_2 = {
    'type': 'BadgeType2',
    'name': 'CONTRACTOR',
    'id': 2,
}

department_1 = {
    'name': 'SALES',
    'id': 1,
    'user_id': 1
}

department_2 = {
    'name': 'ADMIN',
    'id': 2,
    'user_id': 1
}

building_department_1 = {
    'department_id': 1,
    'id': 1,
    'building_id': 1
}

building_department_2 = {
    'department_id': 2,
    'id': 2,
    'building_id': 1
}

print_setup = {
    'building_id': 1,
    'badge_format': 1,
    'stored_printer': 1,
    'stored_badge_size': 1
}

sync_schedule = {
    'building_id': 1,
    'number': 1,
    'unit': 1
}

class WorkstationAPITestCase(APITestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT
        global TOKEN

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)
        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)
        badge_type_1['building_id'] = BUILDING_INIT.id
        badge_type_2['building_id'] = BUILDING_INIT.id
        BadgeType.objects.create(**badge_type_1)
        BadgeType.objects.create(**badge_type_2)

        # login
        url = '/api/v1/auth'
        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'
        }
        response = self.client.post(url, data, **head)
        TOKEN = response.data['token']

    def test_get_badge_type(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_get_badge_type
        """
        url = '/api/v1/manager/badge_type'
        exp_json = {'badge_type': [
            {
                'type': 'BadgeType1',
                'name': 'VISITOR',
                'id': 1,
            },
            {
                'type': 'BadgeType2',
                'name': 'CONTRACTOR',
                'id': 2,
            }
            ]
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_update_badge_type(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_update_badge_type
        """
        url = '/api/v1/manager/badge_type/1'
        data = {'name': 'VENDOR'}
        exp_json = {
                'type': 'BadgeType1',
                'name': 'VENDOR',
                'id': 1,
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, data, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_create_department(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_create_department
        """
        url = '/api/v1/manager/department'
        data = {'name': 'SALES'}

        exp_number_department = 1

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.post(url, data, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        act_number_department = Department.objects.count()
        act_department = Department.objects.first()

        exp_json = {
            'name': 'SALES',
            'id': act_department.id,
        }

        self.assertEqual(exp_number_department, act_number_department, "Department had been created")
        # check data create in database
        self.assertEqual(data['name'], act_department.name)

        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_delete_department(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_delete_department
        """

        Department.objects.create(**department_1)
        url = '/api/v1/manager/department/1'

        exp_number_department = 0

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.delete(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        act_number_department = Department.objects.filter(pk=1).count()

        exp_json = {
            'message': 'Delete successfully'
        }

        self.assertEqual(exp_number_department, act_number_department, "Department had been deleted")

        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_list_department(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_list_department
        """

        Department.objects.create(**department_1)
        Department.objects.create(**department_2)
        url = '/api/v1/manager/department'

        exp_json = {
            'lis_department': [
                {
                    'id': 1,
                    'name': 'SALES'
                },
                {
                    'id': 2,
                    'name': 'ADMIN'
                }
            ]
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_create_building_department(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_create_building_department
        """
        Department.objects.create(**department_1)

        url = '/api/v1/manager/building_department'
        data = {'department': 1}

        exp_number_bd_department = 1

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.post(url, data, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        act_number_bd_department = BuildingDepartment.objects.count()
        act_bd_department = BuildingDepartment.objects.first()

        exp_json = {
            'name': 'SALES',
            'id': act_bd_department.id,
        }

        self.assertEqual(exp_number_bd_department, act_number_bd_department, "Building_Department had been created")
        # check data create in database
        self.assertEqual(data['department'], act_bd_department.department.id)

        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_delete_building_department(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_delete_building_department
        """

        Department.objects.create(**department_1)
        BuildingDepartment.objects.create(**building_department_1)
        url = '/api/v1/manager/building_department/1'

        exp_number_bd_department = 0

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.delete(url, **head_copy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        act_number_bd_department = BuildingDepartment.objects.filter(pk=1).count()

        exp_json = {
            'message': 'Delete successfully'
        }

        self.assertEqual(exp_number_bd_department, act_number_bd_department, "Building_department had been deleted")

        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_list_building_department(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_list_building_department
        """

        Department.objects.create(**department_1)
        Department.objects.create(**department_2)
        BuildingDepartment.objects.create(**building_department_1)
        BuildingDepartment.objects.create(**building_department_2)
        url = '/api/v1/manager/building_department'

        exp_json = {
            'lis_department': [
                {
                    'id': 1,
                    'name': 'SALES'
                },
                {
                    'id': 2,
                    'name': 'ADMIN'
                }
            ]
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_list_print_setup(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_list_print_setup
        """

        PrintSetup.objects.create(**print_setup)
        url = '/api/v1/manager/print_setup'

        exp_json = {
                    'building': 1,
                    'badge_format': 1,
                    'stored_printer': 1,
                    'stored_badge_size': 1
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_update_print_setup(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_update_print_setup
        """

        PrintSetup.objects.create(**print_setup)
        url = '/api/v1/manager/print_setup/1'
        data = {'badge_format': 2}

        exp_json = {
                    'building': 1,
                    'badge_format': 2,
                    'stored_printer': 1,
                    'stored_badge_size': 1
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, data, **head_copy)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_list_sync_schedule(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_list_sync_schedule
        """

        SyncSchedule.objects.create(**sync_schedule)
        url = '/api/v1/manager/sync_schedule'

        exp_json = {
                    'building': 1,
                    'number': 1,
                    'unit': 1
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_update_sync_schedule(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.WorkstationAPITestCase.test_update_sync_schedule
        """

        SyncSchedule.objects.create(**sync_schedule)
        url = '/api/v1/manager/sync_schedule/1'
        data = {'number': 2, 'unit': 2}

        exp_json = {
                    'building': 1,
                    'number': 2,
                    'unit': 2
        }

        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.put(url, data, **head_copy)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)