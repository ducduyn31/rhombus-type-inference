#!/bin/bash

# Load environment variables
printenv | grep "APP_" > /etc/environment
echo "VIRTUAL_ENV=${VIRTUAL_ENV}" >> /etc/environment

# Set root password
mkdir -p /var/run/sshd
echo "root:password" | chpasswd
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/#PermitUserEnvironment no/PermitUserEnvironment yes/g' /etc/ssh/sshd_config
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Start SSH server
/usr/sbin/sshd -D &
echo "SSH server started"

exec "$@"
