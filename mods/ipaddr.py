#!/usr/bin/env python
'''
Module to perform operations on D42 ips.

DEFINED EXIT :: 115, 116, 119
'''
from lib.util import check_deps, encode, confirm, stderr


##
# MODULE HOOKS
##

def modhook_options(opts):
    ''' MODULE HOOK :: OPTIONS '''
    # Group: operations
    opts.opt(
        'operations', '-si', '--search-ips',
        action='store_const', const='ipaddr.op_search_ips', dest='operation',
        help='List all ips; use --params to refine search')

    opts.opt(
        'operations', '-ci', '--create-ip',
        action='store_const', const='ipaddr.op_create_ip', dest='operation',
        help='Create a ip in D42; <ipaddress>')

    opts.opt(
        'operations', '-ui', '--update-ip',
        action='store_const', const='ipaddr.op_update_ip', dest='operation',
        help='Update details of a ip; <ipaddress>')

    opts.opt(
        'operations', '-gi', '--get-ip',
        action='store_const', const='ipaddr.op_get_ip', dest='operation',
        help='Get a single ip; <ip_id>')

    opts.opt(
        'operations', '-di', '--delete-ip',
        action='store_const', const='ipaddr.op_delete_ip', dest='operation',
        help='Delete a ip; <ip_id>')

    opts.opt(
        'operations', '-ri', '--request-ip',
        action='store_const', const='ipaddr.op_request_ip', dest='operation',
        help='Reserve/suggest IP address in given subnet, subnet_id; <reserve_ip>')


##
# HOOK FUNCTIONS
##

def op_create_ip(d42):
    '''
    Create a new ip in D42.
    Required Parameters: number
    Optional Parameters: http://api.device42.com/#update-ips
    '''
    if not check_deps(d42.params, ['ipaddress']):
        d42.err('Required options were not found: ipaddress', 115)

    if _ip_exists(d42, {'ip': d42.params['ipaddress']}):
        d42.err('An existing ip matched this create request', 115)

    ret = d42.api('/ips/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 116, ret['data'])
    d42.out(ret)


def op_update_ip(d42):
    '''
    Update an existing ip in D42.
    Required Parameters: id
    Optional Parameters: http://api.device42.com/#update-ips
    '''
    if not check_deps(d42.params, ['ipaddress']):
        d42.err('Required options were not found: ipaddress', 115)
        return False

    if not _ip_exists(d42, {'ip': d42.params['ipaddress']}):
        d42.err('No existing ip was found for this update request', 115)
        return False

    ret = d42.api('/ips/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 116, ret['data'])
        return False

    d42.out(ret)
    return True


def op_get_ip(d42):
    '''
    Get a single ip.
    Required Parameters: ip_id
    '''
    if not check_deps(d42.params, ['ip_id']):
        d42.err('Required options were not found: ip_id', 115)
        return False

    ret = d42.api('/ips/{}/'.format(d42.params['ip_id']))

    if not ret['result']:
        d42.err('API Error', 116, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_search_ips(d42):
    '''
    Search for ips within D42.
    With no parameters specified, all results are returned.
    '''
    qs = '?{}'.format(encode(d42.params)) if d42.params is not None else ''
    ret = d42.api('/ips/{}'.format(qs))

    if not ret['result']:
        d42.err('API Error', 116, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_request_ip(d42):
    '''
    Reserve or suggest an IP address in a given subnet.
    Required Parameters: subnet_id|subnet|name
    Non-optional Parameters: reserve_ip=(yes|No)
    '''
    if not (check_deps(d42.params, ['subnet_id']) or
            check_deps(d42.params, ['subnet']) or
            check_deps(d42.params, ['name'])):
        d42.err('Need one of: subnet_id, subnet, name', 115)
        return False

    if not check_deps(d42.params, ['reserve_ip']):
        stderr('Parameter reserve_ip was missing; default does not reserve', 'WARNING')

    ret = d42.api('/suggest_ip/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 116, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_delete_ip(d42):
    '''
    Delete a ip.
    Required Parameters: ip_id
    '''
    if not check_deps(d42.params, ['ip_id']):
        d42.err('Required options were not found: ip_id', 115)
        return False

    if not d42.opts.misc_yes:
        if not confirm('Are you sure you want to delete the given ip?'):
            d42.err('Terminated at user request', 119)
            return False

    ret = d42.api('/ips/{}/'.format(d42.params['ip_id']), post=d42.params, delete=True)

    if not ret['result']:
        d42.err('API Error', 116, ret['data'])
        return False

    d42.out(ret['data'])
    return True


##
# MODULE FUNCTIONS
##

def _ip_exists(d42, params):
    '''
    Checks whether a ip with the given name exists.
    Returns: Boolean
    '''
    qs = '?{}'.format(encode(params))
    ret = d42.api('/ips/{}'.format(qs))
    if not ret['result']:
        d42.err('Failed to check if ip currently exists.', 115)
    if not 'ips' in ret['data']:
        d42.err('Failed to check if ip currently exists.', 115)
    if len(ret['data']['ips']) == 0:
        return False
    return True
