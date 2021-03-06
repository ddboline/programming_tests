#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Utility functions """
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from subprocess import call, Popen, PIPE

HOSTNAME = os.uname()[1]
HOMEDIR = os.getenv('HOME')


class PopenWrapperClass(object):
    """ wrapper around subprocess.Popen """
    def __init__(self, command):
        """ init """
        self.command = command
        self.pop_ = Popen(self.command, shell=True, stdout=PIPE,
                          close_fds=True)

    def __enter__(self):
        """ enter """
        return self.pop_

    def __exit__(self, exc_type, exc_value, traceback):
        """ exit """
        if hasattr(self.pop_, '__exit__'):
            return self.pop_.__exit__(exc_type, exc_value, traceback)
        self.pop_.wait()
        if exc_type or exc_value or traceback:
            return False
        else:
            return True


def run_command(command, do_popen=False, turn_on_commands=True,
                single_line=False):
    """ wrapper around os.system """
    if not turn_on_commands:
        print(command)
        return command
    elif do_popen:
        if single_line:
            with PopenWrapperClass(command) as pop_:
                return pop_.stdout.read()
        else:
            return PopenWrapperClass(command)
    else:
        return call(command, shell=True)


def cleanup_path(orig_path):
    """ cleanup path string using escape character """
    chars_to_escape = ' ()"[]&,!;$' + "'"
    for ch_ in chars_to_escape:
        orig_path = orig_path.replace(ch_, r'\%c' % ch_)
    return orig_path


def walk_wrapper(direc, callback, arg):
    """ wrapper around os.walk for py2/py3 compatibility """
    if hasattr(os.path, 'walk'):
        os.path.walk(direc, callback, arg)
    elif hasattr(os, 'walk'):
        for dirpath, dirnames, filenames in os.walk(direc):
            callback(arg, dirpath, dirnames + filenames)


def get_md5_old(fname):
    """ python only md5 function """
    import hashlib
    m = hashlib.md5()
    with open(fname, 'rb') as infile:
        for line in infile:
            m.update(line)
    return m.hexdigest()


def get_md5(fname):
    """ system md5 function """
    try:
        with run_command('md5sum "%s" 2> /dev/null' % cleanup_path(fname),
                         do_popen=True) as pop_:
            output = pop_.stdout.read().split()[0]
        return output.decode()
    except IndexError:
        return get_md5_old(fname)


class OpenPostgreSQLsshTunnel(object):
    """ Class to let us open an ssh tunnel, then close it when done """
    def __init__(self, port=5432):
        self.tunnel_process = 0
        self.postgre_port = 5432
        self.remote_port = port

    def __enter__(self):
        if HOSTNAME != 'dilepton-tower':
            import time
            import shlex
            self.postgre_port = self.remote_port
            _cmd = 'ssh -N -L localhost:%d' % self.remote_port + \
                   ':localhost:5432 ddboline@home.ddboline.net'
            args = shlex.split(_cmd)
            self.tunnel_process = Popen(args, shell=False)
            time.sleep(5)
        return self.postgre_port

    def __exit__(self, exc_type, exc_value, traceback):
        if self.tunnel_process:
            self.tunnel_process.kill()
        if exc_type or exc_value or traceback:
            return False
        else:
            return True


def test_run_command():
    cmd = 'echo "HELLO"'
    out = run_command(cmd, do_popen=True, single_line=True).strip()
    assert out == b'HELLO'


def test_cleanup_path():
    INSTR = '/home/ddboline/THIS TEST PATH (OR SOMETHING LIKE IT) ' \
            '[OR OTHER!] & ELSE $;,""'
    OUTSTR = r'/home/ddboline/THIS\ TEST\ PATH\ \(OR\ SOMETHING\ LIKE\ ' \
             r'IT\)\ \[OR\ OTHER\!\]\ \&\ ELSE\ \$\;\,\"\"'
    assert cleanup_path(INSTR) == OUTSTR
