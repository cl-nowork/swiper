#!/bin/bash

BASE_DIR='/opt/swiper/'

source $BASE_DIR/.venv/bin/activate
gunicorn -c $BASE_DIR/swiper/gunicorn-config.py swiper.wsgi
deactivate
