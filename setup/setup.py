import sys
import subprocess
import os
import platform
import apt
import json

system = None
root_dir = None

sources = {
    'apt': 'apt-get -y install {name}'
}


def download(url):
    subprocess.check_output([get_wget(), '--no-check-certificate', url],
                            stderr=subprocess.STDOUT)
    return os.path.basename(url)


def install(name, instruction):
    print "Installing " + name + " ..."
    try:
        if 'url' in instruction.keys():
            filepath = download(instruction['url'])
        if 'source' in instruction.keys():
            install_via(name, instruction['source'])
        if 'command' in instruction.keys():
            cmd = instruction['command'].format(path=filepath)
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print "Installing {name} failed while executing following command:".format(name=name)
        print ""
        print "$ " + str(e.cmd)
        print e.output
        print ""
        print "Please delete download folder and try again."
    except OSError as e:
        print "Execute command failed:"
        print ""
        print e.filename
        print e.args
        print e.message


def install_via(name, source):
    global sources
    if 'before_install' in source.keys():
        for action in source['before_install']:
            subprocess.check_call(action, stderr=subprocess.STDOUT, shell=True)
    if source['name'] == 'apt':
        cmd = sources[source['name']].format(name=name)

    subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)


def get_wget():
    global system
    if system == 'windows':
        return os.path.join(root_dir, 'bin', 'wget.exe')
    return 'wget'


def is_whitespace_or_none(s):
    return s is None or len(s.strip()) == 0


def check_run(type, cmd):
    if (type == 'apt'):
        apt_install(cmd)


def apt_install(pkg):
    print "apt-get install " + pkg


def start(path, download_dir, packages):
    global system
    global root_dir
    system = platform.system().lower()
    root_dir = path

    os.chdir(download_dir)
    for p in packages:
        if ('disabled' in p.keys() and p['disabled'] == True):
            continue
        if (system in p['installation']):
            instruction = p['installation'][system]
        elif ('default' in p['installation']):
            instruction = p['installation']['default']

        install(p['name'], instruction)
