#!/usr/bin/env python2
import os
import yaml
import json
import shlex
import urllib2
import datetime
import subprocess
from fabric.api import *

#Importing the config YAML file
with open('config.yml') as fc:
    const = yaml.load(fc)

env.hosts = const.get('hosts')
env.user   = const.get('user')
env.branch = const.get('branch')
env.password = const.get('password')
tomcat_user = const.get('tomcat_user')
HIPCHAT_WEB_HOOK = const.get('hipchat')
REVIEWER = const.get('reviewer')
DEV_NAME = const.get('dev_name')
FOLDER = const.get('folder')
LOG_FOLDER = const.get('log_folder')

#Working on log
def log(file=None):
    with cd(LOG_FOLDER):
        if file == None:
            sudo('ls' , user='tomcat')
        else:
            sudo('tail -f %s' , user='tomcat')

def log():
    with cd(FOLDER):
        result = run('git log --oneline -4')
        return result

def checkout(branch="lf-dev"):
    """checkout
            Switch the branch
    :param branch:
    """
    with cd(FOLDER):
        sudo('git fetch', user='tomcat')
        sudo('git checkout %s' % branch, user='tomcat')
        status()

def status():
    """status"""
    with cd(FOLDER):
        sudo('git status', user='tomcat')


def deploy(branch=None):
    """deploy

    :param branch:
    """
    if branch:
        checkout(branch)
    else:
        branch=env.branch

    with cd(FOLDER):
        sudo('git pull origin', user='tomcat')
        with cd('frontend/ingestion'):
            sudo('npm install', user='tomcat')
            sudo('npm run build:dev', user='tomcat')
        status()
        result = log()
    sudo('apachectl graceful')
    hipchat('Deployed to outdev ', branch)

def hipchat(message="Test Hipchat!!", branch=env.branch):
    """hipchat
            Hipchat Notification
    :param message:
    :param branch:
    """
    message = message +  "(yey) @ (%s, %s) by %s " % (branch, datetime.datetime.now().strftime("%y-%m-%d-%H-%M"), env.user)
    data = {
            "color":"green",
            "message":message,
            "notify":True,
            "message_format":"text"
            }
    req = urllib2.Request(HIPCHAT_WEB_HOOK)
    req.add_header("Content-Type", "application/json")
    urllib2.urlopen(req, json.dumps(data))

def sendpr(m='This is PR', b='lf-dev', h=None):
    """sendpr
            Send the PR to base branch
    :param m:
    :param b:
    :param h:
    """
    command = 'hub pull-request -m  "%s" -b %s' % (m,b)

    current_branch_cmd = shlex.split('git rev-parse --abbrev-ref HEAD')
    process = subprocess.Popen(current_branch_cmd, stdout=subprocess.PIPE)
    current_branch, err = process.communicate()
    print('current_branch', current_branch)
    if not h:
        cmd = shlex.split(command)
    else:
        command =  command + '-h %s' % (h)
        cmd = shlex.split(command)
        current_branch = h

    cmd = shlex.split(command)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, err = process.communicate()
    message = m +  " PR from %s @ %s reviewers @%s @%s \n URL: %s \n  %s >>> %s" % (DEV_NAME,
                                                                       datetime.datetime.now().strftime("%y-%m-%d-%H-%M"),
                                                                      REVIEWER[0], REVIEWER[1], output , b,
                                                                                    current_branch)
    data = {
            "color":"green",
            "message":message,
            "notify":True,
            "message_format":"text"
            }
    req = urllib2.Request(HIPCHAT_WEB_HOOK)
    req.add_header("Content-Type", "application/json")
    urllib2.urlopen(req, json.dumps(data))


