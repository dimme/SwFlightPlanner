#!/bin/bash
nice python fplan/extract/extracted_cache.py force $1 $2
for (( ; ; ))
do
   nice python fplan/extract/extracted_cache.py $1 $2
   sleep 7200
done



