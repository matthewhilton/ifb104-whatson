
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10463755
#    Student name: Matthew Hilton
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  What's On?: Online Entertainment Planning Application
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for planning an entertainment schedule.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.  You may import other widgets
# from the Tkinter module provided they are ones that come bundled
# with a standard Python 3 implementation and don't have to
# be downloaded and installed separately.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed one day).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it as a local file and returning its source code
# as a Unicode string. The function tries to produce
# a meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html'):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#

# Name of the planner file. To simplify marking, your program should
# generate its entertainment planner using this file name.
planner_file = 'planner.html'

###-----------  CONFIGURATION   ----------------###

# The maximum number of events per column
threshold = 7

# Stores whether to use offline/cached pages or not
offline = False

# Database file name
dbname = "entertainment_planner.db"

# Database table to store data
db_table = 'events'

# List of websites to be scraped for events
websites_to_scrape = [
    "https://cbussuperstadium.com.au/what-s-on.aspx",
    "https://www.eatonshillhotel.com.au/entertainment-and-events/",
    "http://bneart.com/",
]

# Labels for each column
category_labels = [
    "Sports at CBUS Super Stadium",
    "Events at Eatons Hill Hotel",
    "Art in Brisbane"
]

# Config for checkboxes - checkboxes have a lot of different color configurations, so its easier to save as object
checkbutton_config = {
    'bg':'red',
    'fg':'white',
    'highlightcolor':'firebrick',
    'highlightbackground':'firebrick',
    'selectcolor':'red',
    'activebackground':'red',
    'font': ("Arial", 12, 'bold')
}

# Styling configuration for event headers
header_config = {
    'bg':'maroon',
    'fg':'white',
    'width':30,
    'font': ("Arial", 12, 'bold')
}

###------------  END CONFIG  -----------------###

# Downloads files or uses cached ones if requested
def scraper(url, offline=True):

    # Respective extraction 'engines' for each website
    engines = {
        "https://cbussuperstadium.com.au/what-s-on.aspx": "cbus",
        "http://bneart.com/": "bneart",
        "https://www.eatonshillhotel.com.au/entertainment-and-events/": "eh"
    }

    # Check if URL is supported yet
    if(url not in engines):
        print("there is no supported extraction engine or cached page for ", url)
        return False

    print("\n*** ", url, " ***")
    print("URL accepted, engine/cached page found")

    # If not using cached files (i.e. downloading the live ones)
    if(not offline):
        print("using online page")
        print("downloading webpage")

        # Download live pages
        page = urlopen(url)
        # Parse web page
        html = page.read().decode('UTF-8')

        print("webpage download complete")

    # If using the cached files (the downloaded ones)
    elif(offline):
        print("using cached page")
        # Use cached file, using engines object to lookup file name corresponding to URL
        page = open('cached_pages/' + engines[url] + ".html", "r", encoding="utf8")
        html = page.read()
        page.close()

    # Pass off to extracter to extract information.
    return(extract_information(html, engines[url]))

# The janitor comes and cleans up the mess left behind by the html reader
def janitor(text):

    # List of all tags, and what to replace them with
    replacements = {
        "&#8217;": "'",
        "&#8211;": '',
        "&#8216;": '',
        "&#8230;": '',
        "&#038;": '&',
        "[&hellip;]": '',
        "\\xa0": '',
        "<br />": '',
        "&rsquo;": '',
        "&rdquo;": '',
        "&ndash": '',
        "\\r": '',
        '\\n': '',
        "&ldquo;": '',
    }

    # Go through text and replace according to list above
    for code in replacements:
        value = replacements[code]
        text = text.replace(code, value)

    return text

