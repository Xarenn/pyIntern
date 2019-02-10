# pyIntern Python3.7

## CsvReportProcessing

if you don't have virtualenv so use <code>pip install -r requirements.txt</code> for installing it globally

Create virtualenv: <code>python3 -m virtualenv venv</code>

Install virtualenv for example: <code>virtualenv -p /usr/bin/python3.7 venv/</code>

Prepare CSV file with encoding UTF-8 or UTF-16 which this require one change in code.

Execution line: <code> create_ad_model_view("data-utf8.csv", 'UTF-16') </code>

Second parameter is "UTF-8" as default but if we want to read file with encoding UTF-16 we should add parameter "UTF-16"

Example with UTF-16

<code> create_ad_model_view("data-utf16.csv", 'UTF-16') </code>
