from reddit_scraper import scrape_subreddit
from article_preprocessor import load_companies
from extraction import event_extract
import os 
from dotenv import load_dotenv

class trading_project():

    csv_file_path = "/teamspace/studios/this_studio/trading-project-2024/data/companies.csv"

    for company in load_companies(csv_file_path):
        scrape_subreddit(company, 5)
        event_extract.event_id(company)