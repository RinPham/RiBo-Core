#! /usr/bin/python
#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from shinobi_api.services.base import *
from shinobi_api.services.user import UserService
from template_email import TemplateEmail
from shinobi_api.services.queue import QueueService
from shinobi_core.settings.base import SUPPORT_EMAIL
from django.conf import settings
from shinobi_api.services.utils import Utils

__author__ = "hien"
__date__ = "$Jul 05, 2016 2:04:38 PM$"


def get_template(name):
    return 'emails/{}.html'.format(name)


class EmailError(TypeError):
    pass  # base exception class


class EmailService(BaseService):
    __REPLY_TO = 'no-reply@smartoffice.vn'
    __FROM_ADMIN = 'admin@smartoffice.vn'
    __UNSUBSCRIBE_LINK = '/unsubscribe/'
    __SUPPORT_LINK = '/support'
    __PRIVACY_LINK = '/legal?page=privacy'
    __BRAND_NAME = 'VMS'

    @classmethod
    def _process_queue(cls, data):
        cls.sm_do_send(**data)
        return True

    @classmethod
    def sm_do_send(cls, subject, to_add, context, template_name, reply_to=None):
        try:
            context['unsubscribe_link'] = False  # unable to unsuncrible, example system email
            if context.get("email_token", None):
                context['unsubscribe_link'] = Utils.get_public_url(cls.__UNSUBSCRIBE_LINK + context.get("email_token"))
            context['public_base'] = Utils.get_public_url()
            context['privacy_link'] = Utils.get_public_url(cls.__PRIVACY_LINK)
            context['support_link'] = Utils.get_public_url(cls.__SUPPORT_LINK)
            bcc = context.get("bcc", [])
            if to_add[0] == settings.BCC_EMAIL_ADDRESS:
                pass
            else:
                if settings.ALLOWED_EMAILS != "*":
                    if settings.ALLOWED_EMAILS:
                        to_add = [settings.ALLOWED_EMAILS]
                    else:
                        Utils.log("settings.ALLOWED_EMAILS is empty")
                        return
            mail = TemplateEmail(
                subject=subject,
                template=template_name,
                context=context,
                from_email=u"{} Support <{}>".format(cls.__BRAND_NAME, settings.SUPPORT_EMAIL),
                to=to_add,
                bcc=bcc,
                headers={"Reply-To": reply_to or cls.__REPLY_TO},
            )
            mail.send()
        except Exception as e:
            cls.log_exception(e)

    @classmethod
    def _sm_send_email(cls, subject, to_add, context, template_name, reply_to=None, queue=True):
        data = {
            "subject": subject,
            "to_add": to_add,
            "context": context,
            "template_name": template_name,
            "reply_to": reply_to,
        }
        if queue:
            queued = QueueService.async_job(QueueService.QUEUE_NAME_EMAIL, 'shinobi_api.tasks.send_email', data, delayed_time=0)
            return queued
        else:
            EmailService._process_queue(data)

    @classmethod
    def verify_email(cls, token, email_add, *args, **kwargs):
        """
        Verify email address and active account
        """
        template_name = kwargs.pop('template', 'verify')
        template_name = get_template(template_name)
        uid = kwargs.pop('uid', 'activation')
        subject = "Welcome to {}".format(cls.__BRAND_NAME)
        user_email = email_add
        verify_link = ""
        verify_link = Utils.get_public_url('/verify/{}/{}'.format(uid, token))
        context = {
            'verify_link': verify_link,
            'email': email_add,
            'password': kwargs.pop('password', None)
        }
        cls._sm_send_email(subject, [user_email], context, template_name, False, False)

    @classmethod
    def reset_link(cls, token, uid, *args, **kwargs):
        """
        Send reset password link
        """
        user = kwargs.get('user', None)
        user_id = kwargs.get('user_id', None)
        if not user and not user_id:
            raise EmailError('Please provide user or user id param.')
        if not user:
            user = UserService.get_user(user_id)
        template_name = get_template('reset-password')
        subject = 'Somebody requested a new password for your {} account'.format(cls.__BRAND_NAME)
        user_email = '"%s" <%s>' % (user.get_full_name(), user.email)
        link = Utils.get_public_url('/password/reset/{}/{}'.format(uid.decode('utf-8'), token))
        context = {
            'reset_link': link,
            'username': user.email
        }
        cls._sm_send_email(subject, [user_email], context, template_name, False, False)

    @classmethod
    def support_ticket(cls, name, email, message):
        template_name = get_template('support-ticket')
        subject = 'NEW SUPPORT TICKET'
        context = {
            'name': name,
            'message': message
        }
        cls._sm_send_email(subject, [SUPPORT_EMAIL], context, template_name, reply_to=email)

    @classmethod
    def reset_pin(cls, key, pin, *args, **kwargs):
        user = kwargs.get('user', None)
        user_id = kwargs.get('user_id', None)
        if not user and not user_id:
            raise EmailError('Please provide user or user id param.')
        if not user:
            user = UserService.get_user(user_id)

        template_name = get_template('reset-pin')
        subject = 'Somebody requested a new PIN for your {} account'.format(cls.__BRAND_NAME)
        user_email = '"%s" <%s>' % (user.get_full_name(), user.email)
        context = {
            'key': key,
            'pin': pin,
            'username': user.email
        }
        cls._sm_send_email(subject, [user_email], context, template_name, False, False)

    @classmethod
    def plain_text_email(cls, user_email ,*args, **kwargs):
        body = kwargs.pop('body', '')
        from_email = kwargs.pop('from_email', '')
        subject = kwargs.pop('subject', '')
        template_name = get_template('plain_text')
        try:
            from html import escape  # python 3.x
        except ImportError:
            from cgi import escape  # python 2.x
        context = {
            "email_body": body,#.replace("\n",escape("<br/>"))
            "from_email": from_email
        }
        cls._sm_send_email(subject, [user_email], context, template_name)

    @classmethod
    def _test_email(cls, to_add):
        template_name = get_template('test')
        subject = "test subject"
        context = {
            "test_name": "test name here"
        }
        cls._sm_send_email(subject, [to_add], context, template_name)
