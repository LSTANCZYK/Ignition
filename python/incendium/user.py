# Copyright (C) 2018
# Author: Cesar Roman
# Contact: thecesrom@gmail.com

"""Incendium User module."""

__all__ = [
    'get_emails',
    'get_user'
]

import system.security
import system.user


class _User(object):
    """Wrapper class for Ignition's User object."""

    def __init__(self, user):
        """User initializer.

        Args:
            user (User): Ignition's user object.
        """
        self._username = user.get(user.Username)
        self._first_name = user.get(user.FirstName)
        self._last_name = user.get(user.LastName)
        self._locale = user.getOrDefault(user.Language)

    def get_first_name(self):
        """Returns User's first name.

        Returns:
            str: User's first name.
        """
        return self._first_name

    def get_full_name(self):
        """Returns User's full name.

        Returns:
            str: User's full name.
        """
        return ' '.join([self._first_name, self._last_name])

    def get_locale(self):
        """Returns User's preferred language.

        Returns:
            str: User's preferred language.
        """
        return self._locale


def get_emails(user_source='', filter_role=''):
    """Gets a list of email addresses.

    Args:
        user_source (str): The name of the User Source. If not provided,
            the default User Source will be consulted. Optional.
        filter_role (str): The name of the role. If provided, a list of
            email addresses for users that are assigned to a matching
            role will be retrieved, otherwise all email addresses will
            be retrieved. Optional.

    Returns:
        list[str]: A list of email addresses.
    """
    # Initialize variables.
    emails = set()

    # Retrieve users from the User Source.
    users = system.user.getUsers(user_source)

    for user in users:
        _emails = [ci.value for ci in user.getContactInfo()
                   if ci.contactType == 'email']
        for email in _emails:
            if filter_role:
                if filter_role in user.getRoles():
                    emails.add(email)
            else:
                emails.add(email)

    return sorted(list(emails))


def get_user(user_source, failover=None):
    """Looks up the logged-in User in a User Source.

    Args:
        user_source (str): The name of the User Source.
        failover (str): The name of the Failover profile. Optional.

    Returns:
        _User: A User object.
    """
    # Initialize variables
    user = None
    user_obj = None
    _username = system.security.getUsername()

    # Try User Source.
    if user_source:
        user = system.user.getUser(user_source, _username)
    # Try Failover.
    if not user and failover:
        user = system.user.getUser(failover, _username)

    if user:
        user_obj = _User(user)

    return user_obj
