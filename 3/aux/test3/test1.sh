#!/usr/bin/env bash

# format should be:
# ./test.sh path/to/3 test_number
# or
# ./test.sh path/to/3

./$1 > /dev/null &

# wait for server to start
sleep 1

if [[ $2 -eq 0 ]];
then
	for filename in ./sample-inputs/*.txt;
	do
		echo "test case ${filename##*/}"
		nc localhost 8000 < sample-inputs/${filename##*/} | diff - expected-output/${filename##*/}
	done
else
	nc localhost 8000 < sample-inputs/$2.txt | diff - expected-output/$2.txt
fi

kill %1
