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

class ResultPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.credit_summary_items = self.soup.find_all('div', class_='credit_summary_item')
        self.subtext = self.soup.find('div', class_='subtext')

    def duration(self):
        t = self.soup.find('time')
        if t is not None:
            return t.text.strip()
        else:
            return "" # apparently in development/pre-production stage

    def title(self):
        title_div = self.soup.find('div', class_='title_wrapper')
        return title_div.find('h1').text.strip()

    def directors(self):
        ds = self.credit_summary_items[0].find_all('a')
        return ", ".join([d.text for d in ds])

    def stars(self):
        #  ignore last a href    is for full cast
        stars = self.credit_summary_items[-1].find_all('a')[:-1]
        return ", ".join([d.text for d in stars])

    def rating(self):
        subtext_items = self.subtext.text.split('|')
        return subtext_items[0].strip() if len(subtext_items) == 4 else ''

class MovieTitles(IMDBQueryBase):
    def __init__(self):
        super().__init__(self.by_movie_title)

    def retrieve_details_for(self, title, title_path):
        url = self.base_url + title_path
        # print(url)
        page = requests.get(url)
        result = ResultPage(page)

        print("Title: ", result.title())
        print("Director: ", result.directors())
        print("Stars: ", result.stars())
        print("Time: ", result.duration())
        print("Rating: ", result.rating())
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

    if args.by_movie_title:
        q = MovieTitles()
    # elif args.by_tv_title:
    #     q = TvTitels()

    q.query(args.search_term)

if __name__ == "__main__":
    main()