# Extracts information from webpages and formats it nicely into an object, returning it for use later
def extract_information(text, engine):

    print("trying to extract events...")

    # Empty array, to be filled with the response
    response = []

    # If the site is the CBUS super stadium
    if(engine == "cbus"):
        # Search HTML for event listings
        result = finditer('<div class="event (.*?)<strong>',text, DOTALL)

        # Iterate through each event found (there are usually about 9 of them)
        for event in result:
            text = event.group(0)

            # Find title of event and clean tags
            title = janitor(findall('<h6 class="event-title">(.*?)<', repr(text))[0])

            # Find event date and clean tags
            date = janitor(findall('<h7 class="event-date text-uppercase">(.*?)<', repr(text))[0])

            # Find image of event in event, concatenate to default domain
            imgurl = "https://cbussuperstadium.com.au" + findall('<img src="(.*?)"', repr(text))[0]

            # Find description of event and clean tags
            temp_description = findall('<div class="text-only" data-nb-lines="3"><p>(.*?)<strong>', repr(text), DOTALL)
            if(len(temp_description) > 0):
                description = temp_description
            else:
                description = ''

            # Package into a nice object
            event = {
                'title': title,
                'date': date,
                'imgurl': imgurl,
                'description': description
            }

            # Add event to response to return
            response.append(event)
        print("events extracted successfully")

    # If the website is the Brisbane Art website (BNEart)
    elif(engine == "bneart"):

        # Search HTML for event listings
        result = finditer('<article class="item-list item_(.*?)</article>',text, DOTALL)
        count = 0

        # Iterate through event tag matches
        for event in result:
            count += 1
            text = event.group(0)

            # Find title and and clean tags
            title = janitor(findall('Permalink to (.*?)"', repr(text))[0])

            # Find event date
            date = findall('WHEN</span> : (.*?)</h5>', repr(text))[0]

            # Find event image URL and clean tags
            imgurl = findall('src=\"(.*?)\"', repr(text))[0]

            # Find event description and clean tags
            description = janitor(findall('<p>(.*?)</p>', repr(text))[0])

            # Limit results, or else takes unnessesarily long as BNEart has a lot of events on their page
            if(count > 10):
                break;

            # Package into a nice object
            event = {
                'title': title,
                'date': date,
                'imgurl': imgurl,
                'description': description
            }

            # Add event to response to return
            response.append(event)
        print("events extracted successfully")

    # If the website to check is the Eatons Hill hotel website
    elif(engine == "eh"):

        # Search HTML for event listings
        result = finditer('<div class="event-item">(.*?)<div class="event-share alignleft"',text, DOTALL)

        # Iterate through event tag matches
        for event in result:
            text = event.group(0)
            # Find title and clean up tags
            title = janitor(findall('<h3>(.*?)<\/h3>', repr(text))[0])

            # Find event date
            date = findall('<strong>(.*?)<\/strong>', repr(text))[0]

            # Find event picture URL
            imgurl = findall('background-image:url(.*?)">', repr(text))

            # Special replacement just for this website to get rid of brackets that RegEx wouldn't
            imgurl = str(imgurl[0]).replace('(', '').replace(')', '')

            # Find event description and clean up tags
            description = janitor(findall('<div class="desc">(.*?)<\/div>', repr(text))[0])

            # Format nicely
            event = {
                'title': title,
                'date': date,
                'imgurl': imgurl,
                'description': description
            }

            # Add event to response to return
            response.append(event)
        print("events extracted successfully")
    return response

# Interface setup
gui = Tk()
gui.title(' HIO | event planner tool')
gui.configure(background="red")

# Setup Logo
logo_obj = PhotoImage(file="hio-logo.PPM")
logo = Label(gui, image=logo_obj, background='red')
logo.grid(row=1, column=2)

# Draw the three column labels and add to reference list
category_label_references = []

for label_index in range(0, 3):
    # Geneate 3 labels
    categoryLabel = Label(gui, header_config, text=category_labels[label_index])
    categoryLabel.grid(row=2, column=label_index+1, padx=5, pady=10)
    category_label_references.append(categoryLabel)

# A dump for all the data pulled from every website
data = []

# Coordinates the scraper() function to scrape site event data
def get_site_data():

    # Clear data storage (in case some was there from before)
    global data
    data = []

    # For each website that needs to be scraped
    for site_index in range(0,len(websites_to_scrape)):
        # Dump data from scraper function
        website_data = scraper(websites_to_scrape[site_index], offline=offline)
        data.append(website_data)
    return

# A record of key value pairs to uniquely identify each checkbox, so they can be iterated through later to determine if they are checked or not
checkboxList = {}

# Similar to checkboxList, but keeps a record of the WHOLE event widget, not just checkbox. Used to update event listings.
event_widget_record = []

# Updates the event listings according to stored data
def update_events():

    # Destroy all current event widgets
    for widget in event_widget_record:
        widget.destroy()

    # Show the user the data is loading
    loading(True)

    # Wait until gui has updated
    gui.update()

    # Download new Data
    get_site_data()

    # Repopulate with new data
    populate(threshold)

    # Remove the loading label text
    loading(False)
    return

