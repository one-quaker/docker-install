import os
import sys
import argparse
import platform


'''
docker+docker-compose install script for ubuntu linux.
Install docker in one command:
sh -c "$(wget https://raw.githubusercontent.com/one-quaker/python_start/master/install_docker.sh -O -)"
'''

if platform.python_version()[0] == '2':
    print('python3 {0}'.format(*sys.argv))
    sys.exit(1)


parser = argparse.ArgumentParser(description='Docker install script')
parser.add_argument('--force', '-f', action='store_true', default=False)


ARG = parser.parse_args()


def user_input():
    while True:
        answer = input('\nContinue? (y/n) ')
        if answer.lower() in ('y', 'yes'):
            return True
        elif answer.lower() in ('n', 'no'):
            sys.exit(1)


def install_docker():
    DOCKER_COMPOSE_VERSION = '1.24.1' # https://github.com/docker/compose/releases
    UBUNTU_VERSION = os.popen('lsb_release -cs').read().strip()
    USER = os.popen('whoami').read().strip()
    OS = os.popen('uname -s').read().strip()
    CPU_ARCH = os.popen('uname -m').read().strip()

    if UBUNTU_VERSION == 'tessa': # hello linux mint
        UBUNTU_VERSION = 'xenial'

    cmd_list = (
        'sudo apt update -y',
        r'sudo apt purge -y docker\*',
        'sudo apt install -y apt-transport-https ca-certificates make wget curl software-properties-common',
        'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
        'echo \"deb [arch=amd64] https://download.docker.com/linux/ubuntu {} stable\" | sudo tee /etc/apt/sources.list.d/docker.list'.format(UBUNTU_VERSION),
        'sudo apt update -y',
        'sudo apt install -y docker-ce',
        'sudo usermod -aG docker {}'.format(USER),
        'curl -L https://github.com/docker/compose/releases/download/{}/docker-compose-{}-{} -o /tmp/docker-compose'.format(DOCKER_COMPOSE_VERSION, OS, CPU_ARCH),
        'sudo mv -v /tmp/docker-compose /usr/local/bin/docker-compose',
        'chmod +x /usr/local/bin/docker-compose',
    )

    print('\n'.join(cmd_list))
    if not ARG.force: user_input()

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
