# `WhatsOn.py`
A neat little program that extracts data from websites (scraping) and displays it in a nice user interface for the user to select and create a HTML planner from.

**Completed as second assessment for the unit IFB104**

## How does it work?
It mainly uses the python findall() function from the regex (re) library. For this assessment, we weren't allowed to use other web scraping libraries such as BeautifulSoup. The script downloads pages on opening, searching through them to find the event data. This is then displayed in a nice list as shown below.

![alt text](https://i.imgur.com/U1lgcRt.png, 'Example user interface')

## What does it do?
Users can select events, and then either select the 'Create Planner' button or the 'Save to Database' button.
### Create Planner
This will create a HTML document called `planner.html` in the same directory as `whatson.py`. This planner contains more details about the selected events, and is fully portable. 

### Save to Database
This was added not for any real purpose, but as a requirement of the assessment. Upon pressing, the program will save the events selected to an Sqlite database called `entertainment_planner.db`.

## Other features
If for some reason the online versions of the pages don't work (i.e. they change), users can select the 'switch data source' button to switch to using cached pages, which should work all the time as they are a snapshot of what the pages looked like when I created this. 
