#!/usr/bin/env bash

function tolog()
{
    ts=$(date +%Y%m%d-%H%M%S)
    echo "$ts $1" >> ./push.log  
}

tolog "Starting push"
#ssh root@192.168.1.103 '/root/bin/push'
tolog "Finished push"
sleep 10

