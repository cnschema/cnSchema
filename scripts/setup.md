
# maintain

local update。，。
1. goto settings.py, update version=...
2. goto cns.py, generate jsonld
3. goto search.py, update elastic search data
4. goto server.py, test server

rebuild  package

online updated


python search.py task_es_load_data --version=3.4
python search.py task_es_test_regression
python search.py task_es_test --input 店
