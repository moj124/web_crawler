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
- [Notes](#notes)
    -   [Team Work & Planning](#team-work-&-planning)
    -   [Testing](#testing)
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
# Notes
## Team Work & Planning
Project's [Kanban Board](https://solstice-ceres-14f.notion.site/Web-Crawler-20699892940c46fa990d76079a0dd897)
-   Create a Kanban Board to structure project management, process tasks into bitesize tickets that are actionable.
-   In order to work with others in a team, I would of had a meeting to discuss the required tasks in order to complete the project.
-   Assigned tickets to each person that can be worked on simultaenously without conflict and set deadlines.
-   Create a system of accountability to review each others code via Kanban Board columns and fix any blocked tasks.
-   Set meetings within the team that match the deadlines set at important milestones.
-   Create branches in version control whereby we create multiple methods to implement or fix a feature.
-   Peer review branches to understand what code goes into the main branch and into deployment.

## Testing
- Create tests for development usage to ensure correct functionality
- Create secret tests that haven't been used in development to finally test the deployed code, ideally someone who hasn't coded the functionality within the team.

## Issues
- The web crawler is unable to handle erroneous url links that contain no body.
- Failed HTTP GET request due to unauthorised permissions, partly due to headers.
- Asynchronous gevent threads are causing the queue within the Crawler to be empty while spawning.
