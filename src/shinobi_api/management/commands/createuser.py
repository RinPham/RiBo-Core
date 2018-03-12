from __future__ import unicode_literals

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "07 08 2016, 10:34 AM"

import getpass
import sys
import copy

from django.contrib.auth import get_user_model
from django.contrib.auth.management import get_default_username
from django.core import exceptions
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS
from django.utils.encoding import force_str
from django.utils.six.moves import input
from django.utils.text import capfirst
from shinobi_api.const import UserType, USER_TYPE_CHOICES
from shinobi_api.services import UserService
from shinobi_api.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Used to create a visitor, manager.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)

    def add_arguments(self, parser):
        parser.add_argument('--type', action='store', dest='type',
                            default=False,
                            help='Specifies user type to use. Default is manager.')

    def execute(self, *args, **options):
        self.stdin = options.get('stdin', sys.stdin)  # Used for testing
        return super(Command, self).execute(*args, **options)

    def handle(self, *args, **options):
        database = options.get('database', DEFAULT_DB_ALIAS)
        username = options.get(User.USERNAME_FIELD)
        user_type = options.get('type', None)
        password = None
        user_data = {}
        fake_user_data = {}
        default_username = get_default_username()
        try:
            # Get a username
            verbose_field_name = self.username_field.verbose_name
            while username is None:
                input_msg = capfirst(verbose_field_name)
                if default_username:
                    input_msg += " (leave blank to use '%s')" % default_username
                username_rel = self.username_field.rel
                input_msg = force_str('%s%s: ' % (
                    input_msg,
                    ' (%s.%s)' % (
                        username_rel.to._meta.object_name,
                        username_rel.field_name
                    ) if username_rel else '')
                )
                username = self.get_input_data(self.username_field, input_msg, default_username)
                if not username:
                    continue
                try:
                    User._default_manager.db_manager(database).get_by_natural_key(username)
                except User.DoesNotExist:
                    pass
                else:
                    self.stderr.write("Error: That %s is already taken." %
                            verbose_field_name)
                    username = None
            user_type_choises = copy.deepcopy(USER_TYPE_CHOICES)
            user_type_choises.sort(key=lambda tup: tup[0])
            types = [('%s:%s' % tp) for tp in user_type_choises]
            msg = 'Type (%s):' % (' '.join(types))
            while not user_type or not UserType.is_valid_type(user_type):
                user_type = self.get_input_data('user_type', msg)
                if not user_type:
                    continue
                user_type = int(user_type)
                if not UserType.is_valid_type(user_type):
                    self.stderr.write("Error: Invalid user type")
                    user_type = False
                
            manager_id = 0
            if user_type in [UserType.VISITOR, UserType.MANAGER]:
                while not manager_id:
                    raw_value = input('Manager id: ')
                    try:
                        manager_id = int(raw_value)
                        manager = User.objects.get(id=manager_id)
                        if not manager.user_type in [UserType.STAFF]:
                            raise Exception('Only staff can doing this, type = '+str(manager.user_type))
                    except Exception as pe:
                        if user_type == UserType.MANAGER:
                            print ("No manager set: "+str(pe))
                            #not required
                            break
                        else:
                            self.stderr.write("Error: Invalid manager id: "+str(pe))
                            manager_id = 0

            for field_name in User.REQUIRED_FIELDS:
                field = User._meta.get_field(field_name)
                user_data[field_name] = options.get(field_name)
                while user_data[field_name] is None:
                    message = force_str('%s%s: ' % (
                        capfirst(field.verbose_name),
                        ' (%s.%s)' % (
                            field.remote_field.model._meta.object_name,
                            field.remote_field.field_name,
                        ) if field.remote_field else '',
                    ))
                    input_value = self.get_input_data(field, message)
                    user_data[field_name] = input_value
                    fake_user_data[field_name] = input_value
                    if field.remote_field:
                        fake_user_data[field_name] = field.remote_field.model(input_value)

            profile = {}
            if user_type in [UserType.SUPERUSER, UserType.STAFF]:
                profile = {
                    'gender': 1,
                    'dob': '1988-12-12'
                }
            for field_name in ['gender', 'dob']:
                field = UserProfile._meta.get_field(field_name)
                while profile.get(field_name, None) is None:
                    message = force_str('%s%s: ' % (
                        capfirst(field.verbose_name),
                        ' (%s.%s)' % (
                            field.remote_field.model._meta.object_name,
                            field.remote_field.field_name,
                        ) if field.remote_field else '',
                    ))
                    input_value = self.get_input_data(field, message)
                    profile[field_name] = input_value

            while password is None:
                password = getpass.getpass()
                password2 = getpass.getpass(force_str('Password (again): '))
                if password != password2:
                    self.stderr.write("Error: Your passwords didn't match.")
                    password = None
                    continue

        except KeyboardInterrupt:
            self.stderr.write("\nOperation cancelled.")
            sys.exit(1)

        if username:
            if user_type == UserType.SUPERUSER:
                user_data['is_superuser'] = True
                user_data['is_staff'] = True
                user_data['is_active'] = True
            if user_type == UserType.STAFF:
                user_data['is_staff'] = True
                user_data['is_active'] = True

            user_data['manager_id'] = manager_id
            user_data[User.USERNAME_FIELD] = username
            user_data['password'] = password
            user_data['manager_id'] = int(manager_id)
            user_data['user_type'] = user_type
            user_data['profile'] = profile
            UserService.save(user_data)
            if options['verbosity'] >= 1:
                self.stdout.write("User created successfully.")

    def get_input_data(self, field, message, default=None):
        raw_value = input(message)
        if default and raw_value == '':
            raw_value = default
        try:
            val = field.clean(raw_value, None)
        except exceptions.ValidationError as e:
            self.stderr.write("Error: %s" % '; '.join(e.messages))
            val = None
        except Exception:
            val = raw_value
        return val
