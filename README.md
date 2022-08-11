# ETL Process
1. Crawl data from Open Weather API
2. Load data into SQLite relational database
3. Schedule process to run every 3 seconds

## Requirements
_____________

✔️ Python --version 3.7 or above to run the project

- Download Python at [https://www.python.org/downloads/](https://www.python.org/downloads/)

✔️ Python libraries:

- from asyncio.windows_events import NULL
- import sqlite3 (included in the standard library since Python 2.5).
- import schedule
- import requests
- import json (built-in module)

✔️ Environment: Visual Studio Code, with listed extensions:

- Python (to run Python source)
- SQLite Viewer (to view SQLite tables)

✔️ Project Package Management: Poetry
_____________
## SOURCE FOLDER
- `src/main.py`: run this file, which contains whole process
- `src/database.py`: contains database operations
- `src/utilities.py`: contains file-database processing functions
- `schema/Schema.jpg`: database schema image
- `schema/response_description.txt`: API data description
- `result/weather.json`: response value from API, saved in JSON format
- `result/weather.db`: SQLite database
_____________
## HOW TO RUN
1. Install Python 3.x version, VS Code (https://code.visualstudio.com/), listed above libraries and extensions
2. In Terminal of VS Code, run the command to install all required packages
```
>> pip install poetry
>> poetry install
```
2. Run main.py file
    - "Enter file name (i.e: weather.json)": give JSON file a name, this file will store crawled data
    - "Enter database name (i.e: weather.db)": give SQLite database a name
    - "Enter location": city name (i.e: Hanoi, Moscow, New York, Tokyo, Havana, Seoul, Saigon, Paris, Berlin,..)
    - "Enter unit": metric or imperial
3. If there is no error, the program will produce 2 new files (auto-generate): <name>.json and <name>.db (with crawled data)
