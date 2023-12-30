import argparse
import random
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from car_data import CarData


SITE_URL = "https://www.polovniautomobili.com"
search_url = "https://www.polovniautomobili.com/auto-oglasi"

parser_on = True
pages = 1

user_agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]


def make_header():
    """
    Chooses a random agent from user_agents with which to construct headers
    :return headers: dict: HTTP headers to use to get HTML from article URL
    """
    # Make a header for the ClientSession to use with one of our agents chosen at random
    headers = {
        'User-Agent': random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9"
    }
    return headers


def parse_page(page_url):

    response = requests.get(page_url, headers=make_header())
    soup = BeautifulSoup(response.content, "html.parser")
    car_tags = soup.find_all(name="article", class_="classified")
    global pages
    pages_tag = soup.select("#search-results > div:nth-child(3) > div:nth-child(3) > div.uk-width-medium-5-10.uk-width-1-1.uk-margin-bottom > ul > li.uk-active")
        # Videti kako radi kada dodje do poslednjeg broja?
    if len(pages_tag) > 0:
        pages_number = pages_tag[0].find(name="span").getText()
        pages = int(pages_number) + 1
    else:
        # Ne radi kada nema brojeve stranica na sajtu
        return []

    car_data_list = []
    car_title_list = []
    for car_tag in car_tags:

        h2 = car_tag.find(name="h2")
        title = h2.find("a", class_="ga-title")
        link = title.get("href")
        car_data = CarData(url=link, site_url=SITE_URL, headers=make_header())
        car_title = title.get("title")
        car_title_list.append(car_title)
        car_data_list.append(car_data)

    return car_data_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async scraping for Polovni Automobili website")
    parser.add_argument("--pages", type=int, default=None, help="Specify number of pages to scrape for each keyword")
    parser.add_argument("--brand", type=str, default="nissan", help="Specify brand names")
    parser.add_argument("--model", type=str, default="juke", help="Specify model names")
    parser.add_argument("--price", type=int, default="8000", help="Maximum price for search")
    parser.add_argument("--year", type=int, default="2013", help="Specify minimum year")
    parser.add_argument("--output", type=str, default="cars.csv", help="Choose output file name. Default = cars.csv")
    args = parser.parse_args()

    if args.output[-4] != ".csv": args.output += ":csv"

    start = time.time()

    data_list = []
    while parser_on:

        parse_url = f"https://www.polovniautomobili.com/auto-oglasi/pretraga?page={pages}&sort=basic&" \
                    f"brand={args.brand}&model%5B0%5D={args.model}&price_to={args.price}&year_from={args.year}&" \
                    f"city_distance=0&showOldNew=all&without_price=1"

        print(parse_url)
        page_data = parse_page(parse_url)
        if len(page_data) != 0:
            for _ in page_data:
                data_list.append(_)
        else:
            parser_on = False

    car_list = [car.__dict__ for car in data_list]

    df = pd.DataFrame(car_list)
    df.to_excel("results.xlsx")


