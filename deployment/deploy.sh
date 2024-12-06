#!/bin/bash
PATH=/usr/local/sbin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin

cd /archive/scripts


./deploy-automation.sh

sleep 10s

./deploy-notfication.sh

exit
