# -*- coding: utf-8 -*-
import yaml
import os

from fabric.api import run, env, cd


class DeployToolKit(object):

    """
    Класс реализует методы для управления проектом удаленном сервере:
    создание и удаление директорий, установка зависимостей, публикация новых
    изменений и откат к старым релизам.
    """


    def create_dir(self):
        """Создание папки проекта"""

        run("mkdir -p {path}".format(path=env.project_root))

    def delete_dir(self):
        """Удаление папки проекта со всем содержимым"""

        run("rm -rf {path}".format(path=env.project_root))

    def pip_install_requirements(self, requirements=None):
        """Установка библиотек через pip"""

        req_command = "install -r {requirements}"
        if not requirements:
            self.pip(req_command.format(requirements=env.requirements))
        else:
            self.pip(req_command.format(requirements=requirements))

    def control_service(self, action="restart", service=None):
        """Метод для изменения состояния какого-либо сервиса"""

        if not service:
            service = env.linked_service
            if not service:
                return
        run("sudo service {server_name} {action}".format(server_name=service,
                                                         action=action))

    def run(self, action):
        """Метод для выполнения какой-либо программы внутри корневого каталога
        с проектом"""

        with cd(env.project_root):
            run(action)

    def do(self, f):
    # Запуск стронней функции

        with cd(env.project_root):
            f()

    def pip(self, action):
        """Метод для выполнения команды "от лица" pip из вируального
        окружения"""

        with cd(env.project_root):
            run("{pip} {action}".format(pip=env.pip, action=action))

    def python(self, action):
        """Метод для выполнения команды "от лица" python из вируального
        окружения"""

        with cd(env.project_root):
            run("{python} {action}".format(python=env.python, action=action))

    def init(self):
        """Подготовка окружения на удаленном компьютере к работе"""

        with cd(env.project_root):
            run("git init")
            run("git remote add origin {repository}".format(
                repository=env.repository))
            run("sudo apt-get -y install python-virtualenv")
            # Previous command installs package python-virtualenv only on
            # Debian based systems (Debian, Ubuntu, etc.)
            run("virtualenv {venv}".format(venv=env.venv))
        self.deploy()

    def change_repository(self):
        """Метод для изменения пути до репозитория"""

        with cd(env.project_root):
            run("git remote set-url origin {repository}".format(
                repository=env.repository))

    def deploy(self):
        """Метод для обновления проекта"""

        with cd(env.project_root):
            run("git checkout -B {branch}".format(branch=env.branch))
            run("git pull --rebase origin {branch}".format(branch=env.branch))

    def rollback(self, hash=None):
        """Метод для отката с определенному коммиту"""

        if not hash:
            self.rollback_on_commit()
        else:
            with cd(env.project_root):
                run("git reset --hard {hash}".format(hash=hash))

    def rollback_on_commit(self):
        """Метод для отката последнего изменения (по коммиту)"""

        with cd(env.project_root):
            run("git reset --hard HEAD^")

    def venv_update(self):
        """Метод для полного обновления виртуального окружения
        Подразумевается, что в проекте присутствует файл requirements.txt
        Имя файла можно поменять в настройках"""

        with cd(env.project_root):
            run("rm -rf {venv}".format(venv=evn.venv))
            run("virtualenv {venv}".format(venv=evn.venv))

    def run_migrate_command(self):
        """Метод для запуска команды проводящей миграции в БД"""
        if env.migrate_command:
            run(env.migrate_command)
