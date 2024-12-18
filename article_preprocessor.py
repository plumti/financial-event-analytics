import os
import time
import csv
import logging
import re
from crewai import Crew
from dotenv import load_dotenv
import subprocess
import schedule
from reddit_scraper import scrape_subreddit, TextProcessor
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
# Setup environment
load_dotenv()

company_names = []

# Setup logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
text_processor = TextProcessor()


def load_companies(csv_file_path):
        df = pd.read_csv(csv_file_path)
        return df['company_name'].tolist()

def read_company_info(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df = df.drop(columns=['ID', 'Author'], errors='ignore')
    company_info = df.to_dict(orient='records')
    return company_info

def load_existing_urls(file_path):
    if not os.path.exists(file_path):
        return set()

    df = pd.read_csv(file_path)
    return set(df['URL'])

def load_processed_urls(file_path):
    if not os.path.exists(file_path):
        return set()
    
    df = pd.read_csv(file_path)
    return set(df['Article URL'])

def read_company_for_event_extraction(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Select only the relevant columns
    df = df[['Company', 'Article URL', 'Article Content', 'Submission Date']]
    
    # Convert the DataFrame to a list of dictionaries
    company_info = df.to_dict(orient='records')
    
    return company_info



def analyze_sentiment(self, text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


def calculate_average_polarity(file_path):
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    if df.empty:
        return None
    
    df['Polarity Score'] = df['Polarity Score'].astype(float)
    return df['Polarity Score'].mean()

def write_daily_average(file_path, average_polarity):
    today = datetime.now().date()
    daily_avg_file_path = file_path.replace('.csv', '_daily_avg.csv')

    if not os.path.exists(daily_avg_file_path):
        with open(daily_avg_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Date', 'Average Polarity Score'])

    with open(daily_avg_file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([today, average_polarity])
    
    csv_file_path = '/teamspace/studios/this_studio/crewai-groq-reddit/data/companies.csv'
    results_csv_path = '/teamspace/studios/this_studio/crewai-groq-reddit/data/sentiment_results.csv'

    # Create the results CSV file if it doesn't exist and write the header
    if not os.path.exists(results_csv_path):
        with open(results_csv_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Company', 'Article URL', 'Article Content', 'Polarity Score', 'Submission Date'])

    existing_urls = load_existing_urls(results_csv_path)

    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)

        for company in csv_reader:
            company_name = company['company_name']
            company_names.append(company_name)
            print(company_name)

            scraped_articles = scrape_subreddit(company_name, 4)

            for article in scraped_articles:
                article_content = article['content']
                article_url = article['url']
                submission_date = article['submission_date']

                if not article_content.strip():
                    continue

                if article_url in existing_urls:
                        print(f"Skipping duplicate article: {article_url}")
                        continue
                polarity_score = analyze_sentiment(text_processor,article_content)
                print(polarity_score)
                if polarity_score == 0:
                    print(f"Skipping article with polarity 0: {article}")
                    continue

                # Append the results to the CSV file
                with open(results_csv_path, 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([company_name, article_url, article_content, polarity_score, submission_date])
                
        

    average_polarity = calculate_average_polarity(results_csv_path)
    print(f"Average Polarity Score: {average_polarity}")

    # Write the daily average sentiment score to the CSV file
    if average_polarity is not None:
        write_daily_average(results_csv_path, average_polarity)