#!/bin/sh

DIR="wgbot"

if ! basename $PWD | grep -q "$DIR" ; then
    echo "Invalid folder, you have to be in the repository folder to start the script"
    exit 1
fi

cd ..
if ! scrapy startproject $DIR | grep -q 'New Scrapy project'; then
   echo "Unable to create the scrapy project"
   exit 1
fi

cd $DIR
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
mv wg_spider.py $DIR/spiders/wg_spider.py
