# pyIntern Python3.7

## CsvReportProcessing

if you don't have virtualenv so use <code>pip install -r requirements.txt</code> for installing it globally

Create virtualenv: <code>python3 -m virtualenv venv</code>

Install virtualenv for example: <code>virtualenv -p /usr/bin/python3.7 venv/</code> (not necessary)

and source it use: <code>source venv/bin/activate</code> after that use <code>pip install -r requirements.txt</code>

for windows fast usage: <code> venv/bin/pyhon3.7 -m pip install -r requirements.txt</code>

and run: <code>python csv_report_processing.py<code>

for windows: <code>venv/bin/pyhon3.7 csv_report_processing.py</code>

## CSV FILE

Prepare CSV file with encoding UTF-8 or UTF-16 which should have with columns: date (MM/DD/YYYY), state name, number of impressions and CTR percentage.

Output file is saved in encoding UTF-8 with these columns: date (YYYY-MM-DD), three letter country code, number of impressions, number of clicks 

## Encoding

We want to use utf-8 or utf-16 so it requires one change in code.

Execution line: <code> create_ad_model_view("data-utf8.csv", "UTF-8") </code>

Second parameter is "UTF-8" as default but if we want to read file with encoding UTF-16 we should add parameter "UTF-16"

Example with UTF-16

<code> create_ad_model_view("data-utf16.csv", 'UTF-16') </code>
