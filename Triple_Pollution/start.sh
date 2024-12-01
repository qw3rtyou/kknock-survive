#!/bin/bash
while true; do
    echo "Restarting app container..."
    docker-compose stop app && docker-compose start app
    sleep 1200 # 20분
done
