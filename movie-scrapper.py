#!/usr/bin/env python3

import sys
import argparse
import requests
from bs4 import BeautifulSoup


class IMDBQueryBase(object):
    by_movie_title = "ft"
    by_tv_title = "tv"
    def __init__(self, query_type):
        self.base_url = "https://www.imdb.com"
        # query = " ".join(args.search_term)
        # query_type = "ft" if args.by_movie_title else "tv"
        self.query_url_template = self.base_url + "/find?q={{}}&s=tt&ttype={}".format(query_type)

    def query(self, search_term):
        # print(url)
        query = " ".join(search_term)
        query_url = self.query_url_template.format(query)
        page = requests.get(query_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        main_response = soup.find(id='main')
        # print(results.prettify())

        list = main_response.find('table', class_='findList')
        results = list.find_all('tr', class_='findResult')
        self.retrieve_records(results)

    def retrieve_records(self, results):
        for result in results:
            record = result.find('td', class_='result_text')
            title = record.text
            title_path = record.find('a')['href']
            self.retrieve_details_for(title, title_path)


class MovieTitles(IMDBQueryBase):
    def __init__(self):
        super().__init__(self.by_movie_title)

    def retrieve_details_for(self, title, title_path):
        url = self.base_url + title_path
        # print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        #this is not accurate
        time = soup.find('time')
        if time is not None:
            length = time.text.strip()
        else:
            return # apparently in development/pre-production stage

        title_div = soup.find('div', class_='title_wrapper')
        title = title_div.find('h1').text.strip()

        subtext = soup.find('div', class_='subtext')
        subtext_items = subtext.text.split('|')
        rating = subtext_items[0].strip() if len(subtext_items) == 4 else ''
        # print(subtext_items)
        credit_summary_items = soup.find_all('div', class_='credit_summary_item')

        directors = credit_summary_items[0].find_all('a')
        directors_names = ", ".join([d.text for d in directors])

        #  ignore last a href    is for full cast
        stars = credit_summary_items[-1].find_all('a')[:-1]
        stars_names = ", ".join([d.text for d in stars])

        print(title)
        print("Director: ", directors_names)
        print("Stars: ", stars_names)
        print("Time: ", length)
        print("Rating: ", rating)
        print("----"*10)


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

    # queryIMDb(args)
    mq = MovieTitles()
    mq.query(args.search_term)

if __name__ == "__main__":
    main()
