# #! /usr/bin/python
#
# #
# # Copyright (C) 2017 CG Vietnam, Inc
# #
# # @link http://www.codeographer.com/
# #
#
# from shinobi_api.models import Badge
# from shinobi_api.const import ReportType
# from shinobi_api.services import BaseService
#
# __author__ = "tu"
# __date__ = "$Mars 21, 2017 11:04:25 AM$"
#
#
# class ReportService(BaseService):
#
#     @classmethod
#     def report(cls, input_data, **kwargs):
#         fill = {}
#         fill['building_id'] = input_data['building_id']
#         fill['date_issued__gte'] = input_data['start_date']
#         fill['date_issued__lte'] = input_data['end_date']
#
#         if input_data['type'] == ReportType.DATE:
#             order = ['date_issued', 'time_issued']
#             badge_data = Badge.objects.filter(**fill).order_by(*order)
#
#             # convert to group data by date(Month group)
#             current_month = ''
#             des_data = []
#             data = []
#             count = 0
#             total = 0
#             for badge in badge_data:
#                 if badge.date_issued.strftime("%m/%Y") != current_month:
#                     if current_month == '':
#                         current_month = badge.date_issued.strftime("%m/%Y")
#                     else:
#                         report = {}
#                         report['date'] = current_month
#                         report['data'] = data
#                         report['count'] = count
#                         des_data.append(report)
#                         total += count
#                         current_month = badge.date_issued.strftime("%m/%Y")
#                         data = []
#                     data.append(badge)
#                     count = 1
#                 else:
#                     data.append(badge)
#                     count += 1
#             if badge_data.count() > 0:
#                 report = {}
#                 report['date'] = current_month
#                 report['data'] = data
#                 report['count'] = count
#                 des_data.append(report)
#                 total += count
#             return {
#                 'data': des_data,
#                 'total': total
#             }
#         elif int(input_data['type']) == ReportType.TYPE:
#             order = ['badge_type__name', 'date_issued', 'time_issued']
#             badge_data = Badge.objects.filter(**fill).order_by(*order)
#
#             # convert to group data by type
#             current_type = ''
#             des_data = []
#             data = []
#             count = 0
#             total = 0
#             for badge in badge_data:
#                 if badge.badge_type.name != current_type:
#                     if current_type == '':
#                         current_type = badge.badge_type.name
#                     else:
#                         report = {}
#                         report['type'] = current_type
#                         report['data'] = data
#                         report['count'] = count
#                         des_data.append(report)
#                         total += count
#                         current_type = badge.badge_type.name
#                         data = []
#                     data.append(badge)
#                     count = 1
#                 else:
#                     data.append(badge)
#                     count += 1
#             if badge_data.count() > 0:
#                 report = {}
#                 report['type'] = current_type
#                 report['data'] = data
#                 report['count'] = count
#                 des_data.append(report)
#                 total += count
#             return {
#                 'data': des_data,
#                 'total': total
#             }
#         else:
#             pass
