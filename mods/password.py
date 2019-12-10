#!/usr/bin/env python
'''
Module to perform operations on D42 passwords.

DEFINED EXIT :: 125, 126, 129
'''
from lib.util import check_deps, encode, confirm


##
# MODULE HOOKS
##

def modhook_options(opts):
    ''' MODULE HOOK :: OPTIONS '''
    # Group: operations
    opts.opt(
        'operations', '-sp', '--search-passwords',
        action='store_const', const='password.op_search_passwords', dest='operation',
        help='Search for passwords within given parameters')

    opts.opt(
        'operations', '-cp', '--create-password',
        action='store_const', const='password.op_create_password', dest='operation',
        help='Create a password in D42; <username, password>')

    opts.opt(
        'operations', '-up', '--update-password',
        action='store_const', const='password.op_update_password', dest='operation',
        help='Update details of a password; <id>')

    opts.opt(
        'operations', '-gp', '--get-secret',
        action='store_const', const='password.op_get_password', dest='operation',
        help='Display a password; single-return query')

    opts.opt(
        'operations', '-dp', '--delete-password',
        action='store_const', const='password.op_delete_password', dest='operation',
        help='Delete a password; <password_id>')


##
# HOOK FUNCTIONS
##

def op_create_password(d42):
    '''
    Create a new password in D42.
    Required Parameters: username, password
    '''
    if not check_deps(d42.params, ['username', 'password']):
        d42.err('Required options were not found: username, password', 125)
        return False

    ret = d42.api('/passwords/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 126, ret['data'])
        return False
    d42.out(ret)


def op_update_password(d42):
    '''
    Update an existing password in D42.
    Required Parameters: id
    '''
    if not check_deps(d42.params, ['id']):
        d42.err('Required options were not found: id', 125)
        return False

    ret = d42.api('/passwords/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 126, ret['data'])
        return False

    d42.out(ret)
    return True


def op_get_password(d42):
    '''
    Get a single password.
    Requires search to return a single value.
    Provides only raw or secret output.
    '''
    qs = '?{}'.format(encode(d42.params)) if d42.params is not None else ''
    ret = d42.api('/passwords/{}'.format(qs))

    if not ret['result']:
        d42.err(ret['data'], 125)
        return False

    if not 'Passwords' in ret['data']:
        d42.err('Invalid results returned from API', 125)
        return False
    elif len(ret['data']['Passwords']) > 1:
        d42.err('Too many passwords in D42 match this query', 125)
        return False
    elif len(ret['data']['Passwords']) < 1:
        d42.err('No passwords in D42 match this query', 125)
        return False

    ret = d42.api('/passwords/{}{}'.format(qs, '&plain_text=yes'))

    if not ret['result']:
        d42.err('API Error', 126, ret['data'])
        return False

    pw = ret['data']['Passwords'][0]['password']
    # If raw output was requested, provide the raw password to the shell.
    if d42.opts.output == 'raw':
        d42.out(pw, fmt='raw')
    else:
        d42.out(pw, fmt='secret')

    return True


def op_search_passwords(d42):
    '''
    Search for passwords within D42.
    With no parameters specified, all results are returned.
    '''
    qs = '?{}'.format(encode(d42.params)) if d42.params is not None else ''
    ret = d42.api('/passwords/{}'.format(qs))

    if not ret['result']:
        d42.err('API Error', 126, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_delete_password(d42):
    '''
    Delete a password.
    Required Parameters: password_id
    '''
    if not check_deps(d42.params, ['password_id']):
        d42.err('Required options were not found: password_id', 125)
        return False

    if not d42.opts.misc_yes:
        if not confirm('Are you sure you want to delete the given password?'):
            d42.err('Terminated at user request', 129)
            return False

    ret = d42.api('/passwords/{}/'.format(d42.params['password_id']), post=d42.params, delete=True)

    if not ret['result']:
        d42.err('API Error', 126, ret['data'])
        return False

    d42.out(ret['data'])
    return True


##
# MODULE FUNCTIONS
##
