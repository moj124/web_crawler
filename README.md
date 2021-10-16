# web_crawler
The web_crawler is a asynchoronous gevent link crawler that maps all the associated local links constrained by the input webpage url.

PLEASE MAKE SURE YOU RUN THE FOLLOWING COMMAND FOR CORRECT EXECUTION AND SAVING OF THE LOCAL LINK RELATIONS JSON FILE TO /DATA FOLDER:
```cmd
python3 crawl_website.py -l <url> -s True 
```

- [Requirements](#requirements)
- [Setup](#setup)
    -   [Windows](#windows)
    -   [Linux](#linux)
- [Run Script](#run-script-(linux))
    -   [Run Default with 'bbc.co.uk'](#run-default-settings-with-'bbc.co.uk')
    -   [Run with custom options](#run-with-custom-options)
- [Testing](#testing)
- [Issues](#issues)
## Requirements
- **Dependencies** (included in requirements.txt)
    - bs4
    - requests
    - gevent
  
- **Python Version Tested**
  - 3.7.10

## Setup

### Windows
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux
```cmd
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
## Run Script (Linux)

### Run default settings with 'bbc.co.uk'
```cmd
python3 crawl_website.py
```
### Run with custom options
```cmd
python3 crawl_website.py -l https://webscrapethissite.org -n 10
```
## Testing
```cmd
pytest test/
```
Or for detailed view
```cmd
pytest -v test/
```
## Issues
- The web crawler is unable to handle erroneous url links that contain no body.
- Failed HTTP GET request due to unauthorised permissions, partly due to headers.
- Asynchronous gevent threads are causing the queue within the Crawler to be empty while spawning.
