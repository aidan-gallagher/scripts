#!/usr/bin/env python3

import subprocess
from fabric import Connection
from invoke import Responder
import glob
from os.path import basename
import os
import argparse

# Get IP address of remote machine from the user
parser = argparse.ArgumentParser()
parser.add_argument('IP address', help='IP address of remote machine')
args = vars(parser.parse_args())
ip_addr = args['IP address']

# Can't use a tilde in path name so store debs in /tmp rather than $HOME (https://github.com/fabric/fabric/issues/323)
project = basename(os.getcwd())
builddir = "/tmp/buildDir/" + project

# Used to enter root password on remote system when prompted to
sudopass = Responder(
    pattern=r'\[sudo\] password:',
    response='vyatta\n',
)

# Build the deb packages and deposit them to ~/buildDir
subprocess.run([f"osc-buildpkg -D {builddir}"], shell=True)

# Connect to the remote machine
with Connection(ip_addr, user='vyatta', connect_kwargs={'password': 'vyatta'}) as c:

    # Make folder on remote to deposit packages
    c.run('mkdir -p /home/vyatta/debs/')

    # Copy the deb packages over to the VM
    # Can't specify directory using fabric https://github.com/fabric/fabric/issues/1998
    debs = glob.glob(f'{builddir}/*.deb')
    for deb in debs:
        c.put(deb, '/home/vyatta/debs')

    # Install the deb packages
    c.sudo('dpkg -i /home/vyatta/debs/*.deb', watchers=[sudopass])

    # Restart the VM
    c.sudo('reboot', watchers=[sudopass])
