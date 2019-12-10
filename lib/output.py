#!/usr/bin/env python
'''
Provides the D42Output class.
It prints pretty things to stdout.

DEFINED EXIT :: 31, 32
'''
import time
import json
import pprint

from util import stderr


class D42Output(object):
    '''Object to handle outputting to various formats.'''
    outputs = None
    output_format = 'pprint' # default


    def __init__(self):
        '''Class initialization'''
        self.outputs = list()
        self.load_libraries()


    def load_libraries(self):
        '''Load and register libraries used for outputters.
        This allows outputters to be available despite one or two breaking
        or being otherwise unloadable.'''
        # Required Outputters ; libs already loaded
        # d42-cli will not run without json
        # pprint is the easiest to test/debug/skim and is the default
        outputs = ['json', 'pprint', 'devnull', 'raw']

        # Attempt to load additional outputters
        for lib in ['yaml']:
            try:
                library = __import__(lib)
                globals()[lib] = library
                outputs.append(lib)
            except:
                # No reason to stop loading, but drop something on stderr
                # This should only be reached if there is a bug in this file
                stderr('Unable to load library: {}'.format(lib), 'NOTICE')

        self.outputs = outputs


    def set_format(self, fmt):
        '''Set the selected output option.'''
        if not fmt in self.outputs:
            stderr('Unsupported output format specified; using defaults', 'WARNING')
        if not isinstance(fmt, str):
            stderr('Output format is not string; using defaults', 'WARNING')
        self.output_format = fmt


    def render(self, data, fmt=None):
        '''Render the reousted output using the requested format'''
        if not fmt:
            fmt = self.output_format

        if not isinstance(fmt, str):
            stderr('Output format was externally broked; forcing defaults', 'WARNING')
            fmt = 'pprint'

        if not hasattr(self, '_print_{}'.format(fmt)):
            # If a valid outputter was requested but is unavailable, it should
            # be assumed something is expecting output in that format. Rather
            # than revert to a default to get data out, we should die here.
            stderr('Requested outputter unavailable', exit_status=31)

        try:
            rndr = getattr(self, '_print_{}'.format(fmt))
            rndr(data)
        except:
            # Same as above; an error here should result in death.
            stderr('Unable to render data with requested outputter.', exit_status=31)


    ##
    # Print functions for outputters.
    #   All strings in self.outputs are expected to have a matching _print_FOO() function.
    ##


    def _print_json(self, data):
        '''Render the output using json.'''
        print(json.dumps(data))


    def _print_yaml(self, data):
        '''Render the output using yaml.'''
        print(yaml.dump(data, default_flow_style=False))


    def _print_pprint(self, data):
        '''Render the output using pprint.'''
        pprint.pprint(data)


    def _print_raw(self, data):
        '''Render the unformatted output'''
        print(data)


    def _print_devnull(self, data):
        '''Render nothing'''
        pass

    def _print_secret(self, data):
        '''Render plain output and then clear the screen'''
        try:
            import curses
        except:
            stderr('Unable to load curses library for outputter.', exit_status=32)

        if not isinstance(data, str):
            stderr('Data passed to renderer was invalid.', exit_status=32)
        if '\n' in data:
            stderr('This renderer does not support newlines.', exit_status=32)

        try:
            # Initialize Curses
            stdscr = curses.initscr()
            curses.cbreak()
            curses.noecho()
            stdscr.keypad(1)

            # Render display
            stdscr.addstr(1, 2, "Secret:")
            stdscr.addstr(3, 5, data)
            stdscr.refresh()
            i = 7
            while True:
                stdscr.addstr(5, 1, 'Timeout: %s' % str(i))
                stdscr.refresh()
                time.sleep(1)
                i -= 1
                if i <= 0:
                    break
        except:
            stderr('Unable to render terminal.')
        finally:
            curses.nocbreak()
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
