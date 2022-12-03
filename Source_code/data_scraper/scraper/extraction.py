from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import csv
import threading
import time
import asyncio
from hotel_scraper import scrape_hotel_links
import sys
from hotel_links import links
from headers import user_agent_list
from lxml.html import fromstring
from itertools import cycle
import random

hotel_count = 0
number_of_requests = 0
user_agent_list_cycle = cycle(user_agent_list)


def random_delay():
    time.sleep(random.uniform(0, 1) * 4)


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
        #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return list(proxies)


def get_header():
    global number_of_requests
    return {
        "User-Agent": user_agent_list[number_of_requests % len(user_agent_list)]
    }

""" General hotel data scraping here """


def scrape_hotel_data(url, hotel_id):
    """ Scrape the general data of the hotel url"""
    global number_of_requests
    print(url)
    headers = {
        "User-Agent": next(user_agent_list_cycle)
    }

    try:
        response = requests.get(url, headers=headers)
        number_of_requests += 1
        print(f"request number {number_of_requests}")
    except:
        return "CANNOT REQUEST"

    html = response.content

    try:
        parsed_html = BeautifulSoup(html, 'lxml')
    except:
        return {
            "hotel_id": None,
            "hotel_name": None,
            "hotel_stars": None,
            "address": None,
            "cat_location": None,
            "cat_cleaniness": None,
            "cat_staff": None,
            "cat_comfort": None,
            "cat_value_for_money": None,
            "cat_facilities": None,
            "room_types": None,
            "image_links": None

        }

    hotel_name, hotel_stars, cat_staff, cat_comfort, cat_facilities, cat_value_for_money, cat_cleaniness, cat_location, address, images_links = None, None, None, None, None, None, None, None, None, None

    try:
        hotel_name = parsed_html.find("h2", {"class": "pp-header__title"}).text.strip('\n')
    except:
        print("No hotel name")
    try:
        hotel_stars = len(parsed_html.findAll("span", {"class": "b6dc9a9e69 adc357e4f1 fe621d6382"}))
    except:
        hotel_stars = 0
    try:
        cat_cleaniness = float(parsed_html.findAll("span", {"class": "c-score-bar__score"})[0].text)
    except:
        print("no cat_clean")
    try:
        cat_location = float(parsed_html.findAll("span", {"class": "c-score-bar__score"})[1].text)
    except:
        print("no cat_loc")
    try:
        cat_staff = float(parsed_html.findAll("span", {"class": "c-score-bar__score"})[2].text)
    except:
        print("no cat_staff")
    try:
        cat_comfort = float(parsed_html.findAll("span", {"class": "c-score-bar__score"})[3].text)
    except:
        print("no cat_comfy")
    try:
        cat_facilities = float(parsed_html.findAll("span", {"class": "c-score-bar__score"})[4].text)
    except:
        print("no cat_fac")
    try:
        cat_value_for_money = float(parsed_html.findAll("span", {"class": "c-score-bar__score"})[5].text)
    except:
        print("no cat_val")
    try:
        address = parsed_html.find("span", {"class": "hp_address_subtitle"}).text.strip('\n')
    except:
        print("no address")

    # Get the table of rooms and prices
    room_types_dict = {}
    try:
        rooms_table = parsed_html.find("table", {"id": "hprt-table"})
        room_type_rows = rooms_table.findAll("td", {
            "class": "hprt-table-cell -first hprt-table-cell-roomtype droom_seperator"})  # Need to be findAll
        prices = rooms_table.findAll('span', {"class": "prco-valign-middle-helper"})

        index = 0

        for room_type_row in room_type_rows:
            row_span = room_type_row.attrs["rowspan"]
            room_type = room_type_row.find("span", {"class": "hprt-roomtype-icon-link"}).text.strip('\n')
            room_type_prices = []
            for i in range(int(row_span)):
                room_type_prices.append(prices[index].text.strip('\n'))
                index += 1
            room_types_dict[room_type] = room_type_prices
    except:
        print("No table")

    # Get the images links
    try:
        images = parsed_html.findAll("img", {"class": "hide"})
        images_links = [link.attrs['src'] for link in images]
    except:
        images_links = None

    hotel_dict = {
        "hotel_id": hotel_id,
        "hotel_name": hotel_name,
        "hotel_stars": hotel_stars,
        "address": address,
        "cat_location": cat_location,
        "cat_cleaniness": cat_cleaniness,
        "cat_staff": cat_staff,
        "cat_comfort": cat_comfort,
        "cat_value_for_money": cat_value_for_money,
        "cat_facilities": cat_facilities,
        "room_types": room_types_dict,
        "image_links": images_links

    }
    print(f"{hotel_id} finished scraping")


    return hotel_dict


""" Reviews Data Scraping Here """


