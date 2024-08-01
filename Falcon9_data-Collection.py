import sys

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd


def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out


def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    colunm_name = ' '.join(row.contents)

    # Filter the digit and empty names
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

# use requests.get() method with the provided static_url
# assign the response to an object
response=requests.get(static_url)

# Use BeautifulSoup() to create a BeautifulSoup object from a response text content
soup=BeautifulSoup(response.content, 'html.parser')

# Use soup.title attribute
print(soup.title)

# Use the find_all function in the BeautifulSoup object, with element type `table`
# Assign the result to a list called `html_tables`
# Find all tables
html_tables = soup.find_all('table')

# Print the number of tables found
print(f"Number of tables found: {len(html_tables)}")

first_launch_table = html_tables[2]

# Initialize an empty list to store column names
column_names = []

# Use the third table as the first launch table
first_launch_table = html_tables[2]

# Find all <th> elements in the first launch table
headers = first_launch_table.find_all('th')

# Iterate through each <th> element and extract column names
for header in headers:
    column_name = extract_column_from_header(header)
    if column_name is not None and len(column_name) > 0:
        column_names.append(column_name)

# Apply find_all() function with `th` element on first_launch_table
# Iterate each th element and apply the provided extract_column_from_header() to get a column name
# Append the Non-empty column name (`if name is not None and len(name) > 0`) into a list called column_names
# Find the first launch table

# Initialize an empty list to store column names
column_names = []

# Use the third table as the first launch table
first_launch_table = html_tables[2]

# Find all <th> elements in the first launch table
headers = first_launch_table.find_all('th')

# Iterate through each <th> element and extract column names
for header in headers:
    column_name = extract_column_from_header(header)
    if column_name is not None and len(column_name) > 0:
        column_names.append(column_name)

launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

extracted_row = 0
# Extract each table
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    # Get table row
    for rows in table.find_all("tr"):
        # Check to see if first table heading is a number corresponding to launch number
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        # Get table element
        row = rows.find_all('td')
        # If it is a number, save cells in a dictionary
        if flag:
            extracted_row += 1
            # Flight Number value
            launch_dict['Flight No.'].append(flight_number)

            datatimelist = date_time(row[0])

            # Date value
            date = datatimelist[0].strip(',')
            launch_dict['Date'].append(date)

            # Time value
            time = datatimelist[1]
            launch_dict['Time'].append(time)

            # Booster version
            bv = booster_version(row[1])
            if not bv:
                bv = row[1].a.string
            launch_dict['Version Booster'].append(bv)

            # Launch Site
            launch_site = row[2].a.string if row[2].a else row[2].text.strip()
            launch_dict['Launch site'].append(launch_site)

            # Payload
            payload = row[3].a.string if row[3].a else row[3].text.strip()
            launch_dict['Payload'].append(payload)

            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)

            # Orbit
            orbit = row[5].a.string if row[5].a else row[5].text.strip()
            launch_dict['Orbit'].append(orbit)

            # Customer
            customer = row[6].a.string if row[6].a else row[6].text.strip()
            launch_dict['Customer'].append(customer)

            # Launch outcome
            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'].append(launch_outcome)

            # Booster landing
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)

# Print the filled launch_dict to verify
#print(launch_dict)\

df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })
print(df)

#replace zero values in Payload

# Function to clean and convert payload mass values
def clean_payload_mass(value):
    try:
        # Ensure the value is a string before applying string methods
        if isinstance(value, str):
            # Remove "kg", strip whitespace, remove commas, and convert to float
            value = value.replace('kg', '').strip().replace(',', '')
            # Remove "~" and convert to float
            value = value.replace('~', '')
            # Handle "C" and "Unknown" cases
            if value in ["C", "Unknown"]:
                return float('nan')
        return float(value)
    except ValueError:
        # Return NaN for invalid entries
        return float('nan')

# Apply the cleaning function to the 'Payload mass' column
df['Payload mass'] = df['Payload mass'].apply(clean_payload_mass)

# Calculate the mean of the 'Payload mass' column, excluding NaN and zero values
mean_payload_mass = df[df['Payload mass'] != 0]['Payload mass'].mean()

# Round the mean value
mean_payload_mass = round(mean_payload_mass)

# Replace zero values and NaN values in the 'Payload mass' column with the rounded mean
df['Payload mass'] = df['Payload mass'].replace(0, mean_payload_mass)
df['Payload mass'] = df['Payload mass'].fillna(mean_payload_mass)

# Convert the 'Payload mass' column to integers
df['Payload mass'] = df['Payload mass'].astype(int)

# Print the updated DataFrame to verify
print(df)
df.to_csv('spacex_web_scraped.csv', index=False)