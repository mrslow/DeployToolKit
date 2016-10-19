# coding: utf-8

import os
import yaml

from fabric.api import env, puts
from fabric.colors import red


class Configuration(object):

    def __init__(self, stage, path):
        self.stage = stage
        self.path = path

    def set_env(self):
        self._set_env()

    def _read_config(self):
        if not os.path.exists(self.path):
            puts(red("Path {} does not exists.".format(self.path)))
            os.sys.exit()
        with open(self.path) as f:
            return yaml.load(f.read())

    def _set_env(self):
        settings = self._read_config()
        env.stage = self.stage
        env.hosts = _get_hosts(settings)
        env.passwords = _get_passwords(settings)
        env.project_root = settings.get("project_root", "")

        venv = settings.get('venv_folder', 'venv')
        env.venv = os.path.join(env.project_root, venv)
        env.python = os.path.join(env.venv, 'bin/python')
        env.pip = os.path.join(env.venv, 'bin/pip')

        env.branch = settings.get('branch', 'master')
        env.requirements = settings.get('venv_requirements',
                'requirements.txt')
        env.linked_service = settings.get('linked_service')
        env.repository = settings.get('repository')
        env.migrate_command = settings.get('migrate_command')

def _get_hosts(config_file):
    return config_file.get("servers", {}).keys()

def _get_passwords(config_file):
    passwords = {}
    for server, password in config_file.get("servers", {}).items():
        if password:
            passwords.update({server: password})
    return passwords
