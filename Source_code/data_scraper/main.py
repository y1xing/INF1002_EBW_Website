import time
import csv
import sys
import os
# sys.path.append("/scraper")
# from scraper.hotel_scraper import scrape_hotel_links
# import scraper.extraction
# from scraper.extraction import scrape_hotel_data, scrape_all_reviews, scrape_hotel_links, scrape_data
# import extraction

url = "https://www.booking.com/searchresults.html?ss=Singapore&ssne=Singapore&ssne_untouched=Singapore&label=bdot-Os1*aFx2GVFdW3rxGd0MYQS461500239550%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-334108349%3Alp9062541%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YYriJK-Ikd_dLBPOo0BdMww&sid=166c1c075d1732186b790eaa131584d0&aid=378266&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-73635&dest_type=city&checkin=2023-07-01&checkout=2023-07-02&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure"
cwd = os.getcwd()
os.chdir(f"{cwd}/scraper")
os.system(f'py ./extraction.py "{url}"')


# url = [
#     "https://www.booking.com/searchresults.html?ss=Singapore&ssne=Singapore&ssne_untouched=Singapore&label=bdot-Os1*aFx2GVFdW3rxGd0MYQS461500239550%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-334108349%3Alp9062541%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YYriJK-Ikd_dLBPOo0BdMww&sid=166c1c075d1732186b790eaa131584d0&aid=378266&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-73635&dest_type=city&checkin=2023-07-01&checkout=2023-07-02&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure"]
# gen_col_names = ["HotelID", "HotelName", "HotelStars", "Cat_Staff", "Cat_Facilities", "Cat_Cleanliness", "Cat_Comfort",
#                  "Cat_ValueForMoney", "Cat_Location", "Address", "Room_Types", "ImageLink"]
# review_col_names = ["HotelName", "Title", "NegativeDescription", "Rating", "Room_Type", "User_Country",
#                     "Type_Of_Traveller", "Username", "Date", "No_Of_Nights"]
# scrape_data(url, gen_col_names, review_col_names)

# start_time = time.time()
# print("Hi")
# linked_list = scrape_hotel_links(url)
# print(linked_list)
# all_hotel_data = []
# all_reviews_data = []
# print(linked_list)
# for link in linked_list[:10]:
#     hotel_id = link.split("/sg/")[1].split(".en-gb.html")[0]
#     hotel_data = scrape_hotel_data(link, hotel_id)
#     print(hotel_data)
#     review_data = scrape_all_reviews(hotel_id)
#     print(review_data)
#     all_reviews_data.extend(review_data)
# # print(all_reviews_data)
#
# # col_name = list(all_hotel_data[0].keys())
# with open("generalData3.csv", 'w') as csvFile:
#     wr = csv.DictWriter(csvFile, fieldnames=gen_col_names)
#     wr.writeheader()
#     print(all_hotel_data)
#     for ele in all_hotel_data:
#         wr.writerow(ele)
#
# # col_name = list(all_reviews_data[0].keys())
# with open("reviewsData3.csv", 'w') as csvFile:
#     wr = csv.DictWriter(csvFile, fieldnames=review_col_names)
#     wr.writeheader()
#     print(all_reviews_data)
#     for ele in all_reviews_data:
#         wr.writerow(ele)
#
# print("--- %s seconds ---" % (time.time() - start_time))
