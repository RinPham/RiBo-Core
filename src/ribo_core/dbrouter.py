from django.conf import settings

IS_TEST = False
TEST_FLAG = '__TEST'

class DbRouterMiddleware(object):
    def process_request( self, request):
        global IS_TEST
        IS_TEST = request.GET.get(TEST_FLAG)
        return None

    def process_response( self, request, response ):
        global IS_TEST
        IS_TEST = False
        return response

class DatabaseRouter (object):
    # def db_for_read( self, model, **hints ):
    #     return 'test' if IS_TEST else 'default';
    #
    # def db_for_write( self, model, **hints ):
    #     return 'test' if IS_TEST else 'default';
    #
    # def allow_relation( self, obj1, obj2, **hints ):
    #     return True
    #
    # def allow_migrate( self, db, app_label, model_name=None, **hints ):
    #     return True
    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return 'test' if IS_TEST else 'default';

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return 'test' if IS_TEST else 'default';

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return True

    def allow_migrate(self, db, model):
        """Make sure that apps only appear in the related database."""
        """ No migrate all database no_sql and model have ap_label = no_sql"""
        if db == 'no_sql' or model._meta.app_label == "no_sql":
            return False
        else:
            return True

