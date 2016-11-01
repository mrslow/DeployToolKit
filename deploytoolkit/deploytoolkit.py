# -*- coding: utf-8 -*-
import yaml
import os

from fabric.api import run, env, cd


class DeployToolKit(object):

    # Создание папки с виртуальным окружением
    def create_dir(self):
        run('mkdir -p {path}'.format(path=env.project_root))

    def delete_dir(self):
        run('rm -rf {path}'.format(path=env.project_root))

    # Установка требуемых для нормальной работы плагинов
    def pip_install_requirements(self, requirements=None):
        req_command = 'install -r {requirements}'
        if not requirements:
            self.pip(req_command.format(requirements=env.requirements))
        else:
            self.pip(req_command.format(requirements=requirements))

    # Метод для изменения состояния какого-либо сервиса
    def control_service(self, action='restart', service=None):
        if not service:
            service = env.linked_service
            if not service:
                return
        run('sudo service {server_name} {action}'.format(server_name=service,
                                                         action=action))

    # Метод для выполнения какой-либо программы внутри корневого каталога с
    # проектом
    def run(self, action):
        with cd(env.project_root):
            run(action)

    # Запуск стронней функции
    def do(self, f):
        with cd(env.project_root):
            f()

    # Методы для выполнения команды "от лица" pip из вируального окружения
    def pip(self, action):
        with cd(env.project_root):
            run('{pip} {action}'.format(pip=env.pip, action=action))

    # Метода для выполнения команды "от лица" python из вируального окружения
    def python(self, action):
        with cd(env.project_root):
            run('{python} {action}'.format(python=env.python, action=action))

    # Подготовка окружения на удаленном компьютере к работе
    def init(self):
        with cd(env.project_root):
            run('git init')
            run('git remote add origin {repository}'.format(
                repository=env.repository))
            run('sudo apt-get -y install python-virtualenv')
            # Previous command installs package python-virtualenv only on
            # Debian based systems (Debian, Ubuntu, etc.)
            run('virtualenv {venv}'.format(venv=env.venv))
        self.deploy()

    # Метод для изменения пути до репозитория
    def change_repository(self):
        with cd(env.project_root):
            run('git remote set-url origin {repository}'.format(
                repository=env.repository))

    # Метод для обновления проекта
    def deploy(self):
        with cd(env.project_root):
            run('git pull origin {branch}'.format(branch=env.branch))

    # Метод для отката с определенному коммиту
    def rollback(self, hash=None):
        if not hash:
            self.rollback_on_commit()
        else:
            with cd(env.project_root):
                run('git reset --hard {hash}'.format(hash=hash))

    # Метод для отката последнего изменения (по коммиту)
    def rollback_on_commit(self):
        with cd(env.project_root):
            run('git reset --hard HEAD^')

    # Метод для полного обновления виртуального окружения
    # Подразумевается, что в проекте присутствует файл requirements.txt
    # Имя файла можно поменять в настройках
    def venv_update(self):
        with cd(env.project_root):
            run('rm -rf {venv}'.format(venv=evn.venv))
            run('virtualenv {venv}'.format(venv=evn.venv))

    def run_migrate_command(self):
        if env.migrate_command:
            run(env.migrate_command)
