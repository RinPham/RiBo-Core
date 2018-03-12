#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from os.path import join
from shinobi_core.settings import BASE_DIR
from tests.test_base import BaseTestCase
from shinobi_api.models.user import User
from shinobi_api.models import (
    SystemMeta, AppMeta
)
from shinobi_api.services.msystem import MSystemService
from shinobi_api.services.utils import Utils

__author__ = "hien"
__date__ = "$Oct 7th 2016, 08:55 AM$"


class MSystemServiceTestCase(BaseTestCase):
    
    def test_add_system_app(self):
        app_data = {
            "version": "v0.0.1",
            "version_name": "VMS: Innovative Visitor Management System",
            "changes": "- New layout\n- New features",
            "available_at": "2017-05-20",
            "is_latest": 1,
            "is_force_updated": 1
        }
        sys_app = MSystemService.save(app_data)
        self.assertEqual(sys_app is not None, True)
        apps = MSystemService.get_apps()
        Utils.dump(apps)
        self.assertEqual(len(apps) == 1, True)
        latest_app = MSystemService.get_latest()
        self.assertEqual(latest_app is not None, True)
        user_id = 19
        user_app_data = {
            "version": "v0.0.1"
        }
        validation = MSystemService.validate_user_app(user_id, **user_app_data)
        Utils.dump(validation)
        deleted = MSystemService.delete_app(sys_app.id)
        self.assertEqual(deleted, True)
        apps = MSystemService.get_apps()
        Utils.dump(apps)
        self.assertEqual(len(apps) == 0, True)
