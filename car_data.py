import requests

from bs4 import BeautifulSoup


def get_name(soup):
    return soup.find(name="h1").getText()


class CarData:

    def __init__(self, url, site_url, headers):
        self.page_url = f"{site_url}{url}"
        self.car_name = None
        self.car_brand = None
        self.car_model = None
        self.car_type = None
        self.car_age = None
        self.kilometers = None
        self.fuel = None
        self.power = None
        self.cm = None
        self.price = None
        self.get_data(headers)

    def get_data(self, headers):
        response = requests.get(self.page_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        self.car_name = get_name(soup)
        info_box = soup.find(name="div", class_="infoBox")
        # print(info_box)
        info_box_values = info_box.find_all(name="div", class_="uk-width-1-2")
        # print(info_box_values)
        num_values = len(info_box_values)
        index_value = 0
        for i in range(index_value, num_values - 1):
            if info_box_values[i].getText() == "Marka":
                self.car_brand = info_box_values[i+1].getText()
            elif info_box_values[i].getText() == "Model":
                self.car_model = info_box_values[i + 1].getText()
            elif info_box_values[i].getText() == "Godište":
                self.car_age = info_box_values[i + 1].getText()
            elif info_box_values[i].getText() == "Kilometraža":
                self.kilometers = info_box_values[i+1].getText()
            elif info_box_values[i].getText() == "Gorivo":
                self.fuel = info_box_values[i+1].getText()
            elif info_box_values[i].getText() == "Kubikaža":
                self.cm = info_box_values[i+1].getText()
            elif info_box_values[i].getText() == "Snaga motora":
                self.power = info_box_values[i+1].getText()
            elif info_box_values[i].getText() == "Karoserija":
                self.car_type = info_box_values[i+1].getText()
            else:
                continue
        price = soup.select("body > div.details.js-ad-details-page > div.uk-container.uk-container-center.body > div.table.js-tutorial-all > aside > div.uk-grid > div > div > div > div > span")
        self.price = price[0].getText()


