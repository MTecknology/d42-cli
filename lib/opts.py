#!/usr/bin/env python
'''
Provides the D42Opts class.

Environment Variables Read :: D42_URL, D42_USER, D42_PASS

DEFINED EXIT :: none
'''
import argparse
import os

from util import stderr

class D42Opts(object):
    '''Master object to handle extra options loaded modules may provide'''
    parser = None
    groups = None

    def __init__(self, outputs=None):
        '''Class initialization'''
        self.groups = dict()

        if not isinstance(outputs, list):
            stderr('Outputs passed to D42Opts.__init__ was not type list.', 'WARNING')
            outputs = []

        self.parser = argparse.ArgumentParser(
            usage='d42-cli [-h] <optional arguments> [operation] <options>',
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))
        self._add_base(outputs)


    def _add_base(self, outputs=None):
        '''Standard available options'''
        if outputs is None:
            outputs = list()
        self.parser.add_argument(
            '--d42-url',
            dest='d42_url',
            action='store',
            metavar=' http://...',
            help='Where to find the D42 application',
            default=os.environ.get('D42_API_URL'))
        self.parser.add_argument(
            '--d42-user',
            dest='d42_user',
            action='store',
            metavar='jdoe',
            help='D42 Username; reads env[D42_API_USER]',
            default=os.environ.get('D42_API_USER'))
        self.parser.add_argument(
            '--d42-pass',
            dest='d42_pass',
            action='store',
            metavar='secret',
            help='D42 Password; reads env[D42_API_PASS]',
            default=os.environ.get('D42_API_PASS'))

        # Optional Parameters
        self.parser.add_argument(
            '--params',
            dest='d42_params',
            action='store',
            metavar='\'{"foo": "bar"}\'',
            help='Parameters available to operation; json')
        self.parser.add_argument(
            '--prm', '-p',
            dest='d42_prm',
            action='append',
            metavar='k=v',
            help='Single k=v parameters; supersedes --params')

        # Output formats
        self.parser.add_argument(
            '--out',
            dest='output',
            choices=outputs,
            help='Formatter used to display output; def=pprint')

        # Version
        self.parser.add_argument(
            '--version',
            action='version',
            version='0.977')

        # Operations (made available by modules)
        arg_group = self.parser.add_argument_group(
            'operations',
            'Operations provided by loaded modules.')
        self.groups['operations'] = arg_group


    def _need_group(self, group):
        '''Allows modules to define a group that they want to provide options for.'''
        if not group in self.groups:
            arg_group = self.parser.add_argument_group(group, None)
            self.groups[group] = arg_group


    def opt(self, group, *args, **kwargs):
        '''Add an option from a module.
        Modules are only allowed to work with option groups'''
        self._need_group(group)
        self.groups[group].add_argument(*args, **kwargs)


    def load_module_options(self, d42):
        '''Attempts to run the "modhook_options" hook of modules'''
        if not hasattr(d42, 'modules_loaded'):
            return None

        for modname in getattr(d42, 'modules_loaded'):
            if not hasattr(d42, modname):
                continue
            mod = getattr(d42, modname)

            if not hasattr(mod, 'modhook_options'):
                continue
            mod.modhook_options(self)


    def parse_opts(self):
        '''Return parsed options'''
        return self.parser.parse_args()
