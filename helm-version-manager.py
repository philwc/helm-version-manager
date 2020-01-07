#!/usr/bin/env python3

import argparse
import requests
import tarfile
import io
import os
import shutil
import sys

scriptdir = os.path.dirname(os.path.realpath(__file__))
helmdir = os.path.join(scriptdir, 'helm-versions')


def exists(version):
    path = os.path.join(helmdir, version)

    return os.path.isdir(path)


def get(version):
    if exists(version):
        print(
            '''Helm version already exists. Either switch to it, or delete:

        - `helm-version-manager switch {version}`
        - `helm-version-manager delete {version}`'''.format(version=version)
        )
        return

    type = 'linux-amd64'
    file = 'helm-%s-%s.tar.gz' % (version, type)
    url = 'https://get.helm.sh/' + file

    print('Downloading '+url)
    r = requests.get(url)

    if r.status_code == 200:
        file = io.BytesIO(r.content)
        tar = tarfile.open(fileobj=file, mode="r:gz")
        tar.extractall(path=helmdir)
        tar.close()

        typepath = os.path.join(helmdir, type)
        versionpath = os.path.join(helmdir, version)

        os.rename(typepath, versionpath)
        print(
            'Complete. Switch now using `{script} switch {version}`'.format(script=os.path.basename(sys.argv[0]), version=version))
    else:
        print('Could not find version {version} to download'.format(version=version))


def switch(version):
    if not exists(version):
        print('Version {version} doesn\'t exist. Try `get`ting first?'.format(
            version=version))

    path = os.path.join(helmdir, version, 'helm')
    binpath = '/usr/local/bin/helm'

    if os.path.exists(binpath):
        os.remove(binpath)

    os.symlink(path, binpath)
    print('Switched helm version to '+version)


def delete(version):
    if exists(version):
        path = os.path.join(helmdir, version)
        shutil.rmtree(path)
        print('Deleted helm version '+version)
    else:
        print('Version {version} doesn\'t exist.'.format(version=version))



def sanitiseVersion(version):
    if not version.startswith('v'):
        return 'v' + version
    else:
        return version


parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['get', 'switch', 'delete'],
                    help='Choose an action')
parser.add_argument('version', nargs=1,
                    help='Specify a version to use')
args = parser.parse_args()

# Invoke the relevant function
globals()[args.action](
    sanitiseVersion(args.version[0])
)
