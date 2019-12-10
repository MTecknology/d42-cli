#!/usr/bin/env python
'''
Module to perform operations on D42 vlans.
'''
from lib.util import check_deps, encode, confirm


##
# MODULE HOOKS
##

def modhook_options(opts):
    ''' MODULE HOOK :: OPTIONS '''
    # Group: operations
    opts.opt(
        'operations', '-sv', '--search-vlans',
        action='store_const', const='vlan.op_search_vlans', dest='operation',
        help='List all vlans; use --params to refine search')

    opts.opt(
        'operations', '-cv', '--create-vlan',
        action='store_const', const='vlan.op_create_vlan', dest='operation',
        help='Create a vlan in D42; <number>')

    opts.opt(
        'operations', '-uv', '--update-vlan',
        action='store_const', const='vlan.op_update_vlan', dest='operation',
        help='Update details of a vlan; <id>')

    opts.opt(
        'operations', '-gv', '--get-vlan',
        action='store_const', const='vlan.op_get_vlan', dest='operation',
        help='Get a single vlan; requires <vlan_id>')

    opts.opt(
        'operations', '-dv', '--delete-vlan',
        action='store_const', const='vlan.op_delete_vlan', dest='operation',
        help='Delete a vlan; requires <vlan_id>')


##
# HOOK FUNCTIONS
##

def op_create_vlan(d42):
    '''
    Create a new vlan in D42.
    Required Parameters: number
    Optional Parameters: http://api.device42.com/#update-vlans
    '''
    if not check_deps(d42.params, ['number']):
        d42.err('Required options were not found: number', 135)
        return False

    if _vlan_exists(d42, {'number': d42.params['number']}):
        d42.err('An existing vlan matched this create request', 135)
        return False

    ret = d42.api('/vlans/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 136, ret['data'])
        return False

    d42.out(ret)
    return True


def op_update_vlan(d42):
    '''
    Update an existing vlan in D42.
    Required Parameters: number
    Optional Parameters: http://api.device42.com/#update-vlans
    '''
    if not check_deps(d42.params, ['id']):
        d42.err('Required options were not found: id', 135)
        return False

    if not _vlan_exists(d42, {'vlan_id': d42.params['id']}):
        d42.err('No existing vlan was found for this update request', 135)
        return False

    params = dict(d42.params)
    del params['id']
    ret = d42.api('/vlans/{}/'.format(d42.params['id']), post=params)

    if not ret['result']:
        d42.err('API Error', 136, ret['data'])
        return False

    d42.out(ret)
    return True


def op_get_vlan(d42):
    '''
    Get a single vlan.
    Required Parameters: vlan_id
    '''
    if not check_deps(d42.params, ['vlan_id']):
        d42.err('Required options were not found: vlan_id', 135)
        return False

    ret = d42.api('/vlans/{}/'.format(d42.params['vlan_id']))

    if not ret['result']:
        d42.err('API Error', 136, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_search_vlans(d42):
    '''
    Search for vlans within D42.
    With no parameters specified, all results are returned.
    '''
    qs = '?{}'.format(encode(d42.params)) if d42.params is not None else ''
    ret = d42.api('/vlans/{}'.format(qs))

    if not ret['result']:
        d42.err('API Error', 136, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_delete_vlan(d42):
    '''
    Delete a vlan.
    Required Parameters: vlan_id
    '''
    if not check_deps(d42.params, ['vlan_id']):
        d42.err('Required options were not found: vlan_id', 135)
        return False

    if not d42.opts.misc_yes:
        if not confirm('Are you sure you want to delete the given vlan?'):
            d42.err('Terminated at user request', 139)
            return False

    ret = d42.api('/vlans/{}/'.format(d42.params['vlan_id']), post=d42.params, delete=True)

    if not ret['result']:
        d42.err('API Error', 136, ret['data'])
        return False

    d42.out(ret['data'])
    return True


##
# MODULE FUNCTIONS
##

def _vlan_exists(d42, params):
    '''
    Checks whether a vlan with the given name exists.
    Returns: Boolean
    '''
    if not check_deps(params, ['number']) and not check_deps(params, ['vlan_id']):
        d42.err('Function requires number or id', 135)
    qs = '?{}'.format(encode(params))
    ret = d42.api('/vlans/{}'.format(qs))
    if not ret['result']:
        d42.err('Failed to check if vlan currently exists.', 135)
    if not 'vlans' in ret['data']:
        d42.err('Failed to check if vlan currently exists.', 135)
    if len(ret['data']['vlans']) == 0:
        return False
    return True
