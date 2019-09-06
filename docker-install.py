import os
import sys
import argparse
import platform
import time


'''
docker+docker-compose install script for ubuntu linux
'''

if platform.python_version()[0] == '2':
    print('python3 {0}'.format(*sys.argv))
    sys.exit(1)


parser = argparse.ArgumentParser(description='Docker install script')
parser.add_argument('--curl', action='store_true', default=False)
parser.add_argument('--install', '-i', type=str, choices=['all', 'compose'], default='all')
parser.add_argument('--user', '-u', type=str, default='docker-user')
parser.add_argument('--user-uid', '-U', type=int, default=5000)
parser.add_argument('--delay', '-d', type=int, default=10)
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--compose-version', '-c', type=str, default='1.24.1')


ARG = parser.parse_args()


if ARG.verbose:
    print('User: {user}\nUser UID and GUID: {user_uid}\ndocker-compose version: {compose_version}'.format(**ARG.__dict__))


if ARG.curl:
    print('curl https://raw.githubusercontent.com/one-quaker/docker-install/master/docker-install.py | python3 -')
    sys.exit(0)
elif os.getegid() != 0:
    print('run as root user')
    sys.exit(0)


def install_docker():
    USER = ARG.user
    OS = os.popen('uname -s').read().strip()
    CPU_ARCH = os.popen('uname -m').read().strip()

    DOCKER_COMPOSE_VERSION = ARG.compose_version
    DOCKER_COMPOSE_URL = 'https://github.com/docker/compose/releases/download/{}/docker-compose-{}-{}'.format(DOCKER_COMPOSE_VERSION, OS, CPU_ARCH)
    UBUNTU_VERSION = os.popen('lsb_release -cs').read().strip()

    if UBUNTU_VERSION == 'tessa': # hello linux mint
        UBUNTU_VERSION = 'xenial'

    cmd_list = ()
    docker_list = (
        'sudo apt update -y',
        r'sudo apt purge -y docker\*',
        'sudo apt install -y apt-transport-https ca-certificates make wget curl software-properties-common',
        'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
        'echo \"deb [arch=amd64] https://download.docker.com/linux/ubuntu {} stable\" | sudo tee /etc/apt/sources.list.d/docker.list'.format(UBUNTU_VERSION),
        'sudo apt update -y',
        'sudo apt install -y docker-ce',
        'sudo useradd -m -s /bin/bash -u {uid} -U {user}'.format(uid=ARG.user_uid, user=USER),
        'sudo usermod -aG docker {}'.format(USER),
    )
    compose_list = (
        'curl -L {} -o /tmp/docker-compose'.format(DOCKER_COMPOSE_URL),
        'sudo mv -v /tmp/docker-compose /usr/local/bin/docker-compose',
        'chmod +x /usr/local/bin/docker-compose',
    )
    if ARG.install == 'compose':
        cmd_list += compose_list
    else:
        cmd_list += docker_list + compose_list

    print('\n'.join(cmd_list))

    print('\nDocker compose version "{}"'.format(DOCKER_COMPOSE_VERSION))
    print('Full list of docker-compose versions you can find here -> https://github.com/docker/compose/releases\n')
    print('Install will start in {} seconds...'.format(ARG.delay))
    time.sleep(ARG.delay)

    for cmd in cmd_list:
        out = os.popen(cmd).read()
        print(out)


msg_tpl = 'Download and install: \"{}\"'
if 'linux' in sys.platform:
    install_docker()
    print('Done! Please reboot your system!')
    print('sudo reboot')
elif sys.platform == 'darwin':
    print(msg_tpl.format('https://download.docker.com/mac/stable/Docker.dmg'))
else:
    print(msg_tpl.format('https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe'))
