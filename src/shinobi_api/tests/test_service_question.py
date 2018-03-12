#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.test import override_settings

from shinobi_api.models import Building
from shinobi_api.models import QuestionReset
from shinobi_api.services import UserService
from shinobi_api.services.question import QuestionService

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

import copy
from django.test import TestCase
from . import (
    building_init,
    user_init,
    question_reset_data1, question_reset_data2, question_reset_data_error)


class QuestionServiceTestCase(TestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionServiceTestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT
        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)
        building_test = building_init
        building_test['user_id'] = ADMIN_INIT.id
        BUILDING_INIT = Building.objects.create(**building_test)

    def test_get_question_reset(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionServiceTestCase.test_get_question_reset
        """
        # can't use in current version
        pass

    def test_create_question_reset(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionServiceTestCase.test_create_question_reset
        """
        QuestionService.create(question_reset_data1, ADMIN_INIT.id)
        res_question_count = QuestionReset.objects.count()
        res_question = QuestionReset.objects.all().order_by('number_question')

        exp_count = 3

        self.assertEqual(res_question.first().user_id, ADMIN_INIT.id)
        self.assertEqual(res_question.first().number_question, 1)
        self.assertEqual(res_question.first().answer, question_reset_data1['answer1'])
        self.assertEqual(res_question_count, exp_count, "3 question reset is created")

    def test_create_question_reset_transaction(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionServiceTestCase.test_create_question_reset_transaction
        """

        # question_id outside table question
        try:
            QuestionService.create(question_reset_data_error, ADMIN_INIT.id)
        except:
            pass
        res_question_count = QuestionReset.objects.count()

        exp_count = 0

        self.assertEqual(res_question_count, exp_count, "0 question reset is created")

    def test_update_question_reset(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionServiceTestCase.test_update_question_reset
        """
        QuestionService.create(question_reset_data1, ADMIN_INIT.id)
        res_question_count1 = QuestionReset.objects.count()
        res_question1 = QuestionReset.objects.all().order_by('number_question')

        fill = {'user_id': ADMIN_INIT.id}
        list_ques = QuestionReset.objects.filter(**fill).order_by('number_question')
        QuestionService.update(question_reset_data2, list_ques)

        res_question_count2 = QuestionReset.objects.count()
        res_question2 = QuestionReset.objects.all().order_by('number_question')

        self.assertEqual(res_question2.first().user_id, ADMIN_INIT.id)
        self.assertEqual(res_question2.first().number_question, 1)
        self.assertEqual(res_question2.first().answer, question_reset_data2['answer1'])
        self.assertEqual(res_question_count1, res_question_count2, "3 question reset is updated")
