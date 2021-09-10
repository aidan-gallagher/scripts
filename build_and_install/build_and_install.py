#!/usr/bin/env python3

import subprocess
from fabric import Connection
from invoke import Responder
import glob
from os.path import basename
import os
import argparse

# ======================================
# Configuration Variables
username = "vyatta"
password = "vyatta"
builddir_prefix = "/var/tmp/buildDir/"
build_command = "dpkg-buildpackage"
ip_addr = None
# ======================================


if not ip_addr:
    # Get IP address of remote machine from the user
    parser = argparse.ArgumentParser()
    parser.add_argument('IP address', help='IP address of remote machine')
    args = vars(parser.parse_args())
    ip_addr = args['IP address']

# Set location to store deb files
# Can't use a tilde in path name so store debs in /tmp rather than $HOME (https://github.com/fabric/fabric/issues/323)
project = basename(os.getcwd())
builddir = builddir_prefix + project

# Used to enter root password on remote system when prompted to
sudopass = Responder(
    pattern=r'\[sudo\] password:',
    response=password + "\n",
)

# Build debian packages
subprocess.run([build_command], shell=True)

# Connect to the remote machine
with Connection(ip_addr, user=username, connect_kwargs={'password': password}) as c:

    # Make destination folder
    c.run(f'mkdir -p {builddir}')

    # Copy debs to destination
    # Can't specify directory using fabric (https://github.com/fabric/fabric/issues/1998) so copy each one individually
    debs = glob.glob(f'../*.deb')
    for deb in debs:
        c.put(deb, builddir)

    # Install debs
    c.sudo(f'dpkg -i {builddir}/*.deb', watchers=[sudopass])

    # Restart the remote machine
    c.sudo('reboot', watchers=[sudopass])
