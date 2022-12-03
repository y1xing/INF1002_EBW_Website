## Getting Started

data_scraper directory consists of files we used to scrape data from Booking.com
- The main codes used to scrape are in scraper->hotel_scraper.py and scraper->extraction.py

Datasets directory consists of csv files that was generated from
1. Data scraping
2. Data cleaning

Analysis_Notebooks directory consists of jupyter notebooks used to
1. Do data cleaning
2. Overall Analysis for the report
3. Classifer Algorithm to classify reviews
4. Vader-sa algorithm for sentiment analysis

## To run the website

First, run the flask backend:

```bash
# Enter into the API directory to run backend
cd api
pip install -r requirements.txt
pip install flask python-dotenv
FLASK_APP=api.py
FLASK_ENV=development
flask run

```
Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) with your browser to see the result.

Then, run the nextjs/react frontennd:

```bash
# On the main directory

npm install
npm run dev


```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

