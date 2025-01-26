#!/bin/bash
#
export FLASK_ENV=development
export FLASK_APP=app
export FLASK_DEBUG=True
echo 'Running flaskrun.sh...'

flask run
sleep 1
#
#url="http://127.0.0.1/localhost"
