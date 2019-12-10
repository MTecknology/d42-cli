#!/usr/bin/env python
'''
Utility functions for doing things and stuff

DEFINED EXIT :: 199
'''
import sys
import urllib


def stderr(message, level='INFO', exit_status=None):
    '''Prints a message to stderr and exits with exit_status if set.
    If exit_status is set, then level will be set to CRITICAL.
    NOTE: stdout is reserved for module output'''
    if exit_status:
        if not isinstance(exit_status, int):
            exit_status = 199
        sys.stderr.write('{}: {}\n'.format('CRITICAL', message))
        sys.exit(exit_status)
    else:
        sys.stderr.write('{}: {}\n'.format(level, message))


def confirm(prompt):
    '''Present a prompt to the user.
    Returns bool representing user response.'''
    i = 1
    while True:
        sys.stdout.write('{} [y/N]: '.format(prompt))
        val = input()
        if val == '':
            return False
        if val.lower() in ['y', 'yes', 'justdoit']:
            return True
        if val.lower() in ['n', 'no', 'notachance']:
            return False
        if i >= 3:
            return False
        i += 1


def check_deps(obj, lst=None):
    '''Checks a given object for a list of attributes.
    Returns True if all attributes are in the listed object.'''
    if not obj or not lst:
        return False
    if lst is None:
        lst = list()

    for l in lst:
        if isinstance(obj, (dict, list)):
            if not l in obj:
                return False
            if obj[l] is None:
                return False
        else:
            if not hasattr(obj, l):
                return False
            if getattr(obj, l) is None:
                return False
    return True


def strip_unicode(obj):
    '''The Michael Lustfield Function For Terminals Who Can't Write Good
    And Wanna Display Other Stuff Good Too...

    It recurses through an object and returns a matching object that has
    been stripped of unicode.'''
    if obj is None:
        return None
    elif isinstance(obj, (str, unicode)):
        return str(obj)
    elif isinstance(obj, (int, float, bool)):
        return type(obj)(obj)
    elif isinstance(obj, dict):
        new = {}
        for k, v in obj.iteritems():
            nk = strip_unicode(k)
            new[nk] = strip_unicode(v)
        return new
    elif isinstance(obj, list):
        new = []
        for v in obj:
            new.append(strip_unicode(v))
        return new
    else:
        stderr('Encountered unexpected type while decoding object. {}'.format(type(obj)), 'WARNING')
        return obj


def encode(data):
    '''Return a url encoded string from a dictionary.'''
    try:
        return str(urllib.urlencode(data))
    except:
        return None
