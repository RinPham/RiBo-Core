#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = 'phuong'

from rest_framework import permissions, exceptions
from shinobi_api.services import UserService


class InternalOnly(permissions.BasePermission):
    """
    Internal access only
    """

    def has_permission(self, request, view):
        password = request.META.get('HTTP_PASSWORD')
        if password:
            return True
        else:
            return False


class IsAuthenticated(permissions.BasePermission):
    """
    Global permission check for login user access
    """

    exceptions = [
        'post_auth', 'post_user'
    ]

    def has_permission(self, request, view):
        if self.get_action(request, view) in self.exceptions:
            return True
        return request.user and request.user.is_authenticated()

    def get_action(self, request, view):
        method = request.method.lower()
        view_set = getattr(view, 'view_set', '')
        method = method + "_" + view_set
        return method

class IsManager(IsAuthenticated):
    """
    Only manager can fire this action
    """

    def has_permission(self, request, view):
        has_permission = super(IsManager, self).has_permission(request, view)
        if has_permission:
            return request.user.is_manager
        return False

class IsVisitor(IsAuthenticated):
    """
    Only visitor can fire this action
    """
    exceptions = ['post_visitor_auth']

    def has_permission(self, request, view):
        if self.get_action(request, view) in self.exceptions:
            return True
        if super(IsVisitor, self).has_permission(request, view):
            return request.user.is_guest
        return False


class IsSuperuser(permissions.BasePermission):
    """
    Only staff can access this are
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return request.user.is_superuser


class IsStaff(permissions.BasePermission):
    """
    Only staff can access this are
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return request.user.is_staff or request.user.is_superuser


class NotAuthenticated(permissions.BasePermission):
    """
    Global check permission, only non login can access
    """

    def has_permission(self, request, view):
        return (not request.user or not request.user.is_authenticated())


def allow_access_user(current, user, raise_exception=True):
    """
    Check current user can access user data
    :param current: int user id or User object
    :param user: int manager id or User object
    :param raise_exception: set to True to raise exception
    :return: boolean allowed or not
    """
    return True
    # TODO: change this logic, since user.manager_id has not set
    allowed = False
    if not isinstance(current, int):
        user_id = current.manager_id
    else:
        user_id = current
    if not isinstance(user, int):
        manager_id = user.manager_id
    else:
        manager_id = user
    if manager_id == user_id:
        allowed = True
    if not allowed and raise_exception:
        raise exceptions.PermissionDenied()
    return allowed