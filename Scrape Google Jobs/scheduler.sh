#!/bin/bash

for ((i = 0 ; i < 5 ; i++));
	do
		python Scrape.py;
		echo "Scrapping Completed"
	sleep 14400;
	done