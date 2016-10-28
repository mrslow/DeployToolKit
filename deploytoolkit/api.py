#coding :utf-8

from fabric.api import env, task

from deploytoolkit import DeployToolKit
from configuration import Configuration


before_init = []
after_init = []
before_deploy = []
after_deploy = []
before_rollback = []
after_rollback = []


@task
def production(config_path="config/production.yaml"):
    """
    Set production environment.
    """

    config = Configuration("production", config_path)
    config.set_env()
    print env

@task
def stage(config_path="config/stage.yaml"):
    """
    Set stage environment.
    """

    config = Configuration("stage", config_path)
    config.set_env()
    print env

@task
def test(config_path="config/test.yaml"):
    """
    Set test environment.
    """

    config = Configuration("test", config_path)
    config.set_env()
    print env


@task
def init(service=None):
    """
    Initialize the project on remote server.
    """

    print "Initializing ..."
    tool = DeployToolKit()
    for host in env.hosts:
        tool._update_env(host)

        tool.create_dir()

        for f in before_init:
            tool.do(f)

        tool.run('sudo apt-get install git')
        tool.init()
        tool.pip_install_requirements()
        if service:
            tool.control_service(service=service, action='start')
        else:
            tool.control_service(action='start')
        tool.run_migrate_command()

        for f in after_init:
            tool.do(f)

@task
def deploy(service=None):
    """
    Deploy the project.
    """

    print "Deploing ..."

    tool= DeployToolKit()
    for host in env.hosts:
        tool._update_env(host)

        for f in before_deploy:
            tool.do(f)

        tool.deploy()
        tool.pip_install_requirements()
        if service:
            tool.control_service(service=service, action='restart')
        else:
            tool.control_service(action='restart')
        tool.run_migrate_command()

        for f in after_deploy:
            tool.do(f)

@task
def rollback(service=None, commit=None):
    """
    Rollback last commit.
    """

    print "Rollbacking ..."

    tool= DeployToolKit()
    for host in env.hosts:
        tool._update_env(host)

        for f in before_rollback:
            tool.do(f)

        tool.rollback(commit)
        tool.pip_install_requirements()

        if service:
            tool.control_service(service=service, action='restart')
        else:
            tool.control_service('restart')
        tool.run_migrate_command()

        for f in after_rollback:
            tool.do(f)

@task
def clear():
    """
    Delete a project from remote server.
    """

    print "Clearing ..."

    tool= DeployToolKit()
    for host in env.hosts:
        tool._update_env(host)
        tool.delete_dir()
