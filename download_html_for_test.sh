#! /bin/bash

export BASE_URL=https://www.boatrace.jp/owpc/pc/race/
export MOCK_HTML_DIREC=tests/mock_html

while read line
do
    curl $BASE_URL/$(sed -e "s/\./?/g" <<< $(basename ${line%.*})) -o $MOCK_HTML_DIREC/$(basename $line) -sS
    sleep 3
done < $MOCK_HTML_DIREC/.gitignore