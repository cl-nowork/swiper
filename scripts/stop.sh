#!/bin/bash

BASE_DIR='/opt/swiper/'
PID=`cat $BASE_DIR/logs/gunicorn.pid`
kill $PID
