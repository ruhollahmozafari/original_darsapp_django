#!/bin/bash

while IFS== read -r key value; 
do
     if [ "$key" == "SQL_HOST" ]; then
        value='127.0.0.1'
     fi
    printf -v "$key" %s "$value" && export "$key";
done<$1
# python manage.py runserver 0.0.0.0:8080
