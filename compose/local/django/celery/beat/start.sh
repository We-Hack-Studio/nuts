#!/bin/bash

rm -f './celerybeat.pid'
celery -A yufuquant.taskapp beat -l INFO
