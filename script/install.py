import sys
import subprocess
import os
import platform

root_dir = sys.argv[1]
package_file = os.path.join(root_dir, "etc", "packages.csv")
download_dir = os.path.join(root_dir, "download/")
bin_dir = os.path.join(root_dir, "bin/")

system = platform.system()

def download(url):
    print get_wget() + " --no-check-certificate -P {prefix} {url}".format(url=url, prefix=download_dir)
    subprocess.call([get_wget(), '--no-check-certificate', '-P', 'download/', url])
    return download_dir + os.path.basename(url)

def install(cmd):
    os.chdir(download_dir)
    subprocess.call(cmd)
    os.chdir(root_dir)

def get_wget():
    return os.path.join(bin_dir, "wget.exe")

def is_whitespace_or_none(s):
    return s is None or len(s.strip()) == 0

packages = [line.strip() for line in open(package_file, 'r')]

for p in packages:
    if p.startswith('#'):
        continue
    name, url, cmd = p.split(',')
    # print "name: {0}, url: {1}, cmd: {2}".format(name, url, cmd)
    localpath = "{0}/{1}"
    if (is_whitespace_or_none(url)):
        install(cmd)
    else:
        filepath = download(url)
        install(cmd.format(path=filepath))
