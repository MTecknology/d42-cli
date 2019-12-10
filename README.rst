D42 Command Line Utility
========================

This utility provides a command line interface for working with Device42. It is
meant to be a simple and flexible utility that is modular and easy to expand.

D42-cli was written in a way that should (hopefully) be easy to reference as a
framework for building other api-cli utilities.

Authentication
--------------

The default username and password will be read from the environment variables
if they are available.

D42_API_USER

D42_API_PASS

Example Usage
-------------

./d42-cli [-h] <optional arguments> [operation] <options>

Search for all devices where "manufacturer" is "Globalscale."::

    ./d42-cli --search-devices -p manufacturer=Globalscale

Search for all devices where the name contains the letters "lan"::

    ./d42-cli -sd -p name=lan

    ./d42-cli -sd -v -p name=lan

    ./d42-cli -sd --params '{"name": "lan"}' --verbose

Search for all physical systems::

    ./d42-cli --search-devices -p type=physical

Search for all physical systems where the name contains the letters "zr"::

    ./d42-cli --search-devices -p type=physical -p name=zr

Get details about a single device::

    ./d42-cli --get-device -p device_name=alarm1-pa1

Update the details of an existing device::

    ./d42-cli --update-device -p name=alarm1-pa1 -p osver=Windows

    ./d42-cli --update-device \
        --params '{"name": "alarm1-pa1", "osver": "Squeeze", "osverno": "6.0.10", "os": "Debian"}'

Working with VLANs::

    ./d42-cli -cv -p number=4004 -p name=ml_test

        {'code': 200,
         'data': {'code': 0,
         'msg': ['vlan successfully added', 54, 'ml_test', True, True]},
         'result': True}

    ./d42-cli -gv -p vlan_id=54

        {'description': '',
        'name': 'ml_test',
        'notes': '',
        'number': 4004,
        'switches': [],
        'vlan_id': 54}

    ./d42-cli -dv -p vlan_id=54

        Are you sure you want to delete the given vlan? [y/N]: y
        {'deleted': 'true', 'id': '54'}


Parameters
----------

The d42-cli utility provides a generic interface for passing parameters. These
parameters may be used for searching or updating fields.

In some cases, specific parameters are required. In these cases, the parameter's
help text will display the required parameters.

When multiple matching parameters are specified -p and --prm will take precedence
over --params, regardless of order specified. If the same option was provided twice
using --prm or -p, then the last read option will take precedence.

Development
-----------

Most development work on d42-cli will take place in mods/\*.py. The rest of the
application is intended to provide a modular and flexible framework for talking
to the D42 API.

Exit Status
~~~~~~~~~~~

Currently, all exit statuses are unique. This design was chosen for a number of
reasons that are no longer pertinent.

* d42-cli       ::   2 -   9 ; 0
* lib.d42       ::  10 -  19
* lib.opts      ::  20 -  29
* lib.output    ::  30 -  39
* lib.util      ::  40 -  49 ; 199
* mods.device   :: 100 - 114
* mods.ipaddr   :: 115 - 119
* mods.misc     :: 120 - 124
* mods.password :: 125 - 129
* mods.subnet   :: 130 - 134
* mods.vlan     :: 135 - 139

Note: Exit status 199 is reserved for lib.util's stderr() function.

For mods.X, I've been using:

* 1x0 & 1x5 => Bad Client Request (think HTTP 4xx)
* 1x1 & 1x6 => Request Error (think HTTP 5xx)
* 1x4 & 1x9 => User Canceled (confirmation dialog)
