#!/usr/bin/env bash

# format should be:
# ./test.sh path/to/3 test_number
# or
# ./test.sh path/to/2

./$1 > /dev/null &
pid=$!
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

sleep 6
kill $pid
