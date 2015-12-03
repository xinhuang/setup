import sys
import subprocess
import os
import platform
import json

root_dir = None
system = platform.system().lower()

services = {
    'apt': {'install': 'apt-get -y install {name}', 'repo': 'add-apt-repository -y {value}'},
    'url': {'install': 'wget --no-check-certificate {value}'},
    'command': None,
}


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


def download(url):
    global services
    cmd = get_wget().format(value=url)
    print cmd

    filename = os.path.basename(url)
    if (not os.path.isfile(filename)):
        subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    return filename


def get_wget():
    global system
    if system == 'windows':
        return os.path.join(root_dir, 'bin', 'wget.exe') + ' --no-check-certificate {url}'
    return 'wget --no-check-certificate'


def install_services(new_serv):
    global services
    for k in new_serv.keys():
        print 'Installing service:', k, 'as', new_serv[k]
        services[k] = new_serv[k]


def start_service(service, **kwargs):
    print 'start_service>', service
    cmd = service.format(name=kwargs['name'], path=kwargs['path'])
    print '$', cmd
    subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)


def install(name, instruction):
    print "\n>>>>>>>>>>>>>>>>> Installing", name, "<<<<<<<<<<<<<<<<<"
    try:
        download_path = ''
        if 'url' in instruction.keys():
            download_path = download(instruction['url'])
        for i in instruction:
            if i == 'url' or i == 'post-install':
                continue
            if i not in services.keys():
                print "Error: Don't know how to install", name, 'via', i
                continue

            service = services[i]
            if service is None:
                cmd = instruction[i]
            else:
                cmd = service['install']
            start_service(cmd, name=name, path=download_path)

        if 'post-install' in instruction.keys():
            post_install = instruction['post-install']
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


def is_whitespace_or_none(s):
    return s is None or len(s.strip()) == 0


def check_run(type, cmd):
    if (type == 'apt'):
        apt_install(cmd)


def sort_packages(packages):
    sorted = []
    while len(packages) > 0:
        for p in packages:
            if len(p['dependencies']) == 0:
                sorted.append(p)
                name = p['name']
                for t in packages:
                    if name in t['dependencies']:
                        t['dependencies'].remove(name)
                packages.remove(p)
                break
    return sorted


def start(path, download_dir, packages):
    global system
    global root_dir
    root_dir = path
    for p in packages:
        if 'dependencies' not in p.keys():
            p['dependencies'] = []
    packages = sort_packages(packages)

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
            print '>>>>>>>>>>>>>>>>> Skipped installing', name, 'for', system, '<<<<<<<<<<<<<<<<<'
