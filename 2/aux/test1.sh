#!/usr/bin/env bash

# format should be:
# ./test.sh path/to/2 test_number
# or
# ./test.sh path/to/2
if [[ $2 -eq 0 ]];
then
	for filename in ./sample-inputs/*.txt;
	do
		$1 < sample-inputs/${filename##*/} | diff - expected-output/${filename##*/}
	done
else
	$1 < sample-inputs/$2.txt | diff - expected-output/$2.txt
fi