# Populates event columns with events
def populate(threshold):

    # Iterate over each site (only 3 in this case)
    for site in data:
        for individual_event in site:
            # Only populate up until the threshold
            if(site.index(individual_event) < threshold):

                # Extract useful Data
                name = individual_event['title']
                date = individual_event['date']

                # Create event label frame (which displays the date)
                event = LabelFrame(gui, text=date, bg='red', fg='white', font=("Arial", 8))
                event.grid(row=site.index(individual_event)+3, column=data.index(site)+1, pady=2)

                # Append widget to record so it can be accessed later
                event_widget_record.append(event)

                # Title for the event (incide the label frame)
                event_title = Label(event, text=name, wraplength=210, anchor='w', width=30,bg='red', fg='white', font=("Arial", 8, 'bold'))
                event_title.pack(side=LEFT, padx=5)

                # Create unique ID for checkbox
                uniqueID = site.index(individual_event) + threshold*data.index(site)
                checkboxList[uniqueID] = IntVar()

                # Create checkbox for user selection, assign unique variable to list
                select = Checkbutton(event, checkbutton_config, variable=checkboxList[uniqueID])
                select.pack(side=RIGHT)
    return

# Switches between offline and online and updates GUI accordingly
def switch_mode():
    print("changing mode...")
    global offline

    # If offline, switch to online mode and change button text to reference change
    if(offline):
        offline = False
        status.configure(text="currently using live data")
    else:
        offline = True
        status.configure(text="currently using cached data")

    # Update gui with new data
    update_events()

    return

# Finds checkboxes that are selected, converts into useful format
def get_selected():

    # Record of absolute indexes that have checkboxes selected (these are all unique)
    absolute_indexes = []

    # Record of the real indexes that have checkboxes selected (index of checkbox within its column)
    real_indexes = []

    # Iterate through every checkbox on list
    for item in checkboxList:
        # If checkbox is selected, append to list
        if(checkboxList[item].get() == 1):
            absolute_indexes.append(item)

    # Convert them from absolute indexes to real index (its index within its column)
    for unique_id in absolute_indexes:
        # Work out column number based on threshold
        col_no = unique_id//threshold
        # Real_no is the index in the list of events in a particular column
        real_no = unique_id - (col_no * threshold)
        # Add to record
        real_indexes.append([col_no, real_no])

    # Return real indexes
    return real_indexes

# Gets the event details from the column and real value pairs the user has selected and gets details for those events.
def get_details(col_real_pairs):

    # Array to store events that were selected
    selected_events = []

    # Iterate through each selected checkbox
    for pair in col_real_pairs:

        # Extract useful data
        website_index = pair[0]
        row_num = pair[1]

        # Get website that corresponds to column containing checkbox selected
        website_data = data[website_index]
        # Get event from website data corresponding to checkbox selected
        event = website_data[row_num]

        # Add event details to array for display to user
        selected_events.append(event)

    return selected_events

# Creates a HTML webpage planner based off of events passed to it
def create_planner():
    # First get selected events
    indexes = get_selected()

    # Get event details of each index
    selected_events = get_details(indexes)

    # Make list of event details using <li> tags to insert into HTML
    try:
        li_elements = ""
        for event in selected_events:
            li_elements += "<li> <b> "+ event['title'] + " </b> on " + event['date'] + "<br><br> <img src=" + event['imgurl'] + " alt='Image for Event'> </li> \n            "

        # Make a list of links used
        link_elements = ""
        for site in websites_to_scrape:
            link_elements += "<a href='"+ site +"'>" + site + "</a> <br> \n        "

        # Create file object
        html_planner = open(planner_file, "w")
        # Write HTML file contents
        html_planner.write("""
    <!DOCTYPE html>
    <html>
    <!-- An Automatically generated planner for events from the HIO application (whats_on.py) -->
        <head>
            <meta charset="UTF-8">
            <title>Custom Event Plan from HIO</title>
            <!-- Styling for document (basically just colours) -->
            <style>
                body {
                    color: white;
                    text-align: center;
                    background-color: red;
                    font-style: sans-serif;
                    font-family: Arial;
                }

                ul {
                    list-style-type: none;
                }

                li {
                    padding-top: 10px;
                    padding-bottom: 10px;
                    margin-bottom: 10px;
                    border-left: 8px solid white;
                    box-sizing: border-box;
                    background-color: #ce0300;
                }

                img {
                    max-width: 30%;
                    height: auto;
                }

                a {
                    color: white;
                }

                a:visited {
                    color: white;
                }
            </style>
        </head>

        <body>
            <!-- Banner Image -->
            <img src="http://i65.tinypic.com/2a9uuqp.png" border="0" alt="HIO Banner Image">

            <!-- List of events user has selected -->
            <ul>
                """
                + li_elements +
                """
            </ul>

            <!-- Links to websites -->
            <h3> Events sourced from: </h3>
            """
            + link_elements +
            """
        </body>
    </html>
    """)
        # Close file object
        html_planner.close()

        print("Planner created! ", planner_file)
    except:
        print("An error occured when creating the planner: ", planner_file)
    return

