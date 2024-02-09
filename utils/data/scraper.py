import logging
from datetime import datetime, date, timedelta
import requests as r
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import mysql.connector

logging.basicConfig(filename='scraper_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %('
                                                                           'message)s')

load_dotenv()

conn = mysql.connector.connect(host=,
                               user=,
                               password=,
                               database=,
                               ssl_ca=,
                               ssl_verify_identity=True,
                               )


class Parser:
    """
    This class scrapes reviews from consumeraffairs.com and stores them in a SQLite database.
    The database is created if it doesn't exist.  The reviews table is created if it doesn't exist.
    The database path and headers are passed in as arguments.  The database path is required, but the headers are
    optional.  If no headers are passed in, the default headers are used. The default headers are:
    {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Mobile/15E148'
    }

    The class has one method, run(), which is called when the class is instantiated.  The run() method calls the
    get_bank_reviews() method, which scrapes the reviews from the URLs passed in as arguments. The URLs are passed in
    as a list.  The get_bank_reviews() method loops through the URLs and scrapes the reviews from each URL.  The
    reviews are stored in the reviews table in the database.  The reviews table has four columns: id, date, bank,
    rating, and text.  The id column is the primary key and is autoincremented. The date column is the date the
    review was posted. The bank column is the name of the bank the review is for. The rating column is the rating
    the reviewer gave the bank. The text column is the text of the review.

    """

    def __init__(self, urls: list, headers: dict, max_reviews=1000):
        self.urls = urls
        self.max_reviews = max_reviews
        self.headers = headers

    def create_reviews_table(self):
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews_test (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE,
                    bank VARCHAR(255),
                    rating INTEGER,
                    text VARCHAR(255)
                )
            ''')
        conn.commit()

    def clean_date(self, date_str):
        """
        Cleans the date string by removing unnecessary text and whitespace and returns the cleaned date string.

        :param date_str:
        :return date_str:
        """
        try:
            date_str = date_str.replace("Reviewed", "").replace("Updated review", "")
            # Add additional cleaning steps if needed
            return date_str.strip()
        except Exception as e:
            logging.error(f"Error cleaning date: {e}")
            return None

    def format_date(self, date_str):
        """
        Formats the date string to match the format of the date column in the database and returns the formatted date
        string. The format of the date column in the database is '%b/%d/%Y'.
        The date string is converted to datetime type and then converted back to a string in the correct format.

        :param date_str:
        :return date_str:
        """
        try:
            date_str = date_str.replace(", ", "/").replace(".", "").replace(" ", "/")
            date_str = date_str.replace("Sept", "Sep").replace("June", "Jun").replace("July", "Jul")
            date_str = date_str.replace("April", "Apr").replace("March", "Mar")
            return date_str
        except Exception as e:
            logging.error(f"Error formatting date: {e}")
            return None

    def insert_review(self, date_, bank, rating, text):
        try:
            cursor = conn.cursor()
            cursor.execute('''
                                INSERT INTO reviews_test (date, bank, rating, text) VALUES (%s, %s, %s, %s)
                            ''', (date_, bank, rating, text))
            conn.commit()
            logging.info(f"Review inserted: {date_}, {bank}, {rating}, {text}")
        except Exception as e:
            logging.error(f"Error inserting review: {e}")

    def get_bank_reviews(self):
        self.create_reviews_table()
        today = date.today() - timedelta(days=1)
        for url in self.urls:
            bank = url.split('/')[-1].replace('html', '')
            response = r.get(url + "#sort=recent&filter=none", headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                reviews = soup.findAll('div', {'class': 'js-rvw rvw'})
                assert len(reviews) > 0, 'No reviews found'

                for rev in reviews:
                    date_elem = rev.find('p', class_='rvw__rvd-dt')
                    date_str = date_elem.text.__str__().strip()
                    cleaned_date = self.clean_date(date_str)
                    formatted_date = self.format_date(cleaned_date)
                    formatted_date = datetime.strptime(formatted_date, '%b/%d/%Y').date()
                    if formatted_date == today:
                        print(formatted_date, today, bank)
                        try:
                            text = rev.find('div', {'class': 'rvw__top-text'}).find('p').text.__str__().strip()
                        except:
                            text = 'No Text'
                        try:
                            text += rev.find('div', {'class': "rvw__all-text js-expanded"}).text
                        except:
                            pass
                        try:
                            rating = int(rev.find('meta', itemprop='ratingValue')['content'])
                        except:
                            rating = -1
                        self.insert_review(formatted_date, bank, rating, text[:500])
                        print("data inserted")
                    else:
                        break

    def run(self):
        self.get_bank_reviews()
        conn.close()
