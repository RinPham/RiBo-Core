#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.test import override_settings

__author__ = "hien"
__date__ = "07 13 2016, 9:45 AM"

import copy

from django.test import TestCase

from shinobi_api.const import Gender, UserType
from shinobi_api.services import (
    UserService
)
from shinobi_api.models import (
    UserProfile, UserEmail
)
from . import (
    user_data1, user_data2, create_users
)

class UserServiceTestCase(TestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.UserServiceTestCase
    """

    def setUp(self):
        pass

    def test_create_user(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.UserServiceTestCase.test_create_user
        """
        global user_data1
        PETER, MARIA = create_users()
        self.assertNotEqual(PETER, None)
        self.assertEqual(PETER.first_name, user_data1['first_name'], 'Assert user has been created')
        self.assertEqual(PETER.user_type, user_data1['user_type'])
        self.assertEqual(MARIA.profile.gender, Gender.FEMALE)
        self.assertEqual(2, UserProfile.objects.count(), 'Profile has been created')
        self.assertEqual(2, UserEmail.objects.count(), 'Email has been added')


    def test_update_user(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.UserServiceTestCase.test_update_user
        """
        PETER, MARIA = create_users()
        new_name = 'PEPE'
        new_gender = Gender.MALE
        count1 = UserProfile.objects.count()
        NEWPETER = UserService.save({
            'id': PETER.id,
            'first_name': new_name,
            'profile': {
                'gender': Gender.MALE
            }
        })
        count2 = UserProfile.objects.count()
        count_user_email1 = UserEmail.objects.count()
        new_email = 'this_is_new_email1@gmail.com'
        NEWMARIA = UserService.save({
            'id': MARIA.id,
            'email': new_email,
            'profile': {

            }
        })
        count_user_email2 = UserEmail.objects.count()
        self.assertEqual(count1, count2, 'Not create more profile')
        self.assertEqual(NEWPETER.first_name, new_name, 'Update user success')
        self.assertEqual(NEWPETER.profile.gender, new_gender, 'Update user profile success')
        self.assertEqual(NEWMARIA.email, new_email, 'Update email success')
        # self.assertEqual(count_user_email1 + 1, count_user_email2, 'Email has been saved')
