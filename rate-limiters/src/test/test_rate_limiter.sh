#!/bin/bash

for i in {1..20}
do
    curl -i http://127.0.0.1:5000/api/resource
    sleep 0.1
done
