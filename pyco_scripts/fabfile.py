# coding: utf-8
# /Users/nico/PycharmProjects/dodoru/ab_test/Fabric_AB_Test.py
# ab_test nico$ fab -H sai-dev-010.cloudapp.net,sai-dev-011.cloudapp.net,sai-dev-012.cloudapp.net,sai-dev-013.cloudapp.net,sai-dev-014.cloudapp.net -u azureuser -p malong#1dev check_env


from fabric.api import run
from fabric.api import settings


def host_type():
    run("uname -s")
    # sudo("/etc/init.d/apache2 restart", pty=False)


def exists(path):
    with settings(warn_only=True):
        return run('test -e %s' % path)


def deploy():
    run("cd /path/to/application && ./update.sh")


def run_su(command, user="otheruser"):
    return run('su %s -c "%s"' % (user, command))
    # sudo("command",user="otheruser")
    # su otheruser -c [command]


def remote_bash():
    from fabric.api import env
    env.shell = "/bin/sh -c"
    # /bin/bash -l -c "<command string here>"


def git_push():
    run("git push")


def git_pull():
    run("git pull")


def git_clone():
    # run("mkdir src")
    run("ls")
    run("cd src && pwd")
    # run("pwd")
    # run("git clone https://malong.visualstudio.com/DefaultCollection/StyleAI/_git/ml-tool-operations ")
    # return run("pwd")
    # return run("sh ../script_tests/unit_test.sh")


def deploy_env():
    run("sudo apt-get install python-pip")
    run("sudo apt-get install git")


def run_ABtest():
    pass

def check_env():
    run("which git")
    run("which pip")


def send_email():
    return run("mail -s 'AB_TEST_RESULTS' niconing@malongtech.cn")


