#!/usr/bin/env python3
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
hvmpath = os.path.join(scriptdir, 'helm-version-manager.py')


def createSymlink(targetPath):
    if os.path.exists(targetPath):
        os.remove(targetPath)

    os.symlink(hvmpath, targetPath)


createSymlink('/usr/local/bin/helm-version-manager')
createSymlink('/usr/local/bin/hvm')

print('Installed symlink')