def scrape_individual_review(review_li):
    """ Scrape the individual reviews """

    title, positive_des, negative_des, rating, room_type, user_country, type_of_travel, username, date, no_of_nights = None, None, None, None, None, None, None, None, None, None
    try:
        title = review_li.find("h3", {"class": "c-review-block__title c-review__title--ltr"}).text.strip('\n')
    except:
        title = None

    review_des_divs = review_li.findAll("div", {"class": "c-review__row"})
    for review_des_div in review_des_divs:
        try:
            pos_or_negative = review_des_div.find("span", {"class": "bui-u-sr-only"}).text.strip("\n")
            if pos_or_negative == "Liked":
                positive_des = review_des_div.find("span", {"class": "c-review__body"}).text.strip("\n")

            elif pos_or_negative == "Disliked":
                negative_des = review_des_div.find("span", {"class": "c-review__body"}).text.strip("\n")
        except:
            positive_des = None
            negative_des = None
    try:
        rating = float(review_li.find("div", {"class": "bui-review-score__badge"}).text.strip('\n').strip(' '))
    except:
        rating = None

    try:
        room_type = review_li.find(
            "div", {"class": "c-review-block__row c-review-block__room-info-row"}
        ).find(
            "div", {"class": "bui-list__body"}).text.strip('\n')
    except:
        room_type = None

    try:
        user_country = review_li.find("span", {"class": "bui-avatar-block__subtitle"}).text.strip('\n')
    except:
        user_country = None
    try:
        type_of_travel = review_li.findAll("div", {"class": "bui-list__body"})[2].text.strip('\n')
    except:
        type_of_travel = None
    try:
        username = review_li.find("span", {"class": "bui-avatar-block__title"}).text.strip('\n')
    except:
        username = None
    try:
        date = review_li.find(
            "ul", {
                "class": "bui-list bui-list--text bui-list--icon bui_font_caption c-review-block__row c-review-block__stay-date"}
        ).find(
            "div", {"class": "bui-list__body"}).text.strip("\n").split('\n')[-1]
    except:
        date = None
    try:
        no_of_nights = float(review_li.find(
            "ul", {
                "class": "bui-list bui-list--text bui-list--icon bui_font_caption c-review-block__row c-review-block__stay-date"}
        ).find(
            "div", {"class": "bui-list__body"}).text.strip("\n").split('\n')[0].split(" ")[0])
    except:
        no_of_nights = None

    return title, positive_des, negative_des, rating, room_type, user_country, type_of_travel, username, date, no_of_nights


def scrape_reviews_per_page(parsed_html, hotel_id):
    review_lis = parsed_html.findAll("li", {"class": "review_list_new_item_block"})

    review_list = []

    for review_li in review_lis:
        title, positive_des, negative_des, rating, room_type, user_country, type_of_travel, username, date, no_of_nights = scrape_individual_review(
            review_li)
        review_dict = {
            "hotel_id": hotel_id,
            "title": title,
            "positive_des": positive_des,
            "negative_des": negative_des,
            "rating": rating,
            "user_country": user_country,
            "type_of_travel": type_of_travel,
            "username": username,
            "date": date,
            "no_of_nights": no_of_nights,
            "room_type": room_type,
        }
        review_list.append(review_dict)

    return review_list


def scrape_all_reviews(hotel_id):
    global number_of_requests
    page_number = 1
    page_url = f"https://www.booking.com/reviewlist.en-gb.html?aid=304142" \
               f"&label=gen173nr-1FCAEoggI46AdIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuALB_qWZBsACAdICJGNhZTk4NDY3LWVlNjMtNDIxYi1hNTBmLTcwMWI5ZTRkNzlmZdgCBuACAQ&sid=4e3129dc516ce958ec65f7f0b34cbcae&cc1=sg;dist=1" \
               f";length_of_stay=1" \
               f";pagename={hotel_id}" \
               f";srpvid=bdcb40f4acab0595" \
               f";type=total" \
               f"&&offset={page_number * 10 - 10}" \
               f";rows=10"

    # Get the last page number

    headers = {
        "User-Agent": next(user_agent_list_cycle)
    }

    try:
        response = requests.get(page_url, headers=headers)
        number_of_requests += 1
        print(f"request number {number_of_requests}")
    except:
        return "CANNOT REQUEST"

    if response.status_code != 200:
        print(f"{page_url} at page {page_number} has a problem")
        return []

    html = response.content

    parsed_html = BeautifulSoup(html, 'lxml')

    try:
        last_page = int(parsed_html.findAll("span", {"class": "bui-u-sr-only"})[-1].text.split(" ")[-1])
    except:
        last_page = 200

    all_review_list = []

    while page_number <= last_page:
        page_url = f"https://www.booking.com/reviewlist.en-gb.html?aid=304142" \
                   f"&label=gen173nr-1FCAEoggI46AdIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuALB_qWZBsACAdICJGNhZTk4NDY3LWVlNjMtNDIxYi1hNTBmLTcwMWI5ZTRkNzlmZdgCBuACAQ&sid=4e3129dc516ce958ec65f7f0b34cbcae&cc1=sg;dist=1" \
                   f";length_of_stay=1" \
                   f";pagename={hotel_id}" \
                   f";srpvid=bdcb40f4acab0595" \
                   f";type=total" \
                   f"&&offset={page_number * 10 - 10}" \
                   f";rows=10"
        print(page_url)

        try:
            random_delay()
            response = requests.get(page_url, headers=headers)
            number_of_requests += 1
            print(f"request number {number_of_requests}")
        except:
            return "CANNOT REQUEST"

        page_number += 1
        print(page_number)
        if response.status_code != 200:
            continue
        html = response.content

        parsed_html = BeautifulSoup(html, 'lxml')
        if parsed_html.find("p", {"class", "bui-empty-state__text"}):
            break

        all_review_list.extend(scrape_reviews_per_page(parsed_html, hotel_id))

    return all_review_list


