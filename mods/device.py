#!/usr/bin/env python
'''
Module to perform operations on D42 devices.

DEFINED EXIT :: 110, 111
'''
from lib.util import check_deps, encode


##
# MODULE HOOKS
##

def modhook_options(opts):
    ''' MODULE HOOK :: OPTIONS '''
    # Group: operations
    opts.opt('operations', '-sd', '--search-devices',
             action='store_const', const='device.op_search_devices', dest='operation',
             help='List all devices; use --params to refine search')

    opts.opt('operations', '-cd', '--create-device',
             action='store_const', const='device.op_create_device', dest='operation',
             help='Create a device in D42; <name>')

    opts.opt('operations', '-ud', '--update-device',
             action='store_const', const='device.op_update_device', dest='operation',
             help='Update details of a device; <name>')

    opts.opt('operations', '-gd', '--get-device',
             action='store_const', const='device.op_get_device', dest='operation',
             help='Get a single device; <device_id|device_name>')

    #opts.opt('operations', '--delete-device',
    #         action='store_const', const='device.op_delete_device', dest='operation',
    #         help='Delete a device matching XYZ')

    # Group: devices
    #opts.opt('devices', '--device-name',
    #         action='store', dest='devices_name', metavar='dev',
    #         help='Device Name')


##
# HOOK FUNCTIONS
##

def op_create_device(d42):
    '''
    Create a new device in D42.
    Required Parameters: name (name)
    Optional Parameters: http://api.device42.com/#create-update-device-by-name
    '''
    if not check_deps(d42.params, ['name']):
        d42.err('The field name is a required.', 110)
        return False

    if _device_exists(d42, d42.params['name']):
        d42.err('A device with this name already exists.', 110)
        return False

    ret = d42.api('/device/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 111, ret['data'])
        return False

    d42.out(ret)
    return True


def op_update_device(d42):
    '''
    Update an existing device in D42.
    Required Parameters: name (name)
    Optional Parameters: http://api.device42.com/#create-update-device-by-name
    '''
    if not check_deps(d42.params, ['name']):
        d42.err('The field name is a required.', 110)
        return False

    if not _device_exists(d42, d42.params['name']):
        d42.err('No device with this name currently exists.', 110)
        return False

    ret = d42.api('/device/', post=d42.params)

    if not ret['result']:
        d42.err('API Error', 111, ret['data'])
        return False

    d42.out(ret)
    return True


def op_get_device(d42):
    '''
    Get a single device.
    Required Parameters: device_id
    Examples:
      ./d42-cli --get-device -p device_id=449
      ./d42-cli --get-device -p device_name=zm1.st1
      ./d42-cli --get-device --params device_id=449
    '''
    if check_deps(d42.params, ['device_id']) and check_deps(d42.params, ['device_name']):
        d42.err('A device requires either device_id or device_name be specified. Not both.', 110)
        return False
    elif check_deps(d42.params, ['device_id']):
        ret = d42.api('/devices/id/{}/'.format(d42.params['device_id']))
    elif check_deps(d42.params, ['device_name']):
        ret = d42.api('/devices/name/{}/'.format(d42.params['device_name']))
    else:
        d42.err('Required options were not found', 110)
        return False

    if not ret['result']:
        d42.err('API Error', 111, ret['data'])
        return False

    d42.out(ret['data'])
    return True


def op_search_devices(d42):
    '''
    Search for devices within D42.
    With no parameters specified, all results are returned.
    Examples:
      ./d42-cli --search-devices -p type=virtual
      ./d42-cli --search-devices -p type=virtual -p building=st1
      ./d42-cli --search-devices
    '''
    qs = '?{}'.format(encode(d42.params)) if d42.params is not None else ''
    vs = 'all/' if d42.opts.misc_verbose else ''
    ret = d42.api('/devices/{}{}'.format(vs, qs))

    if not ret['result']:
        d42.err('API Error', 111, ret['data'])
        return False

    d42.out(ret['data'])
    return True


##
# MODULE FUNCTIONS
##

def _device_exists(d42, devname):
    '''
    Checks whether a device with the given name exists.
    Returns: Boolean
    '''
    ret = d42.api('/devices/name/{}/'.format(devname))
    if not ret['result']:
        return False
    return True
