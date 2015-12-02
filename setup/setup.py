import sys
import subprocess
import os
import platform
import json

root_dir = None
system = platform.system().lower()



def apt_add_repo(r):
    global services
    print 'add-apt-repository', r
    subprocess.check_call(['add-apt-repository', '-y', r], stderr=subprocess.STDOUT)


def apt_install(name):
    global services
    print services['apt'], 'install', name
    subprocess.check_call(services['apt'] + ' -y install ' + name,
                          stderr=subprocess.STDOUT, shell=True)


def apt_update():
    global services
    subprocess.check_call(services['apt'] + ' update', stderr=subprocess.STDOUT, shell=True)


def install_apt(apt, **kwargs):
    if 'repositories' in apt.keys():
        for r in apt['repositories']:
            apt_add_repo(r)
        apt_update()
    apt_install(kwargs['name'])


def custom_command(cmd, **kwargs):
    global services
    cmd = services['command'] + cmd.format(path=kwargs['path'])
    print '$ ', cmd
    subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)


def download(url):
    global services
    print get_wget(), url
    subprocess.check_call(get_wget() + ' ' + url,
                          stderr=subprocess.STDOUT, shell=True)
    return os.path.basename(url)

proxies = {
    'apt': install_apt,
    'url': download,
    'command': custom_command,
}

services = {
    'apt': 'apt-get',
    'url': 'wget --no-check-certificate',
    'command': '',
}


def get_wget():
    global system
    if system == 'windows':
        return os.path.join(root_dir, 'bin', 'wget.exe') + ' --no-check-certificate'
    return 'wget --no-check-certificate'

def install_services(services):
    global services
    for k in services.keys():
        services[k] = services[k]

def install(name, instruction):
    print "\n>>>>>>>>>>>>>>>>> Installing " + name + " <<<<<<<<<<<<<<<<<<"
    try:
        download_path = ''
        if 'url' in instruction.keys():
            download_path = proxies['url'](instruction['url'])
        for i in instruction:
            if i == 'url' or i == 'post-install':
                continue
            if i not in proxies.keys():
                print "Error: Don't know how to install " + name
            proxies[i](instruction[i], name=name, path=download_path)

        post_install = instruction['post-install']
        if post_install is not None:
            if 'services' in post_install:
                install_services(post_install['services'])
    except subprocess.CalledProcessError as e:
        print "Error: Installing {name} failed while executing following command.".format(name=name)
        print ""
        print "$ " + str(e.cmd)
        print e.output
        print ""
        print "Please delete download folder and try again."
    except OSError as e:
        print "Error: Execute command failed."
        print ""
        print e.filename
        print e.args
        print e.message


def install_via(name, source):
    global sources
    s = source.keys[0]
    if 'before_install' in source.keys():
        for action in source['before_install']:
            subprocess.check_call(action, stderr=subprocess.STDOUT, shell=True)
    if source['name'] == 'apt':
        cmd = sources[source['name']].format(name=name)

    subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)


def is_whitespace_or_none(s):
    return s is None or len(s.strip()) == 0


def check_run(type, cmd):
    if (type == 'apt'):
        apt_install(cmd)

def sort_packages(packages):
    return packages

def start(path, download_dir, packages):
    global system
    global root_dir
    root_dir = path

    os.chdir(download_dir)
    for p in packages:
        name = p['name']
        if ('disabled' in p.keys() and p['disabled'] == True):
            continue
        instruction = None
        if (system in p['installation']):
            instruction = p['installation'][system]
        elif ('default' in p['installation']):
            instruction = p['installation']['default']

        if instruction != None:
            install(name, instruction)
        else:
            print 'Skipped installing', name, 'for', system
