from flask import Flask
from flask_restful import Api, Resource
import pandas as pd
import ast
import json


app = Flask(__name__, static_folder='../build', static_url_path='/')
api = Api(app)


colors = ['#008B8B', '#4CAF50', '#FF9800', '#0C7CD5', '#8A2BE2', '#006400', '#20B2AA', '#000080', '#CD853F', '#FF69B4',
          '#FFD700', '#F5DEB3', '#FF0000'

          ]

# Reads all the data from the csv files
general_data = pd.read_csv("./dataset/generalDataClean.csv")
general_data = general_data.drop(columns=["room_types", "Unnamed: 0"])
general_cols = list(general_data.columns)
review_data = pd.read_csv("./dataset/ReviewCat3.csv")
review_data_sentiment = pd.read_csv("./dataset/Csv_Darren.csv")
hotel_id_data = pd.read_csv("./dataset/hotel_and_hotel_id.csv")
hotel_id_data['lower_hotel_name'] = hotel_id_data['hotel_name'].str.lower()


# API call to check if the hotel name inputted by the user exists in the database
class ValidateHotelName(Resource):
    def get(self, hotel_name):
        try:
            # Return the closest match to the hotel
            return {
                "hotel_id": hotel_id_data[hotel_id_data['lower_hotel_name'].str.contains(hotel_name.lower())].iloc[0].hotel_id,
                "hotel_name": hotel_id_data[hotel_id_data['lower_hotel_name'].str.contains(hotel_name.lower())].iloc[0].hotel_name,
            }

        except IndexError:
            return {"hotel_id": "No such hotel"}

# API Call to get the general hotel data from the hotel_id field


class GeneralData(Resource):
    def get(self, hotel_id):
        try:
            # Gets the index of the hotel id from the general data
            index = general_data.index[general_data["hotel_id"] == hotel_id].to_list()[
                0]
            # Gets the hotel data from the general data
            data = general_data.iloc[index, :]
            # Stores all the data in a dictionary and returns it in the json format
            result = data.to_dict()
            # Format the roomtypes_clean data to fit frontend
            result["roomtypes_clean"] = ast.literal_eval(
                result["roomtypes_clean"])
            for key, values in result["roomtypes_clean"].items():
                int_values = list(
                    map(lambda x: float(x.replace(",", "")), values))
                result["roomtypes_clean"][key] = sum(
                    int_values) / len(int_values)

            # Format the data for the frontend to load
            result["roomtypes_clean"] = {
                "categories": [key for key, values in result["roomtypes_clean"].items()],
                "values": [values for key, values in result["roomtypes_clean"].items()],
            }

            return result
        except IndexError:
            return {}


# API Call to get the average rating for each type of room for the hotel
class RoomTypesAverageRating(Resource):
    def get(self, hotel_id):
        try:
            # Gets the room types from the general data and stores it in a list
            general_index = general_data.index[general_data["hotel_id"] == hotel_id].to_list()[
                0]
            data = ast.literal_eval(general_data.iloc[general_index, 11])
            room_types = list(data.keys())
            # Gets the average rate for each room type and stores all the averages in a list
            average_list = []
            for i in room_types:
                indexes = review_data.index[
                    (review_data["hotel_id"] == hotel_id) & (review_data["room_type"] == i)].to_list()
                df = review_data.iloc[indexes]
                average_list.append(df["rating"].mean())
            # Returns the result
            result = {"categories": room_types, "values": average_list}
            print(result)
            return result
        except IndexError:
            return {}


# API Call to get the number of reviews per room type across the different months in order to show demand
class RoomTypesNoOfReviews(Resource):
    def get(self, hotel_id):
        try:
            # Gets the room types from the general data and stores it in a list
            general_index = general_data.index[general_data["hotel_id"] == hotel_id].to_list()[
                0]
            data = ast.literal_eval(general_data.iloc[general_index, 11])
            room_types = list(data.keys())
            # Gets the number of reviews for each month for each room type and stores them all in a dict
            result = {}
            months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
            for i in room_types:
                month_num_list = []
                room_type_indexes = review_data.index[
                    (review_data["hotel_id"] == hotel_id) & (review_data["room_type"] == i)].to_list()
                df = review_data.iloc[room_type_indexes]
                # Gets the number of reviews per month and stores it in a list
                for j in months:
                    month_indexes = df.index[df["month"] == j]
                    month_df = review_data.iloc[month_indexes]
                    month_num_list.append(int(month_df["month"].count()))
                result[i] = month_num_list
            data = {"series": []}
            count = 0

            # Formatting for frontend to render
            for key, values in result.items():
                data["series"].append(
                    {
                        "data": values,
                        "name": key,
                        "color": colors[count]
                    }
                )
                count += 1
            return data
        except IndexError:
            return {}

