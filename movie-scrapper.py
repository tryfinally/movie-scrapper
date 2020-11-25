#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(description='IMDb scraper')
    parser.add_argument('search_term', action='store',
                        help='Search term to query IMDb. like word/s in title')


    parser.add_argument('-m', action='store_true', dest='by_movie_title', default=False,
                            help='Search by movies title. This is the default')
    parser.add_argument('-v', action='store_true', dest='by_tv_title', default=False,
                            help='Search by TV title.')

    args = parser.parse_args()


if __name__ == "__main__":
    main()
