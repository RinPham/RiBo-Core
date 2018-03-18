from rest_framework import status
from oauth2client.client import AccessTokenCredentialsError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api import permissions
from ribo_api.exceptions import TokenExpired
from ribo_api.models.task import Task
from ribo_api.models.user import User
from ribo_api.serializers.event import EventSerializer
from ribo_api.services.oauth import OauthService
from ribo_api.services.utils import Utils


class EventViewSet(ViewSet):
    view_set = 'event'
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /user Create new user
        @apiName Create
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {string} email
        @apiParam {string} password
        @apiParam {string} [first_name]
        @apiParam {string} [middle_name]
        @apiParam {string} [last_name]
        @apiParam {object} profile
        @apiParam {number} [profile.gender] (0: male, 1: female)
        @apiParam {string} [profile.dob]
        @apiParam {file} [profile.avatar] upload file
        @apiParam {string} [profile.address1]
        @apiParam {string} [profile.address2]
        @apiParam {string} [profile.zip_code]
        @apiParam {string} [profile.city]
        @apiParam {string} [profile.home_phonenumber] Home phone
        @apiParam {string} [profile.mobile_phonenumber] Mobile phone

        @apiSuccess {object} user
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            items = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
            return Response(items)
        except AccessTokenCredentialsError as e:
            raise TokenExpired()
        except Exception as e:
            raise e

    def create(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /user Create new user
        @apiName Create
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {string} email
        @apiParam {string} password
        @apiParam {string} [first_name]
        @apiParam {string} [middle_name]
        @apiParam {string} [last_name]
        @apiParam {object} profile
        @apiParam {number} [profile.gender] (0: male, 1: female)
        @apiParam {string} [profile.dob]
        @apiParam {file} [profile.avatar] upload file
        @apiParam {string} [profile.address1]
        @apiParam {string} [profile.address2]
        @apiParam {string} [profile.zip_code]
        @apiParam {string} [profile.city]
        @apiParam {string} [profile.home_phonenumber] Home phone
        @apiParam {string} [profile.mobile_phonenumber] Mobile phone

        @apiSuccess {object} user
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            data = request.data.copy()
            timezone = data.get("timezone", "UTC")
            event = {
                'summary': data.get('summary',None),
                'location': data.get('location',None),
                'description': data.get('description',None),
                'start': {
                    'dateTime': data.get('start_time',None),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': data.get('end_time',None),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            return Response(event)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def update(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /user update user
        @apiName update
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {string} email
        @apiParam {string} password
        @apiParam {string} [first_name]
        @apiParam {string} [middle_name]
        @apiParam {string} [last_name]
        @apiParam {object} profile
        @apiParam {number} [profile.gender] (0: male, 1: female)
        @apiParam {string} [profile.dob]
        @apiParam {file} [profile.avatar] upload file
        @apiParam {string} [profile.address1]
        @apiParam {string} [profile.address2]
        @apiParam {string} [profile.zip_code]
        @apiParam {string} [profile.city]
        @apiParam {string} [profile.home_phonenumber] Home phone
        @apiParam {string} [profile.mobile_phonenumber] Mobile phone

        @apiSuccess {object} user
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            data = request.data.copy()
            timezone = data.get("timezone", "UTC")
            event_id = kwargs.get("pk",None)
            if event_id:
                event = {
                    'summary': data.get('summary', None),
                    'location': data.get('location', None),
                    'description': data.get('description', None),
                    'start': {
                        'dateTime': data.get('start_time', None),
                        'timeZone': timezone,
                    },
                    'end': {
                        'dateTime': data.get('end_time', None),
                        'timeZone': timezone,
                    },
                    'reminders': {
                        'useDefault': False,
                    },
                }
                event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
                return Response(event)
            else:
                return Response("Event id is wrong!", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def delete(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /user update user
        @apiName update
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {string} email
        @apiParam {string} password
        @apiParam {string} [first_name]
        @apiParam {string} [middle_name]
        @apiParam {string} [last_name]
        @apiParam {object} profile
        @apiParam {number} [profile.gender] (0: male, 1: female)
        @apiParam {string} [profile.dob]
        @apiParam {file} [profile.avatar] upload file
        @apiParam {string} [profile.address1]
        @apiParam {string} [profile.address2]
        @apiParam {string} [profile.zip_code]
        @apiParam {string} [profile.city]
        @apiParam {string} [profile.home_phonenumber] Home phone
        @apiParam {string} [profile.mobile_phonenumber] Mobile phone

        @apiSuccess {object} user
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            event_id = kwargs.get("pk",None)
            if event_id:
                service.events().delete(calendarId='primary',  eventId=event_id).execute()
                return Response("Deleted")
        except Exception as e:
            Utils.log_exception(e)
            raise e