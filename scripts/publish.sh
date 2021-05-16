#!/bin/bash

LOCAL_DIR='./'
REMOTE_DIR='/opt/swiper/'

USER='root'
HOST='35.201.227.163'

rsync -crvP --delete --exclude={.venv,.git,__pycache__,logs} $LOCAL_DIR $USER@$HOST:$REMOTE_DIR

ssh $USER@$HOST "$REMOTE_DIR/scripts/restart.sh"
