#!/usr/bin/env python3

import subprocess
from fabric import Connection
from invoke import Responder
import glob

# IP address of the VM
IP_ADDR = "192.168.252.239"
# Can't use a tilde in path name (https://github.com/fabric/fabric/issues/323)
BUILDDIR = "/tmp/buildDir"

# Used to enter root password on remote system when prompted to
sudopass = Responder(
    pattern=r'\[sudo\] password:',
    response='vyatta\n',
)

# Build the deb packages and deposit them to ~/buildDir
subprocess.run([f"osc-buildpkg -D {BUILDDIR}"], shell=True)

# Connect to the remote VM
with Connection(IP_ADDR, user="vyatta", connect_kwargs={'password': 'vyatta'}) as c:

    # Make folder on remote to deposit packages
    c.run('mkdir -p /home/vyatta/debs/')

    # Copy the deb packages over to the VM
    # Can't specify directory using fabric https://github.com/fabric/fabric/issues/1998
    debs = glob.glob(f'{BUILDDIR}/*.deb')
    for deb in debs:
        c.put(deb, '/home/vyatta/debs')

    # Install the deb packages
    c.sudo('dpkg -i /home/vyatta/debs/*.deb', watchers=[sudopass])

    # Restart the VM
    c.sudo('reboot', watchers=[sudopass])