# API Call to get the top 10 words that appeared in positive reviews and 5 reviews that has the word in it


class PositiveWordsFrequency(Resource):
    def get(self, hotel_idCountryTraveler):

        # Split the argumemnt
        hotel_id, country, traveler = hotel_idCountryTraveler.split("+")

        # Filter the dataframe based on the parameters of the API Call
        if country.lower() == "everything" and traveler.lower() == "everything":
            filteredhotels = review_data.loc[review_data["hotel_id"] == hotel_id]
        elif country.lower() == "everything":
            filteredhotels = (review_data.loc[(review_data["hotel_id"] == hotel_id)
                                              & (review_data["type_of_travel"] == traveler)])
        elif traveler.lower() == "everything":
            filteredhotels = (review_data.loc[(review_data["hotel_id"] == hotel_id)
                                              & (review_data["user_country"] == country)])
        else:
            # filtered rows, perform wordcloud on these
            filteredhotels = (review_data.loc[(review_data["hotel_id"] == hotel_id)
                                              & (review_data["user_country"] == country)
                                              & (review_data["type_of_travel"] == traveler)])

        filteredhoteldict = filteredhotels.to_dict()

        text = " ".join(reviews for reviews in filteredhoteldict.get(
            "pos_des_cleaned").values())

        # store each word into a list - seperate word by spaces
        wordlist = text.split()

        word_count = {}

        # for each word in wordlist
        for word in wordlist:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        sorted_words = dict(
            sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10])

        # 5 reviews containing these top words
        keylist = list(sorted_words.keys())

        positive_desc = list(filteredhoteldict.get(
            "pos_des_cleaned").values())

        api_word_list = []

        # Format the data for frontend to render
        for key, values in sorted_words.items():
            if key == "no_pos_des":
                continue
            else:
                positive_des_full = []
                count = 0
                for j in range(len(positive_desc)):

                    if key in positive_desc[j]:
                        positive_des_full.append(
                            filteredhotels.loc[filteredhotels['pos_des_cleaned'] == positive_desc[j], "positive_des"].iloc[0])
                        count += 1
                        if count == 5:
                            break
                if len(positive_des_full) == 0:
                    positive_des_full = ["No review like that"]
                tmp_dict = {
                    "word": key,
                    "count": int(values),
                    "sampleReview": positive_des_full[0],
                    "fiveReviews": positive_des_full,
                }

                api_word_list.append(tmp_dict)

        return api_word_list


# API Call to get the top 10 words that appeared in positive reviews and 5 reviews that has the word in it
class NegativeWordsFrequency(Resource):
    def get(self, hotel_idCountryTraveler):

        # Split the argument from the API Call into different variables
        hotel_id, country, traveler = hotel_idCountryTraveler.split("+")

        # Filter the dataframe based on the parameters of the API Call
        if country.lower() == "everything" and traveler.lower() == "everything":
            filteredhotels = review_data.loc[review_data["hotel_id"] == hotel_id]
        elif country.lower() == "everything":
            filteredhotels = (review_data.loc[(review_data["hotel_id"] == hotel_id)
                                              & (review_data["type_of_travel"] == traveler)])
        elif traveler.lower() == "everything":
            filteredhotels = (review_data.loc[(review_data["hotel_id"] == hotel_id)
                                              & (review_data["user_country"] == country)])
        else:
            # filtered rows, perform wordcloud on these
            filteredhotels = (review_data.loc[(review_data["hotel_id"] == hotel_id)
                                              & (review_data["user_country"] == country)
                                              & (review_data["type_of_travel"] == traveler)])

        filteredhoteldict = filteredhotels.to_dict()

        text = " ".join(reviews for reviews in filteredhoteldict.get(
            "neg_des_cleaned").values())

        # store each word into a list - seperate word by spaces
        wordlist = text.split()

        word_count = {}

        # for each word in wordlist
        for word in wordlist:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        sorted_words = dict(
            sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10])

        # 5 reviews containing these top words
        keylist = list(sorted_words.keys())

        negative_desc = list(filteredhoteldict.get(
            "neg_des_cleaned").values())

        api_word_list = []

        # Format data for the frontend
        for key, values in sorted_words.items():
            if key == "no_neg_des":
                continue
            else:
                negative_des_full = []
                count = 0
                for j in range(len(negative_desc)):

                    if key in negative_desc[j]:
                        negative_des_full.append(
                            filteredhotels.loc[filteredhotels['neg_des_cleaned'] == negative_desc[j], "negative_des"].iloc[0])
                        count += 1
                        if count == 5:
                            break
                if len(negative_des_full) == 0:
                    negative_des_full = ["No review like that"]
                tmp_dict = {
                    "word": key,
                    "count": int(values),
                    "sampleReview": negative_des_full[0],
                    "fiveReviews": negative_des_full,
                }

                api_word_list.append(tmp_dict)

        return api_word_list