# Checks if events() table exists, creates if it doesn't
def checkTableExists():
    # If some error with database, sqlite3 will create empty db file
    # Adds tables to db when sqlite3 creates an empty file to ensure program still works
    create_table_query = ('CREATE TABLE IF NOT EXISTS {0}(event_name TEXT NOT NULL, event_date TEXT NOT NULL)').format(db_table)

    # Try query, error if fails
    try:
        database.execute(create_table_query)
        database.commit()
    except:
        print("An error occurred when executing query: " + create_table_query)
        print("Table most likely already exists")
    return

# Saves selected events to database
def saveToDatabase():
    print("Saving events to database: ", dbname, " table: ", db_table)

    global database
    # Create a database cursor
    database = connection.cursor()

    # Make sure table exists
    checkTableExists()

    # Clear database of previous data
    database.execute("DELETE FROM " + db_table)

    # Get selected event details
    indexes = get_selected()
    event_details = get_details(indexes)

    # Insert data into database
    for event in event_details:

        # Structure query
        insert_query = ('INSERT INTO {0}(event_name, event_date) VALUES("{1}","{2}")').format(db_table, event['title'], event['date'])

        # Try query, error if fails
        try:
            database.execute(insert_query)
        except:
            print("An error occurred when executing query: " + insert_query)

    # Commit changes to Database
    connection.commit()

    return

# Connects to database
def connectDatabase():
    global connection

    # Let user know state of database
    dbconnection.config(text="ERROR: Database not connected!", bg="darkred")
    print("Connecting to " + dbname)

    # Connect to database
    connection = connect(database=dbname)

    # Let user know state of database
    dbconnection.config(text="Database connected", bg="tomato")
    print("Database connected!")

# Updates GUI to let user know data is loading
def loading(isLoading):

    # Iterate through each category label
    for label in category_label_references:
        if(isLoading):
            label.config(text="Data is loading...")
        else:
            index = category_label_references.index(label)
            label.config(text=category_labels[index])
    return

###----------------------GUI setup----------------------###

# Footer automatically goes to bottom even when amount of events changes
footerRow = threshold+3

# Button to allow user to switch online/offline mode
useoffline = Button(gui, text="Switch data source", command=switch_mode, width="36", bg="red", fg="white", activebackground="firebrick", activeforeground="white", font=("Arial", 8, "bold"))
useoffline.grid(row=footerRow, column=1, pady=10)

# Button to allow user to create a HTML planner document
submit = Button(gui, text="Create Planner", command=create_planner, width="36", bg="firebrick", fg="white", activebackground="maroon", activeforeground="white", font=("Arial", 8, "bold"))
submit.grid(row=footerRow, column=3, pady=10)

# Button to let user know where data is currently coming from
status = Label(gui, text="currently using live data", width="36", bg="red", fg="white", font=("Arial", 10, "bold"))
status.grid(row=footerRow, column=2, pady=10)

# Label for database connection
dbconnection = Label(gui, width="36", bg="red", fg="white", font=("Arial", 10, "bold"))
dbconnection.grid(row=footerRow+1, column=1, pady=10)

# Button for user to insert data into database
insertDatabase = Button(gui, text="Save to Database", command=saveToDatabase, width="36", bg="firebrick", fg="white", activebackground="maroon", activeforeground="white", font=("Arial", 8, "bold"))
insertDatabase.grid(row=footerRow+1, column=3, pady=10)

###-------------------End GUI setup----------------------###

# Start loading data 100ms after GUI has loaded
gui.after(100, update_events)

# Connect to database once interface has loaded
gui.after(100, connectDatabase)

# Main loop for TKinter, loops forever
gui.mainloop()
