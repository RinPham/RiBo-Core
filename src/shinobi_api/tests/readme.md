Running the test

$python manage.py test

If you get problem like "Cannot add foreign key constraint", this is because authtools_ tables doing migrate before auth's table but it create a FK to auth_group's table. 
You can find details of the mysql error my issue mysql command "SHOW ENGINE INNODB STATUS;". This is known problem for Django 1.8 as describe here https://code.djangoproject.com/ticket/24311

Please continue the test by running this

$python manage.py test --keepdb

OR using memmory database for quick unittest

$python manage.py test --settings=vmscore.settings.test

$python manage.py test --pattern="*_task.py" --settings=vmscore.settings.test

Read more: https://docs.djangoproject.com/en/1.8/topics/testing/overview/ 

# Run all the tests in the vms_api.tests module
$ python manage.py test vms_api --pattern="*_message.py" --settings=vmscore.settings.test

# Run all the tests found within the 'vms_api' package
$ python manage.py test vms_api

# Run just one test case
$ python manage.py test vms_api.tests.SampleTestCase

# Run just one test method
$ python manage.py test --settings=vmscore.settings.test vms_api.tests.MessageServiceTestCase.test_list_thread
