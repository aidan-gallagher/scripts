#!/usr/bin/env python3

import subprocess
from fabric import Connection
from invoke import Responder

# IP address of the VM 
IP_ADDR="192.168.252.239"
BUILDDIR="/tmp/buildDir"  # Can't use a tilde in path name (https://github.com/fabric/fabric/issues/323)

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
     c.put(f'{BUILDDIR}/vyatta-policy-qos-groupings-v1-yang_6.1.0_all.deb', '/home/vyatta/debs/vyatta-policy-qos-groupings-v1-yang_6.1.0_all.deb')
     c.put(f'{BUILDDIR}/vplane-config-qos_6.1.0_all.deb', '/home/vyatta/debs/vplane-config-qos_6.1.0_all.deb')
     c.put(f'{BUILDDIR}/vyatta-policy-qos-vci_6.1.0_amd64.deb', '/home/vyatta/debs/vyatta-policy-qos-vci_6.1.0_amd64.deb')

     # Install the deb packages
     c.sudo('dpkg -i /home/vyatta/debs/vyatta-policy-qos-groupings-v1-yang_6.1.0_all.deb', watchers=[sudopass])
     c.sudo('dpkg -i /home/vyatta/debs/vplane-config-qos_6.1.0_all.deb', watchers=[sudopass])
     c.sudo('dpkg -i /home/vyatta/debs/vyatta-policy-qos-vci_6.1.0_amd64.deb', watchers=[sudopass])

     # Restart the VM
     c.sudo('reboot', watchers=[sudopass])