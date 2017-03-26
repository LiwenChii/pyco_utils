#!/usr/bin/env python
import os

# python2
# import ConfigParser
from configparser import ConfigParser
from manager import Manager
from functools import partial
from subprocess import check_call as _call

call = partial(_call, shell=True)

manage = Manager()

base_path = os.path.dirname(os.path.abspath(__file__))
BASE_DOCKER_FILE = 'Dockerfile'
BASE_DOCKER_CELERY = 'Dockerfile_celery'
BASE_DOCKER_GUNICORN = 'Dockerfile_gunicorn'
BASE_DOCKER_SUPERVISORD = 'Dockerfile_supervisord'
filter_exts = ['min.min.css', 'min.min.js', '.pyc', '.log']


@manage.command
def clean(path=base_path, filter_exts=filter_exts):
    subs = os.listdir(path)
    for sub in subs:
        sub_path = os.path.join(path, sub)
        if os.path.isfile(sub_path):
            for ext in filter_exts:
                if sub.endswith(ext):
                    os.remove(sub_path)
                    print('remove file', sub_path)
        else:
            clean(sub_path, filter_exts)


@manage.command
def build_docker(dockerfile='', suffix=''):
    '''
    :param part: ['major', 'minor', 'patch']
    :return: git tag amd docker build/tag/push
    '''
    if dockerfile:
        call("copy %s Dockerfile" % dockerfile)
    # config = ConfigParser.ConfigParser() py2
    config = ConfigParser()
    config.read(".bumpversion.cfg")
    version = config.get('bumpversion', 'current_version')

    docker_host = config.get('docker', 'host')
    docker_name = config.get('docker', 'name')
    latest_tag = config.get('docker', 'latest_tag')
    build_log = config.get('docker', 'build_log')
    image = "%s/%s:%s%s" % (docker_host, docker_name, version, suffix)
    latest_image = "%s/%s:%s" % (docker_host, docker_name, latest_tag)

    call("docker build -t {image} .".format(image=image))
    call("docker tag {image} {latest_image}".format(image=image, latest_image=latest_image))
    call("docker push {image}".format(image=image))
    call("docker push {latest_image}".format(latest_image=latest_image))
    with open(build_log, 'a+') as f:
        f.write(image + '\n')
    return image


@manage.command
def help():
    call("bumpversion -h")
    print('\ndefault: [{major}.{minor}.{patch}]\n')


@manage.command
def bump(part='patch'):
    assert part in ['major', 'minor', 'patch']
    call("bumpversion %s" % part)


if __name__ == "__main__":
    manage.main()
