# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-27 05:37
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shinobi_api.models.user
import shinobi_api.models.usertypes


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, max_length=30, verbose_name='middle name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='Required. 245 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=254, null=True, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_disabled', models.BooleanField(default=False)),
                ('manager_id', models.PositiveIntegerField(default=0)),
                ('user_type', shinobi_api.models.usertypes.TinyIntegerField(choices=[(1, 'Guest'), (2, 'Visitor'), (3, 'Employee'), (4, 'Manager'), (5, 'Staff'), (6, 'Superuser')], default=1)),
            ],
            options={
                'db_table': 'auth_user',
                'verbose_name': 'user',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', shinobi_api.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin1',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country_code', models.CharField(max_length=2)),
                ('admin1_code', models.CharField(max_length=5)),
                ('admin1_name', models.CharField(max_length=64)),
                ('timezone', models.CharField(max_length=128)),
                ('latitude', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'db_table': 'vms_admin1',
            },
        ),
        migrations.CreateModel(
            name='Api',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expired_at', models.DateTimeField(default='2000-10-10 00:00:00')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('device', models.CharField(max_length=64)),
                ('ip', models.GenericIPAddressField()),
                ('token', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=40)),
                ('type', shinobi_api.models.usertypes.PositiveTinyIntegerField(default=0)),
                ('app_id', models.CharField(default='', max_length=64)),
            ],
            options={
                'db_table': 'vms_apis',
            },
        ),
        migrations.CreateModel(
            name='AppKey',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('activated_at', models.DateTimeField(null=True, verbose_name='Actived at')),
            ],
            options={
                'db_table': 'vms_app_keys',
            },
        ),
        migrations.CreateModel(
            name='AppMeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(default='v0.0.1', max_length=10)),
                ('installed_at', models.DateTimeField(default=None, null=True)),
                ('last_updated', models.DateTimeField(default=None, null=True)),
                ('is_active', shinobi_api.models.usertypes.TinyIntegerField(default=1)),
            ],
            options={
                'db_table': 'vms_app_meta',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country_code', models.CharField(max_length=2)),
                ('country_name', models.CharField(max_length=64)),
                ('currency', models.CharField(default='', max_length=3)),
            ],
            options={
                'db_table': 'vms_countries',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=256)),
            ],
            options={
                'db_table': 'vms_department',
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', shinobi_api.models.usertypes.NormalTextField()),
                ('answer', shinobi_api.models.usertypes.NormalTextField()),
            ],
            options={
                'db_table': 'vms_faq',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('short', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'vms_languages',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=2)),
                ('admin1_name', models.CharField(max_length=64)),
                ('admin1_code', models.CharField(default='', max_length=2)),
                ('city', models.CharField(max_length=64)),
                ('latitude', models.DecimalField(decimal_places=7, default=0, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=7, default=0, max_digits=10)),
                ('weight', shinobi_api.models.usertypes.TinyIntegerField(default=0)),
            ],
            options={
                'db_table': 'vms_locations',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('api_id', models.PositiveIntegerField(default=0)),
                ('user_agent', models.CharField(max_length=256)),
                ('ip', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('device_id', models.CharField(default='', max_length=256)),
                ('time_since_last_login', models.PositiveIntegerField(default=0)),
                ('time_since_last_open_app', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'vms_logins',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('dom_structure', models.TextField()),
                ('apis', models.TextField()),
                ('active_elements', models.TextField()),
                ('technology', models.CharField(default='', max_length=100)),
                ('version', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'shinobi_page',
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Privacy')),
                ('updated_at', models.DateTimeField(verbose_name='Updated at')),
            ],
            options={
                'db_table': 'vms_privacy',
            },
        ),
        migrations.CreateModel(
            name='SystemMeta',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(default='v0.0.1', max_length=10)),
                ('version_name', models.CharField(default='VMS v0.0.1', max_length=50)),
                ('changes', shinobi_api.models.usertypes.NormalTextField(default=None)),
                ('available_at', models.DateTimeField(default=None, null=True)),
                ('is_latest', shinobi_api.models.usertypes.TinyIntegerField(default=1)),
                ('is_force_updated', shinobi_api.models.usertypes.TinyIntegerField(default=0)),
            ],
            options={
                'ordering': ['-id'],
                'db_table': 'vms_system_meta',
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Terms')),
                ('updated_at', models.DateTimeField(verbose_name='Updated at')),
            ],
            options={
                'db_table': 'vms_terms',
            },
        ),
        migrations.CreateModel(
            name='UserActivityLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField()),
                ('action', models.CharField(max_length=6, verbose_name='Action')),
                ('status', models.SmallIntegerField(default=200, verbose_name='Request status code')),
                ('url', models.CharField(default='', max_length=2000, verbose_name='Url')),
                ('meta', shinobi_api.models.usertypes.NormalTextField(default='{}', verbose_name='Meta data')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('latest_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('device_type', shinobi_api.models.usertypes.TinyIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'activity_log',
                'verbose_name_plural': 'activity_logs',
                'db_table': 'vms_user_activity_logs',
            },
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('email', models.CharField(default='', max_length=255, unique=True)),
                ('is_primary', models.BooleanField(default=0)),
                ('token', models.CharField(default='', max_length=40)),
                ('verified_at', models.PositiveIntegerField(default=0)),
                ('created_at', models.PositiveIntegerField(default=1446015876)),
                ('unsubscribe_at', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'vms_emails',
            },
        ),
        migrations.CreateModel(
            name='UserMedia',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('origin_uri', models.CharField(default='', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('mime_type', models.CharField(default='', max_length=10)),
                ('thumb_uri', models.CharField(default='', max_length=255)),
                ('s3_name', models.CharField(default='', max_length=255)),
                ('expires_at', models.IntegerField(default=0)),
                ('origin_w', models.PositiveIntegerField(default=0)),
                ('origin_h', models.PositiveIntegerField(default=0)),
                ('thumb_w', models.PositiveIntegerField(default=0)),
                ('thumb_h', models.PositiveIntegerField(default=0)),
                ('on_remove', shinobi_api.models.usertypes.PositiveTinyIntegerField(default=0)),
            ],
            options={
                'db_table': 'vms_user_medias',
            },
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pref_id', shinobi_api.models.usertypes.PositiveTinyIntegerField(default=0)),
                ('pref_value', models.CharField(default='', max_length=255)),
                ('extra_param', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'vms_users_prefs',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', shinobi_api.models.usertypes.TinyIntegerField(choices=[(0, 'Male'), (1, 'Female')], default=2)),
                ('dob', models.DateField(default=datetime.date.today, verbose_name='Date of birth')),
                ('avatar', models.CharField(default='', max_length=255)),
                ('msg_indicator', models.PositiveIntegerField(default=0)),
                ('head_shot_media_id', models.PositiveIntegerField(default=0)),
                ('NPI', models.PositiveIntegerField(default=None, null=True, unique=True)),
                ('home_phonenumber', models.CharField(default='', max_length=15, verbose_name='Home phone number')),
                ('mobile_phonenumber', models.CharField(default='', max_length=15, verbose_name='Mobile phone number')),
                ('address1', models.CharField(default='', max_length=255, verbose_name='Address line 1')),
                ('address2', models.CharField(default='', max_length=255, verbose_name='Address line 2')),
                ('zip_code', models.CharField(default='', max_length=6, verbose_name='Zipcode')),
                ('city', models.CharField(default='', max_length=64, verbose_name='City')),
                ('location_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'vms_user_profiles',
            },
        ),
        migrations.AddField(
            model_name='userpref',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermedia',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useractivitylog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='loginlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appmeta',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appkey',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='api',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
