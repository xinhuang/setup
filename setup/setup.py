import sys
import subprocess
import os
import platform
import json

system = None
root_dir = None


def apt_add_repo(r):
    print 'add-apt-repository', r
    subprocess.check_call(['add-apt-repository', '-y', r], stderr=subprocess.STDOUT)


def apt_install(name):
    print 'apt-get install', name
    subprocess.check_call(['apt-get', '-y', 'install', name], stderr=subprocess.STDOUT)


def apt_update():
    subprocess.check_call(['apt-get', 'update'], stderr=subprocess.STDOUT)


def install_apt(apt, **kwargs):
    if 'repositories' in apt.keys():
        for r in apt['repositories']:
            apt_add_repo(r)
        apt_update()
    apt_install(kwargs['name'])


def custom_command(cmd, **kwargs):
    cmd = cmd.format(path=kwargs['path'])
    print '$ ', cmd
    subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)


def download(url):
    print 'wget --no-check-certificate ', url
    subprocess.check_call([get_wget(), '--no-check-certificate', url],
                          stderr=subprocess.STDOUT)
    return os.path.basename(url)

proxies = {
    'apt': install_apt,
    'url': download,
    'command': custom_command,
}


def install(name, instruction):
    print ">>>>>>>>>>>>>>>>> Installing " + name + " <<<<<<<<<<<<<<<<<<"
    try:
        download_path = ''
        if 'url' in instruction.keys():
            download_path = proxies['url'](instruction['url'])
        for i in instruction:
            if i == 'url':
                continue
            if i not in proxies.keys():
                print "Error: Don't know how to install " + name
            proxies[i](instruction[i], name=name, path=download_path)
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
