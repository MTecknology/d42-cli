#!/usr/bin/env python
'''
Module to perform operations on D42 subnets.

DEFINED EXIT :: 130, 131, 134
'''
from lib.util import check_deps, encode, confirm


##
# MODULE HOOKS
##

def modhook_options(opts):
    ''' MODULE HOOK :: OPTIONS '''
    # Group: operations
    opts.opt(
        'operations', '-ss', '--search-subnets',
        action='store_const', const='subnet.op_search_subnets', dest='operation',
        help='List all subnets; use --params to refine search')

    opts.opt(
        'operations', '-cs', '--create-subnet',
        action='store_const', const='subnet.op_create_subnet', dest='operation',
        help='Create a subnet in D42; <network, mask_bits>')

    opts.opt(
        'operations', '-us', '--update-subnet',
        action='store_const', const='subnet.op_update_subnet', dest='operation',
        help='Update details of a subnet; <network, mask_bits>')

    opts.opt(
        'operations', '-gs', '--get-subnet',
        action='store_const', const='subnet.op_get_subnet', dest='operation',
        help='Get a single subnet; <subnet_id>')

    opts.opt(
        'operations', '-ds', '--delete-subnet',
        action='store_const', const='subnet.op_delete_subnet', dest='operation',
        help='Delete a subnet; <subnet_id>')


##
# HOOK FUNCTIONS
##

def op_create_subnet(d42):
    '''
    Create a new subnet in D42.
    Required Parameters: network, mask_bits, name
    Optional Parameters: http://api.device42.com/#create-update-subnets
    '''
    if not check_deps(d42.params, ['network', 'mask_bits', 'name']):
        d42.err('Required options were not found: network, mask_bits, name', 130)

    if _subnet_exists(d42, d42.params):
        d42.err('An existing subnet matched this create request', 130)

    ret = d42.api('/subnets/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 131, ret['data'])
    d42.out(ret)


def op_update_subnet(d42):
    '''
    Update an existing subnet in D42.
    Required Parameters: network, mask_bits, name
    Optional Parameters: http://api.device42.com/#create-update-subnets
    '''
    if not check_deps(d42.params, ['network', 'mask_bits']):
        d42.err('Required options were not found: network, mask_bits', 130)
        return False

    if not _subnet_exists(d42, d42.params):
        d42.err('No existing subnet was found for this update request', 130)
        return False

    ret = d42.api('/subnets/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 131, ret['data'])
        return False

    d42.out(ret)
    return True


def op_get_subnet(d42):
    '''
    Get a single subnet.
    Required Parameters: subnet_id
    '''
    if not check_deps(d42.params, ['subnet_id']):
        d42.err('Required options were not found: subnet_id', 130)
        return False

    ret = d42.api('/subnets/{}/'.format(d42.params['subnet_id']))

    if not ret['result']:
        d42.err('API Error', 131, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_search_subnets(d42):
    '''
    Search for subnets within D42.
    With no parameters specified, all results are returned.
    '''
    qs = '?{}'.format(encode(d42.params)) if d42.params is not None else ''
    ret = d42.api('/subnets/{}'.format(qs))

    if not ret['result']:
        d42.err('API Error', 131, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_delete_subnet(d42):
    '''
    Delete a subnet.
    Required Parameters: subnet_id
    '''
    if not check_deps(d42.params, ['subnet_id']):
        d42.err('Required options were not found: subnet_id', 130)
        return False

    if not d42.opts.misc_yes:
        if not confirm('Are you sure you want to delete the given subnet?'):
            d42.err('Terminated at user request', 134)
            return False

    ret = d42.api('/subnets/{}/'.format(d42.params['subnet_id']), post=d42.params, delete=True)

    if not ret['result']:
        d42.err('API Error', 131, ret['data'])
        return False

    d42.out(ret['data'])
    return True


##
# MODULE FUNCTIONS
##

def _subnet_exists(d42, params):
    '''
    Checks whether a subnet with the given name exists.
    Returns: Boolean
    '''
    if not check_deps(params, ['network', 'mask_bits']):
        d42.err('Function requires network and mask_bits', 130)
    qs = '?{}'.format(encode({'network': params['network'], 'mask_bits': params['mask_bits']}))
    ret = d42.api('/subnets/{}'.format(qs))
    if not ret['result']:
        d42.err('Failed to check if subnet currently exists.', 130)
    if not 'subnets' in ret['data']:
        d42.err('Failed to check if subnet currently exists.', 130)
    if len(ret['data']['subnets']) == 0:
        return False
    return True
