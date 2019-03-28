#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
JS_DIR="${DIR}/../spendtrackapp/static/spendtrackapp/js"
CSS_DIR="${DIR}/../spendtrackapp/static/spendtrackapp/css"

echo "Start compressing JS files"
cd "${JS_DIR}"
rm *.min.js
for file in `ls ${JS_DIR}`; do
    echo "    Compressing ${file}"
    uglifyjs ${file} > ${file%.*}.min.js
done

echo "Start compressing CSS files"
cd ${CSS_DIR}
rm *.min.css
for file in `ls ${CSS_DIR}`; do
    echo "    Compressing ${file}"
    uglifycss ${file} > ${file%.*}.min.css
done

echo "Done"
echo
