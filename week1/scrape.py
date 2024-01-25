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
    out = "".join(
        [
            booster_version
            for i, booster_version in enumerate(table_cells.strings)
            if i % 2 == 0
        ][0:-1]
    )
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
        new_mass = mass[0 : mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    colunm_name = " ".join(row.contents)

    # Filter the digit and empty names
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name


static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

# use requests.get() method with the provided static_url
# assign the response to a object
response = requests.get(static_url)

# Use BeautifulSoup() to create a BeautifulSoup object from a response text content
soup = BeautifulSoup(response.content, "html.parser")

# Use soup.title attribute
# print(soup.title)

# Use the find_all function in the BeautifulSoup object, with element type `table`
# Assign the result to a list called `html_tables`
html_tables = soup.find_all("table")

# Let's print the third table and check its content
first_launch_table = html_tables[2]
# print(first_launch_table)

column_names = []

# Apply find_all() function with `th` element on first_launch_table
# Iterate each th element and apply the provided extract_column_from_header() to get a column name
# Append the Non-empty column name (`if name is not None and len(name) > 0`) into a list called column_names
for ele in first_launch_table.find_all("th"):
    name = extract_column_from_header(ele)
    if name is not None and len(name) > 0:
        column_names.append(name)

# print(column_names)

launch_dict = dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict["Date and time ( )"]

# Let's initial the launch_dict with each value to be an empty list
launch_dict["Flight No."] = []
launch_dict["Launch site"] = []
launch_dict["Payload"] = []
launch_dict["Payload mass"] = []
launch_dict["Orbit"] = []
launch_dict["Customer"] = []
launch_dict["Launch outcome"] = []
# Added some new columns
launch_dict["Version Booster"] = []
launch_dict["Booster landing"] = []
launch_dict["Date"] = []
launch_dict["Time"] = []

extracted_row = 0
# Extract each table
for table_number, table in enumerate(
    soup.find_all("table", "wikitable plainrowheaders collapsible")
):
    # get table row
    for rows in table.find_all("tr"):
        # check to see if first table heading is as number corresponding to launch a number
        flag = False
        flight_number = -1
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        # get table element
        row = rows.find_all("td")
        # for id, ele in enumerate(row):
        #     print(f"col:{id}, content: {ele.text}")
        # if it is number save cells in a dictonary
        if flag and len(row) > 0:
            extracted_row += 1
            # Flight Number value
            # TODO: Append the flight_number into launch_dict with key `Flight No.`
            # print(flight_number)
            launch_dict["Flight No."].append(flight_number)
            datatimelist = date_time(row[0])

            # Date value
            # TODO: Append the date into launch_dict with key `Date`
            date = datatimelist[0].strip(",")
            # print(date)
            launch_dict["Date"].append(date)

            # Time value
            # TODO: Append the time into launch_dict with key `Time`
            time = datatimelist[1]
            # print(time)
            launch_dict["Time"].append(time)

            # Booster version
            # TODO: Append the bv into launch_dict with key `Version Booster`
            bv = booster_version(row[1])
            if not (bv):
                bv = row[1].a.string
            # print(bv)
            launch_dict["Version Booster"].append(bv)

            # Launch Site
            # TODO: Append the bv into launch_dict with key `Launch Site`
            launch_site = row[2].a.string
            # print(launch_site)
            launch_dict["Launch site"].append(launch_site)

            # Payload
            # TODO: Append the payload into launch_dict with key `Payload`
            payload = row[3].a.string
            # print(payload)
            launch_dict["Payload"].append(payload)

            # Payload Mass
            # TODO: Append the payload_mass into launch_dict with key `Payload mass`
            payload_mass = get_mass(row[4])
            # print(payload)
            launch_dict["Payload mass"].append(payload_mass)

            # Orbit
            # TODO: Append the orbit into launch_dict with key `Orbit`
            orbit = row[5].a.string
            # print(orbit)
            launch_dict["Orbit"].append(orbit)

            # Customer
            # TODO: Append the customer into launch_dict with key `Customer`
            # customer = row[6].a.string
            customer = row[6].text
            # print(customer)
            launch_dict["Customer"].append(customer.replace('\n', ''))

            # Launch outcome
            # TODO: Append the launch_outcome into launch_dict with key `Launch outcome`
            launch_outcome = list(row[7].strings)[0]
            # print(launch_outcome)
            launch_dict["Launch outcome"].append(launch_outcome.replace('\n', ''))

            # Booster landing
            # TODO: Append the launch_outcome into launch_dict with key `Booster landing`
            booster_landing = landing_status(row[8])
            # print(booster_landing)
            launch_dict["Booster landing"].append(booster_landing.replace('\n', ''))

df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })
print(df)
df.to_csv('spacex_web_scraped.csv', index=False)
