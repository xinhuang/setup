import sys
import subprocess
import os

package_file = sys.argv[1]
download_dir = sys.argv[2]

def download(url):
    print "bin/wget.exe --no-check-certificate -P download/ {url}".format(url=url)
    subprocess.call(['bin/wget.exe', '--no-check-certificate', '-P', 'download/', url])
    return 'download/' + os.path.basename(url)

def install(cmd):
    subprocess.call(cmd)

packages = [line.strip() for line in open(package_file, 'r')]

for p in packages:
    if p.startswith('#'):
        continue
    name, url, cmd = p.split(',')
    print "name: {0}, url: {1}, cmd: {2}".format(name, url, cmd)
    localpath = "{0}/{1}"
    filepath = download(url)
    install(cmd.format(path=filepath))
