#!/usr/bin/env bash

# format should be:
# ./test.sh path/to/2 test_number
# or
# ./test.sh path/to/2
if [ $2 -eq 0]
then
	COUNTER=ls -1 ./sample-inputs | wc -l
	for i in COUNTER;
	do
		$1 < sample-inputs/$i.txt | diff - expected-output/$i.txt
	done
else
	$1 < sample-inputs/$2.txt | diff - expected-output/$2.txt
fi
