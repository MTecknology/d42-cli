#!/usr/bin/env python
'''
This is the main D42 library, providing the D42() class.
It loads all the bits needed to talk to the D42 web application.

DEFINED EXIT :: 11
'''
import json
import requests
import os

from util import stderr, strip_unicode
from output import D42Output

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


class D42(object):
    '''Master object for holding D42 stuff (including API).'''
    api_user = None
    api_pass = None
    api_url = None
    api_ver = None
    opts = None
    params = None
    mods_list = None        # List of modules that should be loaded
    modules_loaded = []     # Modules that have been loaded
    outputter = D42Output()
    err_list = []


    def __init__(self):
        '''Class initialization'''
        self.opts = dict()
        self.params = dict()
        self.prepare_attributes()
        self.load_modules()


    def prepare_attributes(self):
        '''Initialize anything that hasn't been set'''
        if not self.api_url:
            self.api_url = 'https://d42.suitabletech.com/api/'
        if not self.api_ver:
            self.api_ver = '1.0'
        if self.mods_list is None:
            self.mods_list = ['mods.{}'.format(i[:-3]) for i in os.listdir('mods')
                    if i.endswith('.py') and i != '__init__.py']


    def update_attributes(self):
        '''Updates object attributes from passed options'''
        opts = self.opts
        if hasattr(opts, 'd42_url'):
            if opts.d42_url is not None:
                self.api_url = opts.d42_url
        if hasattr(opts, 'd42_user'):
            if opts.d42_user is not None:
                self.api_user = opts.d42_user
        if hasattr(opts, 'd42_pass'):
            if opts.d42_pass is not None:
                self.api_pass = opts.d42_pass

        if hasattr(opts, 'd42_params'):
            if opts.d42_params is not None:
                try:
                    self.params = json.loads(opts.d42_params)
                except:
                    stderr('Unable to parse parameters; is it valid serialized json?',
                           exit_status=11)
        if hasattr(opts, 'd42_prm'):
            if opts.d42_prm is not None:
                for param in opts.d42_prm:
                    opt = param.split('=')
                    self.params[opt[0]] = opt[1]

        if hasattr(opts, 'output'):
            if opts.output is not None:
                if opts.output not in self.outputter.outputs:
                    # This /should/ be impossible to get to, but handling it anyway
                    stderr('Selected output format is not available.', exit_status=11)
                self.outputter.set_format(opts.output)

        if self.api_url and not self.api_url.endswith('/'):
            self.api_url = self.api_url + '/'


    def load_modules(self):
        '''Attempts to load all modules in mods_list'''
        com = None
        if not self.mods_list:
            stderr('No modules loaded', 'NOTICE')
            return None

        for nam in self.mods_list:
            try:
                mod = __import__(nam)
                components = nam.split('.')
                for com in components[1:]:
                    mod = getattr(mod, com)
                setattr(self, com, mod)
                self.modules_loaded.append(com)
            except:
                stderr('Unable to load module {}'.format(nam), 'NOTICE')


    def api(self, query, post=None, delete=False):
        '''Performs an API query and returns the results'''
        if not query:
            return {'result': False,
                    'data': 'No API query provided.'}
        if self.api_user is None or self.api_pass is None:
            return {'result': False,
                    'data': 'No API credentials provided.'}

        url = '{}{}{}'.format(self.api_url, self.api_ver, query)
        auth = (self.api_user, self.api_pass)

        try:
            verify = not self.opts.misc_insecure
            if delete and post:
                req = requests.delete(url, auth=auth, data=post, verify=verify)
            elif delete:
                req = requests.delete(url, auth=auth, verify=verify)
            elif post:
                req = requests.post(url, auth=auth, data=post, verify=verify)
            else:
                req = requests.get(url, auth=auth, verify=verify)
            code = req.status_code
        except requests.exceptions.SSLError:
            return {'result': False,
                    'data': 'SSL error when connecting to server.'}
        except:
            return {'result': False,
                    'data': 'Unable to connect to server.'}

        # Return API response
        if req.ok:
            return {'result': True,
                    'data': strip_unicode(req.json()),
                    'code': code}

        # Process error code (non-digit)
        reason = getattr(req, 'reason', '')
        if isinstance(reason, str):
            err = {'error_message': 'Error accessing API ({})'.format(reason)}
        else:
            err = {'error_message': 'Error accessing API (Invalid Error)'}

        # Process server response
        message = getattr(req, 'text', '')
        if len(message) != 0:
            err['server_response'] = strip_unicode(req.json())

        # Return error to caller
        return {'result': False,
                'data': err}


    def out(self, data, fmt=None):
        '''Print output in a pretty way.'''
        self.outputter.render(data, fmt)


    def err(self, message, exit_status, blob=None):
        '''Wraps up data into an error dictionary and outputs result.
        Errors handled by this method do not terminate processing.
        The error produced is sent to stdout for processing by caller.
        Any call to err() will append an exit status to the running session.'''
        self.err_list.append(exit_status)
        self.out({'error': message, 'exit_status': exit_status, 'blob': blob})
