# reddit_scraper.py
import csv
import os
import glob
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from charset_normalizer import from_bytes
import praw

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent, subreddit_name):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.subreddit_name = subreddit_name

    def fetch_submissions(self, limit=90):
        subreddit = self.reddit.subreddit(self.subreddit_name)
        return subreddit.new(limit=limit)

class TextProcessor:
    def fetch_article_content(self, url):
        try:
            if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
                print(f"Skipping image URL: {url}")
                return ""
                
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            guess_encoding = from_bytes(response.content).best()
            if guess_encoding is None:
                print(f"Unable to guess encoding for {url}, skipping.")
                return ""
            response.encoding = guess_encoding.encoding
            content = response.text
            
            soup = BeautifulSoup(content, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = ' '.join(para.get_text() for para in paragraphs)
            cleaned_article_text = ' '.join(article_text.split())

            return cleaned_article_text
        except Exception as e:
            print(f"Error fetching article content for {url}: {e}")
            return ""

class DataSaver:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    @staticmethod
    def get_next_filename(prefix, suffix):
        existing_files = glob.glob(f"{prefix}_*.{suffix}")
        max_num = 0
        for file in existing_files:
            try:
                num = int(file.replace(prefix + '_', '').replace('.' + suffix, ''))
                max_num = max(max_num, num)
            except ValueError:
                continue
        return f"{prefix}_{max_num + 1}.{suffix}"

   

def scrape_subreddit(subreddit_name, limit):
    today_date = datetime.now().strftime('%Y%m%d')
    output_dir = "/teamspace/studios/this_studio/trading-project-2024/data/"
    csv_prefix = os.path.join(output_dir, f"{subreddit_name}_articles_{today_date}")
    csv_suffix = 'csv'

    reddit_scraper = RedditScraper(
        client_id='Lwj_z2HwieLmFE-Q45hSKQ',
        client_secret='eIi-k_8746ovHx35V7vqvDyhWo3LUQ',
        user_agent='redditdev scraper-bot by u/Sad_Bonus_4248.',
        subreddit_name=subreddit_name
    )

    text_processor = TextProcessor()
    data_saver = DataSaver(output_dir)
    csv_file = data_saver.get_next_filename(csv_prefix, csv_suffix)

    articles = []

    collection_file_path = os.path.join(output_dir, f"/teamspace/studios/this_studio/trading-project-2024/data/{subreddit_name}_article_collection.csv")
    if not os.path.exists(collection_file_path):
        with open(collection_file_path, 'w', newline='', encoding='utf-8') as collection_file:
            csv_writer = csv.writer(collection_file)
            csv_writer.writerow(['Company','Title', 'URL', 'Article Content', 'Submission Date'])

    existing_urls = set()
    with open(collection_file_path, 'r', encoding='utf-8') as collection_file:
        csv_reader = csv.reader(collection_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            existing_urls.add(row[2])


        with open(collection_file_path, 'a', newline='', encoding='utf-8') as collection_file:
            collection_writer = csv.writer(collection_file)
            
            for submission in reddit_scraper.fetch_submissions(limit=limit):
                if submission.url in existing_urls:
                    print(f"Skipping duplicate URL: {submission.url}")
                    continue

                article_content = text_processor.fetch_article_content(submission.url)
                if not article_content.strip():
                    print(f"Article content for {submission.url} is empty after processing, skipping.")
                    continue

                submission_date = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d')
                article_info = {
                    'company': subreddit_name,
                    'title': submission.title,
                    'url': submission.url,
                    'content': article_content,
                    'submission_date': submission_date
                }
                articles.append(article_info)

                collection_writer.writerow([
                    subreddit_name,
                    submission.title,
                    submission.url,
                    article_content,
                    submission_date
                ])

    return articles

# Example usage