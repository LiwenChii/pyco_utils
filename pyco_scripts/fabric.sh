#!/usr/bin/env bash

echo "\n"
echo "***************************************************\n"
echo "   Fabric Control AB TEST with Several Machine     "
echo "                      START\n"
echo $(date '+%Y-%m-%d %H:%M:%s')
echo " 1.go to the target file"
pwd
cd {fabfile.path}
pwd
# fab -H {host1},{host2},{host3} -u {user} -p {password} {fabfile.command_func}

