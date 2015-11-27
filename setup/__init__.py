import platform
import json
import os

import setup


def start(path):
    package_dir = os.path.join(path, 'etc')
    download_dir = os.path.join(path, 'download')

    files = [os.path.join(package_dir, f) for f in os.listdir(package_dir)
             if os.path.isfile(os.path.join(package_dir, f))]
    contents = [open(f).read().replace('\n', '') for f in files]
    packages = [json.loads(c) for c in contents]

    setup.start(path, download_dir, packages)
