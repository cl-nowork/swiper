#!/bin/bash

echo 'server restart...'

BASE_DIR='/opt/swiper/'
PID=`cat $BASE_DIR/logs/gunicorn.pid`
kill -HUP $PID

echo 'done'