# API Call to get all the country and travelers from a hotel to populate filter options
class GetCountryAndTravelers(Resource):
    def get(self, hotel_id):
        hotel_df = review_data.loc[review_data['hotel_id'] == hotel_id]

        # Get list of countries and sort them
        user_countries = list(set(hotel_df['user_country']))
        user_countries_cleaned = sorted([country.replace(
            '\u200b', '') for country in user_countries if type(country) == str])

        # Get list of travelers and sort them
        travelers = list(set(hotel_df['type_of_travel']))
        travelers_clean = [
            traveler for traveler in travelers if type(traveler) == str]

        user_countries_cleaned.insert(0, "Everything")
        travelers_clean.insert(0, "Everything")

        return {
            "countries": user_countries_cleaned,
            "traveler": travelers_clean
        }


# API Call to get sentiments of reviews based on categories of review
class GetSentiment(Resource):
    def get(self, hotel_idCountryTraveler):
        hotel_id, country, traveler = hotel_idCountryTraveler.split("+")

        # Filter the hotel based on the API argument
        if country.lower() == "everything" and traveler.lower() == "everything":
            filteredhotels = review_data_sentiment.loc[review_data_sentiment["hotel_id"] == hotel_id]
        elif country.lower() == "everything":
            filteredhotels = (review_data_sentiment.loc[(review_data_sentiment["hotel_id"] == hotel_id)
                                                        & (review_data_sentiment["type_of_travel"] == traveler)])
        elif traveler.lower() == "everything":
            filteredhotels = (review_data_sentiment.loc[(review_data_sentiment["hotel_id"] == hotel_id)
                                                        & (review_data_sentiment["user_country"] == country)])
        else:
            filteredhotels = (review_data_sentiment.loc[(review_data_sentiment["hotel_id"] == hotel_id)
                                                        & (review_data_sentiment["user_country"] == country)
                                                        & (review_data_sentiment["type_of_travel"] == traveler)])

        review_categories = ['location', 'staff', 'cleanliness',
                             'comfort', 'facilities', 'value for money']

        sentiments = {}

        for category in review_categories:
            # Filter dataframe to only have curent category of review
            df = filteredhotels[(filteredhotels['pos_cat'].str.contains(category)) | (
                filteredhotels['neg_cat'].str.contains(category))]

            # Combine both pos and neg review sentiment to get a score from 0 - 1
            df['total_compound'] = df['compound_x'] + df['compound_y']
            max_value = max(df['total_compound'])
            min_value = min(df['total_compound'])
            df['total_compound_percentage'] = df['total_compound'].apply(
                lambda x: (x - min_value) / (max_value - min_value))

            # Only positive review and its average sentiment score
            no_neg_score = df[df['neg_des_cleaned'] ==
                              "no_neg_des"]["total_compound_percentage"].mean()

            # Only negative review and its average sentiment score
            no_pos_score = df[df['pos_des_cleaned'] ==
                              "no_pos_des"]["total_compound_percentage"].mean()

            # Get the number of reviews that has a higher score that no_neg_score
            pos_review = len(
                df[df["total_compound_percentage"] > no_neg_score])

            # Get the number of reviews that has a lower score that no_pos_score
            neg_review = len(
                df[df["total_compound_percentage"] <= no_pos_score])

            # Get the mean sentiment score
            mean = df["total_compound_percentage"].mean()

            # Format data for frontend to render
            sentiments[category] = {

                "series": [
                    {
                        "color": '#688eff',
                        "data": "{:.1f}".format(mean * 100),
                        "label": 'AverageSentiment Score'
                    },
                ],
                "numberOfReviews": [
                    {
                        "data": pos_review,
                        "color": '#4CAF50',
                        "label": "Positive Reviews"
                    },
                    {
                        "data": neg_review,
                        "color": '#ff3333',
                        "label": "Negative Reviews"
                    },
                ]
            }

        return sentiments


# API Calls and their respective routes
api.add_resource(ValidateHotelName, "/checkHotel/<hotel_name>")
api.add_resource(GeneralData, "/general/<hotel_id>")
api.add_resource(RoomTypesAverageRating,
                 "/room_types_average_rating/<hotel_id>")
api.add_resource(RoomTypesNoOfReviews, "/room_types_no_reviews/<hotel_id>")
api.add_resource(PositiveWordsFrequency,
                 "/wordFrequency/<hotel_idCountryTraveler>")
api.add_resource(NegativeWordsFrequency,
                 "/negwordFrequency/<hotel_idCountryTraveler>")
api.add_resource(GetCountryAndTravelers,
                 "/countryAndTraveler/<hotel_id>")
api.add_resource(GetSentiment,
                 "/sentiment/<hotel_idCountryTraveler>")


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/')
def index():
    return {'data': "API CALL HERE"}
