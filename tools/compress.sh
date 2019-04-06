#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
JS_DIR="${DIR}/../spendtrackapp/static/spendtrackapp/js"
CSS_DIR="${DIR}/../spendtrackapp/static/spendtrackapp/css"

if [[ `which uglifyjs` == '' ]]; then
    echo 'Cannot find uglifyjs executable'
    exit 1
elif [[ `which uglifycss` == '' ]]; then
    echo 'Cannot find uglifycss executable'
    exit 1
fi

success=0

echo "Start compressing JS files"
cd "${JS_DIR}"
rm *.min.js
for file in `ls ${JS_DIR}`; do
    echo "    Compressing ${file}"
    uglifyjs ${file} > ${file%.*}.min.js
    success=$((success + $?));
done

echo "Start compressing CSS files"
cd ${CSS_DIR}
rm *.min.css
for file in `ls ${CSS_DIR}`; do
    echo "    Compressing ${file}"
    uglifycss ${file} > ${file%.*}.min.css
    success=$((success + $?));
done

if [[ ${success} == 0 ]]; then
    echo -e "Compressed successfully!\n"
    exit 0
else
    echo -e "Some errors occurred\n" >&2
    exit 1
fi

