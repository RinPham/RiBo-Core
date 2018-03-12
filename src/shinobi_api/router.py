#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "$Jul 05, 2016 01:47:00 PM$"

from django.conf.urls import url, include
from rest_framework import routers

from shinobi_api.views import *
from shinobi_api.views import api

router = routers.SimpleRouter(trailing_slash=False)

# Public view sets
# Unauthorized users can access
router.register(r'auth', AuthViewSet, base_name="Auth")
router.register(r'user', UserViewSet, base_name="User")
router.register(r'geo', GeoViewSet, base_name='Geo')
router.register(r'page', api.PageView, base_name='Page')
router.register(r'practiced-list', api.PracticedView, base_name='PracticedView')
router.register(r'support', SupportViewSet, base_name="Support")  # Support view sets

# Visitor view sets
# Only visitors can access into these repositories
#router.register(r'visitor/auth', visitor.AuthViewSet, base_name="VisitorAuth")
#router.register(r'visitor/report', visitor.ReportViewSet, base_name='VisitorReport')
#router.register(r'visitor/terms', visitor.TermsViewSet, base_name='VisitorTerms')
#router.register(r'visitor/privacy', visitor.PrivacyViewSet, base_name='VisitorPrivacy')

# Api view
# Listening data from agents
# router.register(r'send-data', api.ListenerView.as_view(), base_name='ApiListener')

# # Manager view sets
# # Only manager can access into these repositories
# router.register(r'manager/dashboard', manager.DashboardViewSet, base_name='ManagerDashboard')
# router.register(r'manager/question', manager.QuestionViewSet, base_name='ManagerQuestion')
# router.register(r'manager/question-reset', manager.QuestionResetViewSet, base_name='ManagerQuestionReset')
# router.register(r'manager/badge_manager', manager.BadgeManagerViewSet, base_name='BadgeManager')
# router.register(r'manager/badge_type', manager.BadgeTypeViewSet, base_name='BadgeType')
# router.register(r'manager/department', manager.DepartmentViewSet, base_name='Department')
# router.register(r'manager/building_department', manager.BuildingDepartmentViewSet, base_name='BuildingDepartment')
# router.register(r'manager/print_setup', manager.PrintSetupViewSet, base_name='PrintSetup')
# router.register(r'manager/sync_schedule', manager.SyncScheduleViewSet, base_name='SyncSchedule')
# router.register(r'manager/building', manager.BuildingViewSet, base_name='Building')
# router.register(r'manager/report', manager.ReportViewSet, base_name='Report')
# router.register(r'manager/visitor', manager.VisitorViewSet, base_name='visitor')
#
# # Admin view sets
# # Only admins can access into these repositories
# router.register(r'admin/manager', admin.ManagerViewSet, base_name='AdminManager')
#
# # Staff view sets
# # Only for staff (for employees)
# router.register(r'staff/terms', staff.TermsViewSet, base_name='StaffTerms')
# router.register(r'staff/privacy', staff.PrivacyViewSet, base_name='StaffPrivacy')
# router.register(r'staff/system-meta', staff.SystemMetaViewSet, base_name='StaffSystemMeta')

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^send-data', api.ListenerView.as_view())
]
