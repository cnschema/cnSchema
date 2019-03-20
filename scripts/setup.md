
# maintain

local update。，。
1. goto settings.py, update version=...
  prev version cns_20190115
  current version cns_20190320
2. download schemaorg_translate.xlsx from google doc  
    https://docs.google.com/spreadsheets/d/1mpiBxI5rK_qs86IpbXgN1xbhrxS_VYF0XjI_fcRpl00/edit#gid=364353024
    mv ~/Downloads/schemaorg_translate.xlsx  ../data/releases/3.4/
3. goto cns.py, generate jsonld
4. goto search.py, update elastic search data
5. goto server.py, test server


rebuild  package
* req
   cp ../data/releases/3.4/classes.json ../vue-site/static/
   cp ../data/releases/3.4/properties.json ../vue-site/static/


online updated
rsync -rv -e ssh 3.4.0/ ubuntu@106.75.116.250:/home/ubuntu/cnschema.org/sites/3.4.0


python search.py task_es_load_data --version=3.4
python search.py task_es_test_regression
python search.py task_es_test --input 店