sample_links = [
    "https://www.booking.com/hotel/sg/hilton-singapore-orchard.en-gb.html?label=gen173nr-1FCAsoyQE4qAZIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKMlKqZBsACAdICJGQ4MTA3MTVkLTI3Y2YtNGVmYS1iNDViLTc4MzIxOThjMmMzZtgCBuACAQ&sid=4e3129dc516ce958ec65f7f0b34cbcae&aid=304142&ucfs=1&arphpl=1&checkin=2022-10-18&checkout=2022-10-19&dest_id=-73635&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=1&hapos=1&sr_order=popularity&srpvid=24bd38c221ac019c&srepoch=1663747462&all_sr_blocks=2503023_344328142_2_2_0&highlighted_blocks=2503023_344328142_2_2_0&matching_block_id=2503023_344328142_2_2_0&sr_pri_blocks=2503023_344328142_2_2_0__65797&tpi_r=2&from_sustainable_property_sr=1&from=searchresults#hotelTmpl",
    "https://www.booking.com/hotel/sg/81-geylang.en-gb.html?label=gen173nr-1FCAsoyQE4qAZIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKMlKqZBsACAdICJGQ4MTA3MTVkLTI3Y2YtNGVmYS1iNDViLTc4MzIxOThjMmMzZtgCBuACAQ&sid=4e3129dc516ce958ec65f7f0b34cbcae&aid=304142&ucfs=1&arphpl=1&checkin=2022-10-18&checkout=2022-10-19&dest_id=-73635&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=2&hapos=2&sr_order=popularity&srpvid=24bd38c221ac019c&srepoch=1663747462&all_sr_blocks=17562201_270991548_0_0_0&highlighted_blocks=17562201_270991548_0_0_0&matching_block_id=17562201_270991548_0_0_0&sr_pri_blocks=17562201_270991548_0_0_0__7001&tpi_r=2&from_sustainable_property_sr=1&from=searchresults#hotelTmpl",
    "https://www.booking.com/hotel/sg/novotel-singapore-on-stevens.en-gb.html?aid=304142&label=gen173nr-1FCAsoyQE4qAZIM1gEaMkBiAEBmAEJuAEHyAEM2AEB6AEB-AELiAIBqAIDuAKMlKqZBsACAdICJGQ4MTA3MTVkLTI3Y2YtNGVmYS1iNDViLTc4MzIxOThjMmMzZtgCBuACAQ&sid=4e3129dc516ce958ec65f7f0b34cbcae&all_sr_blocks=257344502_104436455_2_42_0;checkin=2022-10-18;checkout=2022-10-19;dest_id=-73635;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=326;highlighted_blocks=257344502_104436455_2_42_0;hpos=1;matching_block_id=257344502_104436455_2_42_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;show_room=257344502;sr_order=bayesian_review_score;sr_pri_blocks=257344502_104436455_2_42_0__37899;srepoch=1663777514;srpvid=24bd38c221ac019c;type=total;ucfs=1&#RD257344502"
]

all_hotel_data = []
all_reviews_data = []

def write_to_csv(col_name, hotel_data):
    with open("reviewsDataOfficial.csv", 'w') as csvFile:
        wr = csv.DictWriter(csvFile, fieldnames=col_name)
        wr.writeheader()
        # print(hotel_data)
        for ele in hotel_data:
            wr.writerow(ele)


