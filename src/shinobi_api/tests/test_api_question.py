#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
import copy
from rest_framework.test import APITestCase

from shinobi_api.models import QuestionReset
from shinobi_api.services import UserService
from shinobi_api.tests import user_init, head

__author__ = "tu"
__date__ = "05 16 2017, 9:45 AM"

question_reset_1 = {
    'id': 1,
    'question_id': '1',
    'number_question': '1',
    'answer': 'answer 1',
}
question_reset_2 = {
    'id': 2,
    'question_id': '2',
    'number_question': '2',
    'answer': 'answer 2',
}
question_reset_3 = {
    'id': 3,
    'question_id': '3',
    'number_question': '3',
    'answer': 'answer 3',
}


class QuestionAPITestCase(APITestCase):
    """
    python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionAPITestCase
    """

    def setUp(self):
        global ADMIN_INIT
        global BUILDING_INIT

        admin_test = copy.deepcopy(user_init)
        ADMIN_INIT = UserService.save(admin_test)

        question_reset_1['user_id'] = ADMIN_INIT.id
        question_reset_2['user_id'] = ADMIN_INIT.id
        question_reset_3['user_id'] = ADMIN_INIT.id
        QuestionReset.objects.create(**question_reset_1)
        QuestionReset.objects.create(**question_reset_2)
        QuestionReset.objects.create(**question_reset_3)

    def test_question_reset_by_email(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionAPITestCase.test_question_reset_by_email
        """
        url = '/api/v1/manager/question-reset/by_email'
        data = {'email': user_init['email']}
        exp_json = {
                    "question": [
                        {
                            "id": 1,
                            "question": {
                                "id": 1,
                                "question": "What is the first and last name of your first boyfriend or girlfriend?"
                            },
                            "number_question": 1,
                            "user": ADMIN_INIT.id
                        },
                        {
                            "id": 2,
                            "question": {
                                "id": 2,
                                "question": "Which phone number do you remember most from your childhood?"
                            },
                            "number_question": 2,
                            "user": ADMIN_INIT.id
                        },
                        {
                            "id": 3,
                            "question": {
                                "id": 3,
                                "question": "What was your favorite place to visit as a child?"
                            },
                            "number_question": 3,
                            "user": ADMIN_INIT.id
                        }
                      ]
                    }
        response = self.client.post(url, data, **head)
        self.assertEqual(3, len(response.data['question']))
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_question_reset(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionAPITestCase.test_question_reset
        """

        # login
        url = '/api/v1/auth'
        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'
        }
        response = self.client.post(url, data, **head)
        TOKEN = response.data['token']

        url = '/api/v1/manager/question-reset'
        exp_json = {
                    "list_ques": [
                        {
                            "id": 1,
                            "question": {
                                "id": 1,
                                "question": "What is the first and last name of your first boyfriend or girlfriend?"
                            },
                            "number_question": 1,
                            "user": ADMIN_INIT.id
                        },
                        {
                            "id": 2,
                            "question": {
                                "id": 2,
                                "question": "Which phone number do you remember most from your childhood?"
                            },
                            "number_question": 2,
                            "user": ADMIN_INIT.id
                        },
                        {
                            "id": 3,
                            "question": {
                                "id": 3,
                                "question": "What was your favorite place to visit as a child?"
                            },
                            "number_question": 3,
                            "user": ADMIN_INIT.id
                        }
                      ]
                    }
        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.get(url, **head_copy)
        self.assertEqual(3, len(response.data['list_ques']))
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)

    def test_config_question_reset(self):
        """
        python manage.py test --settings=shinobi_core.settings.test shinobi_api.tests.QuestionAPITestCase.test_config_question_reset
        """

        # login
        url = '/api/v1/auth'
        data = {
            'email': 'admintest@example.com',
            'password': 'abc123'
        }
        response = self.client.post(url, data, **head)

        data = {
            'question1': 4,
            'question2': 5,
            'question3': 6,
            'answer1': 'answer 4',
            'answer2': 'answer 5',
            'answer3': 'answer 6',
        }
        TOKEN = response.data['token']

        url = '/api/v1/manager/question-reset/config'
        exp_json = {
            "message": "Config question successfully"
        }
        head_copy = copy.deepcopy(head)
        head_copy['HTTP_AUTHORIZATION'] = 'token {}'.format(TOKEN)
        response = self.client.post(url, data, **head_copy)
        self.assertJSONEqual(response.content.decode("utf-8"), exp_json)
