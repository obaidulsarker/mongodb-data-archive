#!/bin/bash
LOGFILE=/archive/scripts/deploy.log

NAMESPACE_NAME=docker.xyz.com/devops

AUTOMATION_APP_REPO=mongodb-archive
AUTOMATION_APP_VERSION=latest


echo "$(date) : [$AUTOMATION_APP_REPO] deployment is Started." >> $LOGFILE;
sudo docker ps --filter status=exited -q | xargs docker rm
sudo docker pull $NAMESPACE_NAME/$AUTOMATION_APP_REPO:$AUTOMATION_APP_VERSION
sudo docker run -d -v /archive/logs:/app/logs -v /archive/cred:/app/cred -v /archive/data:/app/data -v /archive/config:/app/config $NAMESPACE_NAME/$AUTOMATION_APP_REPO:$AUTOMATION_APP_VERSION
echo "$(date) : [$AUTOMATION_APP_REPO] deployment is Completed." >> $LOGFILE;