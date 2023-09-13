import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# This function is used to get the BS4 doc by providing the page number


def get_doc(ps, page_number):
    time.sleep(2)
    url = 'https://www.foreclosure.com/listing/search?q=Florida&ps={}&pg={}&loc=Florida&view=list&'.format(
        str(ps), str(page_number))
    doc = get_page(url)
    return doc


def get_page(url):
    print("Scraping URL:", url)
    time.sleep(2)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)
    page_contents = response.text
    with open('webpage.html', 'w') as f:
        f.write(response.text)
    doc = BeautifulSoup(page_contents, 'html.parser')
    return doc


def get_property_addresses(doc):
    address_tages = doc.find_all('div', {"class": "address"})
    Addresses = []
    for tag in address_tages:
        try:
            title_attribute = tag.a.get('title')
            Addresses.append(title_attribute)
        except:
            Addresses.append("N/A")
    return Addresses


# get all the prices of the properties
def get_property_prices(doc):
    price_tags = doc.find_all('div', {"class": "savePrice"})
    Prices = []
    for tag in price_tags:
        try:
            price_text = tag.find('span', {"class": "tdprice"}).strong.text
            Prices.append(price_text)
        except:
            Prices.append("N/A")
    return Prices


def get_price_type(doc):
    save_price_tags = doc.find_all('div', {"class": "savePrice"})
    price_types = []
    for tag in save_price_tags:
        try:
            price_type = tag.find('span', {"class": "priceText"}).text.strip()
            if price_type == "EMV":
                price_type = "Estimated Market Value"
            price_types.append(price_type)
        except:
            price_types.append("N/A")
    return price_types


def get_rent_estimate(doc):
    rent_estimate_tags = doc.find_all('div', {"class": "rentEstimate"})
    estimates = []
    for tag in rent_estimate_tags:
        try:
            estimate_text = tag.text
            match = re.search(r'\$\d+\/m', estimate_text)
            estimates.append(match.group())
        except:
            estimates.append("N/A")
    return estimates


def get_property_type(doc):
    property_type_tags = doc.find_all('div', {"class": "fl c ptypebox"})
    types = []
    for tag in property_type_tags:
        try:
            type_text = tag.text.strip()
            type = type_text.split()[0]
            if type != "PROPERTY":
                types.append(type)
            else:
                types.append("N/A")
        except:
            types.append("N/A")
    return types


def get_bedrooms_count(doc):
    bedrooms_tags = doc.find_all('div', {"class": "fl c bedroomsbox"})
    bedroom_counts = []
    for tag in bedrooms_tags:
        try:
            bedroom_count = tag.contents[0].strip()
            if bedroom_count != "":
                bedroom_counts.append(bedroom_count)
            else:
                bedroom_counts.append("N/A")
        except:
            bedroom_counts.append("N/A")
    return bedroom_counts


def get_bathrooms_count(doc):
    bathrooms_tags = doc.find_all('div', {"class": "fl c barhroomsbox"})
    bathroom_counts = []
    for tag in bathrooms_tags:
        try:
            bathroom_count = tag.contents[0].strip()
            if bathroom_count != "":
                bathroom_counts.append(bathroom_count)
            else:
                bathroom_counts.append("N/A")
        except:
            bathroom_counts.append("N/A")
    return bathroom_counts


def get_property_status(doc):
    message_type_tags = doc.find_all('div', {"class": "messajeType"})
    messages = []
    for tag in message_type_tags:
        try:
            if "NEW" in tag.text:
                messages.append("new")
            else:
                messages.append("Foreclosure")
        except:
            messages.append("N/A")
    return messages


def get_square_feet(doc):
    square_feet_tags = doc.find_all('div', {"class": "fl c sizebox hidden-xs"})
    square_feet_values = []
    for tag in square_feet_tags:
        try:
            square_feet_text = tag.contents[0].strip()
            if square_feet_text != "":
                square_feet_text = square_feet_text.replace(',', '')
                square_feet_values.append(square_feet_text)
            else:
                square_feet_values.append("N/A")
        except:
            square_feet_values.append("N/A")
    return square_feet_values


def get_year_to_date_change(doc):
    view_details_tags = doc.find_all(
        'div', {"class": "contViewDetails text-right hidden-xs"})
    changes = []
    for tag in view_details_tags:
        try:
            year_to_date_change_tag = tag.find(
                'div', {"class": "yearToDateChange"})
            if year_to_date_change_tag:
                year_to_date_change_text = year_to_date_change_tag.text.strip()[
                    4:]

                changes.append(year_to_date_change_text)
            else:
                changes.append("N/A")
        except:
            changes.append("N/A")
    return changes


def get_address_link(doc):
    con_listing_photo_tags = doc.find_all('div', {"class": "conListingPhoto"})
    addresses = []
    for tag in con_listing_photo_tags:
        try:
            address_link = tag.a.get('href')
            address_link = "https://www.foreclosure.com" + address_link
            addresses.append(address_link)
        except:
            addresses.append("Not Available")
    return addresses

# def get_all_url(doc):
#     book_url_tag = doc.find_all('div', {"class": "zg-grid-general-faceout"})
#     Book_Title_Urls = []
#     base_url = "https://www.amazon.com"
#     for tag in book_url_tag:
#         try:
#             Book_Title_Urls.append(
#                 base_url + tag.find('a', {'class': 'a-link-normal'})['href'])
#         except:
#             Book_Title_Urls.append("Not Available")
#     return Book_Title_Urls


def get_all_details(ps, n):
    # n is the number of pages you want to scrape
    all_properties = {'Addresses': [],
                      'Price': [],
                      "Price Type": [],
                      "Rent Estimate": [],
                      "Property Type": [],
                      "Number of Bedrooms": [],
                      "Number of Bathrooms": [],
                      "Square Feet": [],
                      "YTD": [],
                      "Address Link": []}
    for page_number in range(1, n+1):
        print("Scraping page number:", page_number)
        doc = get_doc(ps, page_number)
        all_properties['Addresses'] += get_property_addresses(doc)
        all_properties['Price'] += get_property_prices(doc)
        all_properties['Price Type'] += get_price_type(doc)
        all_properties['Rent Estimate'] += get_rent_estimate(doc)
        all_properties['Property Type'] += get_property_type(doc)
        all_properties['Number of Bedrooms'] += get_bedrooms_count(doc)
        all_properties['Number of Bathrooms'] += get_bathrooms_count(doc)
        all_properties['Square Feet'] += get_square_feet(doc)
        all_properties['YTD'] += get_year_to_date_change(doc)
        all_properties['Address Link'] += get_address_link(doc)
    return all_properties


dataframe = pd.DataFrame.from_dict(get_all_details(100, 100), orient='index')
dataframe = dataframe.transpose()
dataframe.to_csv('real_estate.csv', index=None)
