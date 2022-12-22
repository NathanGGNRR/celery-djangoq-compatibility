#!/bin/bash
winpty docker exec -it celery_back celery -A poccelery worker -l INFO -n worker1 --concurrency=$1