def scrape_general_data(hotel_links):
    global number_of_requests
    start_time = time.time()

    # linked_list = scrape_hotel_links(start_url)



    all_hotel_data = []
    all_reviews_data = []
    for index, link in enumerate(hotel_links):
        hotel_id = link.split("/sg/")[1].split(".en-gb.html")[0]
        hotel_data = scrape_hotel_data(link, hotel_id)
        print(f"hotel_data is {hotel_data}")
        if hotel_data == "CANNOT REQUEST":
            print("hotel_name is", link)
            print(f"number of requests made is {number_of_requests}")
            col_name = list(all_hotel_data[0].keys())
            write_to_csv(col_name, all_hotel_data)
            quit()
        all_hotel_data.append(hotel_data)



        # review_data = scrape_all_reviews(hotel_id)
        # all_reviews_data.extend(review_data)

    print(all_hotel_data)
    col_name = list(all_hotel_data[0].keys())
    write_to_csv(col_name, all_hotel_data)

    # col_name = list(all_reviews_data[0].keys())
    # with open("reviewsData3.csv", 'w') as csvFile:
    #     wr = csv.DictWriter(csvFile, fieldnames=col_name)
    #     wr.writeheader()
    #     print(all_reviews_data)
    #     for ele in all_reviews_data:
    #         wr.writerow(ele)

    print("--- %s seconds ---" % (time.time() - start_time))


def scrape_reviews_data(hotel_links):
    global number_of_requests
    start_time = time.time()

    # linked_list = scrape_hotel_links(start_url)

    all_reviews_data = []
    for index, link in enumerate(hotel_links):

        if number_of_requests % 1000 == 0:
            time.sleep(20)


        hotel_id = link.split("/sg/")[1].split(".en-gb.html")[0]
        reviews_data = scrape_all_reviews(hotel_id)
        if reviews_data == "CANNOT REQUEST":
            print("hotel_name is", link)
            print(f"number of requests made is {number_of_requests}")
            col_name = list(all_reviews_data[0].keys())
            write_to_csv(col_name, all_reviews_data)
            print("--- %s seconds ---" % (time.time() - start_time))
            quit()

        all_reviews_data.extend(reviews_data)



        # review_data = scrape_all_reviews(hotel_id)
        # all_reviews_data.extend(review_data)
    try:
        col_name = list(all_reviews_data[0].keys())
        write_to_csv(col_name, all_reviews_data)
    except:
        col_name = ["HotelName", "Title", "NegativeDescription", "Rating", "Room_Type", "User_Country", "Type_Of_Traveller", "Username", "Date", "No_Of_Nights"]
        write_to_csv(col_name, all_reviews_data)

    # col_name = list(all_reviews_data[0].keys())
    # with open("reviewsData3.csv", 'w') as csvFile:
    #     wr = csv.DictWriter(csvFile, fieldnames=col_name)
    #     wr.writeheader()
    #     print(all_reviews_data)
    #     for ele in all_reviews_data:
    #         wr.writerow(ele)




def main():
    threads = list()

    for link in sample_links:
        x = threading.Thread(target=scrape_general_data, args=([link],))
        threads.append(x)
        x.start()

    col_name = list(all_hotel_data[0].keys())
    with open("generalData2.csv", 'w') as csvFile:
        wr = csv.DictWriter(csvFile, fieldnames=col_name)
        wr.writeheader()
        for ele in all_hotel_data:
            wr.writerow(ele)

    col_name = list(all_reviews_data[0].keys())
    with open("reviewsData2.csv", 'w') as csvFile:
        wr = csv.DictWriter(csvFile, fieldnames=col_name)
        wr.writeheader()
        for ele in all_reviews_data:
            wr.writerow(ele)




scrape_reviews_data(links)


# url = ""
# try:
#     url = sys.argv[1]
# except:
#     print("Invalid URL.")
#     quit()
#
# print(url)
# generalColNames = ["HotelID", "HotelName", "HotelStars", "Cat_Staff", "Cat_Facilities", "Cat_Cleanliness", "Cat_Comfort",
#                  "Cat_ValueForMoney", "Cat_Location", "Address", "Room_Types", "ImageLink"]
# reviewColNames = ["HotelName", "Title", "NegativeDescription", "Rating", "Room_Type", "User_Country",
#                     "Type_Of_Traveller", "Username", "Date", "No_Of_Nights"]
# scrape_data([url], generalColNames, reviewColNames)


# print("Running")
# links = scrape_hotel_links(["https://www.booking.com/searchresults.html?ss=Singapore&ssne=Singapore&ssne_untouched=Singapore&label=bdot-Os1*aFx2GVFdW3rxGd0MYQS461500239550%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-334108349%3Alp9062541%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YYriJK-Ikd_dLBPOo0BdMww&sid=166c1c075d1732186b790eaa131584d0&aid=378266&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-73635&dest_type=city&checkin=2023-07-01&checkout=2023-07-02&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure"])
# print(links)


