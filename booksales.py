import time
import jovian
import requests
from bs4 import BeautifulSoup
import pandas as pd

# This function is used to get the BS4 doc by providing the page number


def get_doc(page_number):
    time.sleep(2)
    url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_{}?ie=UTF8&pg={}'.format(
        str(page_number), str(page_number))
    doc = get_page(url)
    return doc


def get_page(url):
    print("Scraping URL:", url)
    time.sleep(2)
    response = requests.get(url)
    print("Status code:", response.status_code)
    page_contents = response.text
    with open('webpage.html', 'w') as f:
        f.write(response.text)
    doc = BeautifulSoup(page_contents, 'html.parser')
    return doc


def get_book_title(doc):
    book_title_tags = doc.find_all('div', {"class": "zg-grid-general-faceout"})
    Book_Titles = []
    for tag in book_title_tags:
        try:
            title_tag = tag.find('span')
            Book_Titles.append(title_tag.text)
        except:
            Book_Titles.append("Not Available")
    return Book_Titles


# get all the authors name
def get_all_authors(doc):
    author_name_tags = doc.find_all(
        'div', {'class': 'zg-grid-general-faceout'})
    Author_Names = []
    for tag in author_name_tags:
        try:
            Author_Names.append(
                tag.find('div', {'class': 'a-row a-size-small'}).text)
        except:
            Author_Names.append("Not Available")
    return Author_Names

# get the rating on each book


def get_all_stars(doc):
    rating_tags = doc.find_all('div', {'class': 'zg-grid-general-faceout'})
    Stars = []
    for tag in rating_tags:
        try:
            Stars.append(tag.find('span', {'class': 'a-icon-alt'}).text)
        except:
            Stars.append("Not Available")

    return Stars

# get the cost of the books


def get_all_price(doc):
    book_price_tags = doc.find_all('div', {"class": "zg-grid-general-faceout"})
    Book_Price = []
    for tag in book_price_tags:
        try:
            Book_Price.append(
                tag.find('span', {'class': 'p13n-sc-price'}).text)
        except:
            Book_Price.append("Not Available")

    return Book_Price

# at last get the book url


def get_all_url(doc):
    book_url_tag = doc.find_all('div', {"class": "zg-grid-general-faceout"})
    Book_Title_Urls = []
    base_url = "https://www.amazon.in"
    for tag in book_url_tag:
        try:
            Book_Title_Urls.append(
                base_url + tag.find('a', {'class': 'a-link-normal'})['href'])
        except:
            Book_Title_Urls.append("Not Available")
    return Book_Title_Urls


def get_all_details(n):
    all_books = {'Title': [], 'Author': [],
                 'Stars': [], 'Price': [], 'URL': []}
    for page_number in range(1, n+1):
        doc = get_doc(page_number)
        all_books['Title'] += get_book_title(doc)
        time.sleep(1)
        all_books['Author'] += get_all_authors(doc)
        time.sleep(1)
        all_books['Stars'] += get_all_stars(doc)
        time.sleep(1)
        all_books['Price'] += get_all_price(doc)
        time.sleep(1)
        all_books['URL'] += get_all_url(doc)
        time.sleep(1)

    return all_books


url = 'https://www.amazon.in/gp/bestsellers/books/'
dataframe = pd.DataFrame.from_dict(get_all_details(2), orient='index')
dataframe = dataframe.transpose()
dataframe.to_csv('books.csv', index=None)

jovian.commit(files=['books.csv'])
