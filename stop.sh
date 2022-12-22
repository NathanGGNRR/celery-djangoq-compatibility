#!/bin/bash

winpty docker stop celery-celery-1
winpty docker exec -it celery_back pkill -f "worker1"
