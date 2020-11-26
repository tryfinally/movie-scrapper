#!/usr/bin/env python3

import sys
import argparse
import requests
from bs4 import BeautifulSoup

def prepare_search_url(args):
    query = " ".join(args.search_term)
    query_type = "ft" if args.by_movie_title else "tv"
    return "https://www.imdb.com/find?q={}&s=tt&ttype={}".format(query, "ft")

def retrieve_details_for(title, title_url):
    url = "https://www.imdb.com" + title_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title_div = soup.find('div', class_='title_wrapper')
    title = title_div.find('h1').text
    length = soup.find('time').text
    subtext = soup.find('div', class_='subtext')
    subtext_items = subtext.text.split('|')
    # print(subtext_items)
    credit_summary_items = soup.find_all('div', class_='credit_summary_item')

    directors = credit_summary_items[0].find_all('a')
    directors_names = ", ".join([d.text for d in directors])

    #  ignore last a href is for full cast
    stars = credit_summary_items[2].find_all('a')[:-1]
    stars_names = ", ".join([d.text for d in stars])

    print(title)
    print("Director: ", directors_names)
    print("Stars: ", stars_names)
    print("Time: ", length.strip())
    print("Rating: ", subtext_items[0].strip())
    print("----"*10)





def retrieve_records_for(results):
    for result in results:
        record = result.find('td', class_='result_text')
        title = record.text
        titl_url = record.find('a')['href']
        retrieve_details_for(title, titl_url)

def queryIMDb(args):
    url = prepare_search_url(args)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    main_response = soup.find(id='main')
    # print(results.prettify())

    list = main_response.find_all('table', class_='findList')
    results = list[0].find_all('tr', class_='findResult')

    retrieve_records_for(results)

def main():
    parser = argparse.ArgumentParser(description='IMDb scraper')
    parser.add_argument('search_term', action='store', nargs='*',
                        help='Search term to query IMDb. like word/s in title')


    parser.add_argument('-m', action='store_true', dest='by_movie_title', default=False,
                            help='Search by movies title. This is the default')
    parser.add_argument('-v', action='store_true', dest='by_tv_title', default=False,
                            help='Search by TV title.')

    args = parser.parse_args()
    if len(args.search_term) == 0:
        print("you must specify a search term")
        exit(1)

    queryIMDb(args)

if __name__ == "__main__":
    main()
