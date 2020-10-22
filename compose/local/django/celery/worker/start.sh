#!/bin/bash

celery -A yufuquant.taskapp worker -l INFO
